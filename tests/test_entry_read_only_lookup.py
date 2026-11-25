"""Ticket 79: a read-only question goes from its index straight to its leaf; only a change takes the start order.

Four texts carry the rule, and this test pins each one exactly:

- `AGENTS.md`, the start order's condition line, with its read-only carve-out;
- `AGENTS.md`, the `read-only-lookup` anchor (on its own line, blank lines around it) and the paragraph,
  between step 5 of the start order and the paragraph that begins "狀態只保存";
- `skills/johnny-project-takeover/SKILL.md`, the frontmatter `description`, which must also be a valid YAML
  plain scalar (a colon and space inside it makes the skill fail to register);
- `skills/johnny-project-takeover/SKILL.md`, section `## Start`: the new first step, then the four original
  steps renumbered 2 to 5, in order.

The check is a function over a root directory (`find_defects`), so each injection case below runs it on a
temporary copy of the two files with one text damaged, and must go red; the unmodified copy must stay green.
A named file that is missing or not UTF-8 is a defect that names the file.

The frontmatter is parsed by `parse_frontmatter`, a small strict reader of the one shape the skill file uses
(`key: plain scalar`, one line each). It applies the YAML 1.2 plain-scalar rules that matter here (no `: `, no
` #`, no leading indicator, no trailing colon) and rejects every line shape it does not know, so it fails
closed. It is written here because PyYAML is not in `requirements-dev.txt` and has no stubs under
`mypy --strict`.
"""
from __future__ import annotations

import re
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

AGENTS = "AGENTS.md"
SKILL = "skills/johnny-project-takeover/SKILL.md"

START_ORDER_HEADING = "## 啟動順序"
OLD_CONDITION = "在讀取 target source、執行工具或寫入前："
CONDITION = "除下方唯讀查詢外，在讀取 target source、執行工具或寫入前："
ANCHOR = '<a id="read-only-lookup"></a>'
STATE_PARAGRAPH_START = "狀態只保存"

# The sentences the review fixed (S79R-07, S79R-03, S79R-16); the paragraph is also pinned whole.
P0_SENTENCE = "P0 照常適用：不讀取或回覆 Secret、正式 Log，不讀 target repository 以外或其他 worktree 的檔案。"
NO_PROGRAM_SENTENCE = "不為定位而讀 Workflow 或 Router，不載入整棵樹，不寫受據，不執行閘門腳本、測試或其他程式。"
NOT_FOUND_SENTENCE = (
    "找不到該類索引、索引有歧義、leaf 不存在或索引與 leaf 記載的 revision 不符時，"
    "回答找不到並列出已查的路徑，不掃描、不憑記憶補答、不進入 Wayfinder。"
)
STOP_ON_CHANGE_SENTENCE = "查詢中發現需要改動時，回報後停下；只有使用者要求改動，才走上面的啟動順序。"
NEXT_STEP_SENTENCE = "問下一步、能否派工、整合或核准，屬於推進流程，不是唯讀查詢。"

PARAGRAPH = (
    "唯讀查詢（只問某份文件的內容、某張票的狀態或某條規則的寫法，不要求改動）不走上面的啟動順序；"
    "target project 自己的治理檔另有規定時從其規定。"
    + P0_SENTENCE
    + "使用者指名確切檔案時只讀該檔；否則從該類文件的索引一次解析一條路徑到確切的 leaf。"
    "本插件規則的查詢以本檔「流程索引」為索引，只讀含該規則的那一份（已安裝的插件版本），並註明檔案與版本。"
    + NO_PROGRAM_SENTENCE
    + "票的狀態以目前 checkout 已提交的 leaf 為準，不以索引列、其他 worktree 或未提交的檔案為準；"
    "回答附上 leaf 路徑與 commit；需要受據或佇列才能判定時照實說明，不推斷。"
    + NOT_FOUND_SENTENCE
    + STOP_ON_CHANGE_SENTENCE
    + NEXT_STEP_SENTENCE
)
REQUIRED_SENTENCES: tuple[tuple[str, str], ...] = (
    ("the P0 sentence", P0_SENTENCE),
    ("the sentence that forbids reading Workflow, writing a receipt and running programs", NO_PROGRAM_SENTENCE),
    ("the not-found sentence", NOT_FOUND_SENTENCE),
    ("the stop-on-change sentence", STOP_ON_CHANGE_SENTENCE),
    ("the next-step-is-a-workflow-action sentence", NEXT_STEP_SENTENCE),
)

DESCRIPTION = (
    "Route an action that changes a software project's workflow state (Wayfinder, architecture, requirements, "
    "specification, tickets, implementation, review, handoff, integration, delivery maturity POC/MVP/commercial, "
    "staging) through Johnny's governed workflow. Use when Codex must take over or resume a project, select the "
    "next governed stage, dispatch or review an implementer, minimize Agent context, or apply Johnny workflow "
    "policy without adding a runtime dependency to the target project. Not for a read-only question about an "
    "existing document, ticket or rule; answer it as this plugin's AGENTS.md read-only-lookup paragraph says."
)
DESCRIPTION_LAST_SENTENCE = (
    "Not for a read-only question about an existing document, ticket or rule; answer it as this plugin's "
    "AGENTS.md read-only-lookup paragraph says."
)

START_HEADING = "## Start"
START_STEPS = (
    "1. A read-only question (the content of a document, the state of a ticket, the wording of a rule) is not a "
    "workflow action, unless the target project's own governing files route it otherwise: resolve it as the "
    "[read-only-lookup paragraph](../../AGENTS.md#read-only-lookup) of this plugin's `AGENTS.md` says, answer, "
    "and stop. Do not read `Workflow.md` for it. Asking for the next step, or whether something can be "
    "dispatched, integrated or approved, is a workflow action.\n"
    "2. Read the target project's own `AGENTS.md` and authority record.\n"
    "3. Read `../../Workflow.md` only far enough to identify the current stage and its routing row.\n"
    "4. Read exactly the reference named by that row, plus the minimum committed target artifacts it\n"
    "   requires. Do not load unrelated references, the full library or chat history.\n"
    "5. Execute one legal action, record its typed completion event in the receipt and let the next\n"
    "   gate script read the state files (Revision 04: the Router is the gate scripts over the state\n"
    "   files, not a process to re-enter). Do not select the next stage locally."
)

FRONTMATTER_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ ]+(.*?)[ \t]*$")
STEP_LINE = re.compile(r"^([1-9])\. ")
YAML_INDICATORS = ",[]{}#&*!|>'\"%@`"


class FrontmatterError(ValueError):
    """The frontmatter is not a mapping of one-line plain scalars."""


def plain_scalar_defect(value: str) -> str | None:
    """Name why `value` is not a valid one-line YAML plain scalar, or return None."""
    if value == "":
        return "empty value"
    if value[0] in YAML_INDICATORS:
        return f"starts with the indicator {value[0]!r}"
    if value[0] in "-?:" and (len(value) == 1 or value[1] == " "):
        return f"starts with the indicator {value[0]!r} and a space"
    if ": " in value:
        return "contains a colon and a space"
    if value.endswith(":"):
        return "ends with a colon"
    if " #" in value:
        return "contains a space and a number sign"
    return None


def parse_frontmatter(text: str) -> dict[str, str]:
    """Read the leading `---` block as a mapping of `key: plain scalar` lines; fail closed on anything else."""
    if not text.startswith("---\n"):
        raise FrontmatterError("the file does not start with a frontmatter line")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise FrontmatterError("the frontmatter is not closed")
    result: dict[str, str] = {}
    for line in text[4:end].split("\n"):
        match = FRONTMATTER_LINE.match(line)
        if match is None:
            raise FrontmatterError(f"unsupported frontmatter line {line[:60]!r}")
        key, value = match.group(1), match.group(2)
        if key in result:
            raise FrontmatterError(f"the key {key!r} appears twice")
        defect = plain_scalar_defect(value)
        if defect is not None:
            raise FrontmatterError(f"the value of {key!r} is not a YAML plain scalar: {defect}")
        result[key] = value
    return result


def read_utf8(root: Path, name: str, defects: list[str]) -> str | None:
    """Read a named file as UTF-8 with LF line ends (a Windows checkout may hold CRLF); a missing or
    non-UTF-8 file is a defect that names it."""
    path = root / name
    try:
        raw = path.read_bytes()
    except OSError as error:
        defects.append(f"{name}: cannot be read ({type(error).__name__})")
        return None
    try:
        return raw.decode("utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        defects.append(f"{name}: is not UTF-8")
        return None


def check_agents(text: str, defects: list[str]) -> None:
    lines = text.split("\n")

    if OLD_CONDITION in lines:
        defects.append(f"{AGENTS}: the start order's condition line is still the old one without the carve-out")
    if lines.count(CONDITION) != 1:
        defects.append(f"{AGENTS}: the start order's condition line {CONDITION!r} must appear exactly once")
    if lines.count(ANCHOR) != 1:
        defects.append(f"{AGENTS}: the anchor {ANCHOR} must stand on its own line exactly once")
    if text.count(ANCHOR) != 1:
        defects.append(f"{AGENTS}: the anchor {ANCHOR} must appear exactly once in the file")
    if text.count(PARAGRAPH) != 1:
        defects.append(f"{AGENTS}: the read-only-lookup paragraph must appear exactly once, word for word")
    for label, sentence in REQUIRED_SENTENCES:
        if sentence not in text:
            defects.append(f"{AGENTS}: {label} is missing")

    if lines.count(START_ORDER_HEADING) != 1:
        defects.append(f"{AGENTS}: the heading {START_ORDER_HEADING!r} must appear exactly once")
        return
    heading = lines.index(START_ORDER_HEADING)
    if lines[heading + 1 : heading + 3] != ["", CONDITION]:
        defects.append(f"{AGENTS}: the condition line must follow the heading {START_ORDER_HEADING!r} and a blank line")
        return
    if lines[heading + 3] != "":
        defects.append(f"{AGENTS}: a blank line must follow the condition line")
        return

    # The five steps: each starts at its number; the block ends at the first blank line.
    cursor = heading + 4
    last_step = 0
    step_5_line = -1
    while cursor < len(lines) and lines[cursor] != "":
        match = STEP_LINE.match(lines[cursor])
        if match is not None:
            last_step = int(match.group(1))
            if last_step == 5:
                step_5_line = cursor
        cursor += 1
    if last_step != 5 or step_5_line == -1:
        defects.append(f"{AGENTS}: the start order must keep its five steps")
        return

    expected_after_steps = ["", ANCHOR, "", PARAGRAPH, ""]
    if lines[cursor : cursor + 5] != expected_after_steps:
        defects.append(
            f"{AGENTS}: after step 5 must come a blank line, the anchor, a blank line, the paragraph and a "
            "blank line, in that order"
        )
        return
    if not lines[cursor + 5].startswith(STATE_PARAGRAPH_START):
        defects.append(f"{AGENTS}: the paragraph that begins {STATE_PARAGRAPH_START!r} must follow the lookup paragraph")


def section_body(text: str, heading: str) -> str | None:
    """The text after `heading` and one blank line, up to the next blank-line-separated non-list paragraph."""
    marker = f"\n{heading}\n\n"
    start = text.find(marker)
    if start == -1 or text.count(marker) != 1:
        return None
    body = text[start + len(marker) :]
    end = body.find("\n\n")
    return body if end == -1 else body[:end]


def check_skill(text: str, defects: list[str]) -> None:
    try:
        meta = parse_frontmatter(text)
    except FrontmatterError as error:
        defects.append(f"{SKILL}: frontmatter does not parse: {error}")
    else:
        description = meta.get("description", "")
        if description == "":
            defects.append(f"{SKILL}: the frontmatter description is missing or empty")
        elif description != DESCRIPTION:
            defects.append(f"{SKILL}: the frontmatter description is not the ticket's text")
        if not description.endswith(DESCRIPTION_LAST_SENTENCE):
            defects.append(f"{SKILL}: the description's last sentence (the read-only exclusion) is missing")

    steps = section_body(text, START_HEADING)
    if steps is None:
        defects.append(f"{SKILL}: the section {START_HEADING!r} must appear exactly once")
    elif steps != START_STEPS:
        defects.append(
            f"{SKILL}: {START_HEADING!r} must be the new first step followed by the four original steps "
            "renumbered 2 to 5, in order, word for word"
        )


def find_defects(root: Path) -> list[str]:
    defects: list[str] = []
    agents = read_utf8(root, AGENTS, defects)
    if agents is not None:
        check_agents(agents, defects)
    skill = read_utf8(root, SKILL, defects)
    if skill is not None:
        check_skill(skill, defects)
    return defects


def remove_text(sentence: str) -> Callable[[str], str]:
    """An edit that deletes `sentence` from a text."""

    def edit(text: str) -> str:
        return text.replace(sentence, "")

    return edit


def copy_texts(root: Path) -> None:
    for name in (AGENTS, SKILL):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / name).read_bytes().decode("utf-8").replace("\r\n", "\n").encode("utf-8"))


def damage(root: Path, name: str, edit: Callable[[str], str]) -> None:
    """Rewrite one copied file through `edit`, and require that the edit changed it."""
    path = root / name
    before = path.read_bytes().decode("utf-8")
    after = edit(before)
    if after == before:
        raise AssertionError(f"the injection did not change {name}")
    path.write_bytes(after.encode("utf-8"))


class FrontmatterReaderTests(unittest.TestCase):
    def test_a_plain_scalar_with_a_colon_and_a_space_is_rejected(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("---\nname: x\ndescription: a rule: answer it\n---\n\nbody\n")

    def test_the_other_plain_scalar_breaks_are_rejected(self) -> None:
        for value in ("", "- item", "? key", ": x", "@at", "`tick", "a #comment", "ends with:", "'quoted'"):
            with self.subTest(value=value):
                self.assertIsNotNone(plain_scalar_defect(value))

    def test_a_valid_frontmatter_is_read(self) -> None:
        meta = parse_frontmatter("---\nname: x\ndescription: a rule; answer it, (really) a/b's\n---\n\nbody\n")
        self.assertEqual(meta, {"name": "x", "description": "a rule; answer it, (really) a/b's"})

    def test_an_unknown_line_shape_fails_closed(self) -> None:
        for text in (
            "no frontmatter\n",
            "---\nname: x\n",
            "---\nname: x\n  continued\n---\n",
            "---\nname: x\nname: y\n---\n",
            "---\n- a\n---\n",
        ):
            with self.subTest(text=text), self.assertRaises(FrontmatterError):
                parse_frontmatter(text)


class EntryReadOnlyLookupTests(unittest.TestCase):
    def test_the_committed_texts_carry_the_rule(self) -> None:
        self.assertEqual(find_defects(REPO), [])

    def test_the_skill_frontmatter_parses_and_names_the_skill(self) -> None:
        meta = parse_frontmatter((REPO / SKILL).read_bytes().decode("utf-8").replace("\r\n", "\n"))
        self.assertEqual(meta["name"], "johnny-project-takeover")
        self.assertEqual(meta["description"], DESCRIPTION)

    def assert_red(self, name: str, edit: Callable[[str], str], expected: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_texts(root)
            self.assertEqual(find_defects(root), [], "the unmodified copy must stay green")
            damage(root, name, edit)
            defects = find_defects(root)
            self.assertTrue(defects, "the damaged copy must be red")
            self.assertTrue(
                any(expected in defect for defect in defects),
                f"no defect names {expected!r}: {defects}",
            )

    def test_the_condition_line_without_its_carve_out_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace(CONDITION, OLD_CONDITION), "condition line")

    def test_the_paragraph_removed_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace(PARAGRAPH + "\n\n", ""), "paragraph")

    def test_each_named_sentence_removed_from_the_paragraph_is_red(self) -> None:
        for label, sentence in REQUIRED_SENTENCES:
            with self.subTest(sentence=label):
                self.assert_red(AGENTS, remove_text(sentence), label)

    def test_the_anchor_moved_below_the_paragraph_is_red(self) -> None:
        def move(text: str) -> str:
            without = text.replace(ANCHOR + "\n\n", "")
            return without.replace(PARAGRAPH + "\n\n", PARAGRAPH + "\n\n" + ANCHOR + "\n\n")

        self.assert_red(AGENTS, move, "after step 5")

    def test_the_anchor_without_its_blank_lines_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace(ANCHOR + "\n\n", ANCHOR + "\n"), "after step 5")

    def test_the_paragraph_after_the_state_paragraph_is_red(self) -> None:
        def move(text: str) -> str:
            block = ANCHOR + "\n\n" + PARAGRAPH + "\n\n"
            without = text.replace(block, "")
            return without.replace("## Router 返回規則\n\n", "## Router 返回規則\n\n" + block)

        self.assert_red(AGENTS, move, "after step 5")

    def test_the_description_without_its_last_sentence_is_red(self) -> None:
        self.assert_red(SKILL, lambda t: t.replace(" " + DESCRIPTION_LAST_SENTENCE, ""), "description")

    def test_the_description_with_a_colon_and_a_space_is_red(self) -> None:
        self.assert_red(
            SKILL,
            lambda t: t.replace("ticket or rule; answer it", "ticket or rule: answer it"),
            "frontmatter does not parse",
        )

    def test_an_empty_description_is_red(self) -> None:
        self.assert_red(SKILL, lambda t: t.replace(DESCRIPTION, ""), "description")

    def test_the_new_start_step_moved_after_the_original_first_step_is_red(self) -> None:
        first = START_STEPS.split("\n")[0]
        second = START_STEPS.split("\n")[1]
        self.assert_red(SKILL, lambda t: t.replace(first + "\n" + second, second + "\n" + first), "Start")

    def test_the_start_steps_not_renumbered_are_red(self) -> None:
        self.assert_red(
            SKILL,
            lambda t: t.replace("2. Read the target project's own", "1. Read the target project's own"),
            "Start",
        )

    def test_a_missing_file_is_red_and_named(self) -> None:
        for name in (AGENTS, SKILL):
            with self.subTest(file=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                copy_texts(root)
                (root / name).unlink()
                defects = find_defects(root)
                self.assertTrue(any(defect.startswith(f"{name}: cannot be read") for defect in defects), defects)

    def test_a_non_utf8_file_is_red_and_named(self) -> None:
        for name in (AGENTS, SKILL):
            with self.subTest(file=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                copy_texts(root)
                (root / name).write_bytes(b"\xff\xfe\x00\xff")
                defects = find_defects(root)
                self.assertTrue(any(defect.startswith(f"{name}: is not UTF-8") for defect in defects), defects)


if __name__ == "__main__":
    unittest.main()
