"""Ticket 82: the plugin ships a SessionStart hook that tells every session where its rules are and that a
read-only lookup starts at the 流程索引.

The hook is one file, `hooks/hooks.json`, whose command only prints text. This module pins:

- the file, parsed and byte for byte (the command is ASCII only, there is no matcher, one command);
- the two anchors the command names, each exactly once in `AGENTS.md` (`read-only-lookup`, and `process-index`
  directly above `## 流程索引`);
- the payload declaration, which lists `hooks/hooks.json` and carries no `hooks` tree, and the publication tree
  step, which writes the same bytes;
- the README sentence, the last paragraph of section `## 8. 它怎麼運作`;
- the old-plugin guard of the command: its two match conditions stand once in the command and once in the line
  of `SKILL.md` that begins `1. Before anything else`;
- the command itself, run in each shell it must work in, with `${CLAUDE_PLUGIN_ROOT}` replaced by a temporary
  directory.

The file checks are one function over a root directory (`hook_defects`), so each injection case below runs it on a
temporary copy of the five files with one text damaged and must go red; the unmodified copy must stay green. A
missing or unparsable file is a named defect and never a traceback. The pinned commit is not checked here: K1 does it.

Shells: on Windows the bash case runs the file named by `CLAUDE_CODE_GIT_BASH_PATH`, or
`C:\\Program Files\\Git\\bin\\bash.exe`, and never a bare `bash` (it resolves to the WSL launcher). The PowerShell case
runs on Windows only.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path

from library.local_orchestration.plugin_publication import (
    load_payload_declaration,
    materialise_publication_tree,
)

REPO = Path(__file__).resolve().parents[1]

HOOKS = "hooks/hooks.json"
AGENTS = "AGENTS.md"
README = "README.md"
MANIFEST = ".claude-plugin/plugin.json"
SKILL = "skills/johnny-project-takeover/SKILL.md"

PLACEHOLDER = "${CLAUDE_PLUGIN_ROOT}"
COMMAND = (
    'echo "Software Factory plugin: its rules are in ${CLAUDE_PLUGIN_ROOT}/AGENTS.md. '
    "To answer a read-only question about one of those rules, read that file: "
    "its paragraph at the anchor read-only-lookup says how, and its table at the anchor process-index "
    "gives the one row and the one section to read. "
    "Do not locate a rule with grep, a full-text search or by browsing files. "
    "If this session also lists a skill whose name begins with johnny-ai-skill: "
    "or whose file lies in a folder named johnny-ai-skill, "
    "then before anything else tell the user that the old 0.4.x plugin is still installed "
    "and conflicts with this version, give the removal commands in section 5 of "
    '${CLAUDE_PLUGIN_ROOT}/README.md, ask the user to open a new session after removing it, '
    'and do nothing else in this session."'
)
EXPECTED_HOOKS: dict[str, object] = {
    "hooks": {
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": COMMAND,
                    }
                ]
            }
        ]
    }
}
EXPECTED_TEXT = (
    "Software Factory plugin: its rules are in {root}/AGENTS.md. "
    "To answer a read-only question about one of those rules, read that file: "
    "its paragraph at the anchor read-only-lookup says how, and its table at the anchor process-index "
    "gives the one row and the one section to read. "
    "Do not locate a rule with grep, a full-text search or by browsing files. "
    "If this session also lists a skill whose name begins with johnny-ai-skill: "
    "or whose file lies in a folder named johnny-ai-skill, "
    "then before anything else tell the user that the old 0.4.x plugin is still installed "
    "and conflicts with this version, give the removal commands in section 5 of "
    "{root}/README.md, ask the user to open a new session after removing it, "
    "and do nothing else in this session."
)

LOOKUP_ANCHOR_NAME = "read-only-lookup"
INDEX_ANCHOR_NAME = "process-index"
INDEX_HEADING = "## 流程索引"

README_HEADING = "## 8. 它怎麼運作"
README_SENTENCE = (
    "每次開新的 session，插件會用一個 SessionStart hook 告訴 agent 規則檔在哪裡、"
    "查本插件規則的唯讀查詢要先查流程索引，以及舊版 johnny-ai-skill 還裝著時要先停下來；"
    "在 Claude Code 終端機裡輸入 /hooks 可以看到它。"
)

# The two match conditions of the old-plugin guard: the command and `SKILL.md` step 1 carry them word for word.
GUARD_CONDITIONS = (
    "name begins with johnny-ai-skill:",
    "file lies in a folder named johnny-ai-skill",
)
SKILL_STEP_START = "1. Before anything else"

# Revision05 to revision07, items 4b and 4c: one paragraph in README section 4 and one in section 5, each at a
# fixed place (the three lines before it and the two lines after it are pinned), without code, path or link.
README_SECTION_4 = "## 4. 安裝：Codex"
README_SECTION_5 = "## 5. 從舊版 johnny-ai-skill 換過來"
CODEX_TRUST_PARAGRAPH = (
    "安裝或更新 Software Factory 之後，請先在終端機裡進到你平常用 Codex 的專案資料夾，執行一次 codex；"
    "它詢問是否信任 Software Factory 的 hook 時請選信任，然後離開，之後就可以照常使用 Codex 桌面 app。"
    "目前的 Codex 桌面 app 不會詢問：hook 有變動而還沒在終端機裡重新信任時，這個 hook 不會生效，"
    "Codex 開場時不會知道插件的規則檔在哪裡，查規則時可能改用搜尋，也不會在舊版還裝著時先停下來。"
)
SCOPE_PARAGRAPH = (
    "上面的 uninstall 指令針對裝在 user 範圍的舊版（0.4.x 的 README 就是這樣教的）。"
    "如果當初裝在 project 或 local 範圍，請到那個專案的資料夾裡執行上面兩個指令，"
    "並把 uninstall 的 --scope user 換成 --scope project 或 --scope local。"
)
FORBIDDEN_IN_PARAGRAPH = ("`", "](", "/", "\\")

FILES = (HOOKS, AGENTS, README, MANIFEST, SKILL)


def expected_file_text() -> str:
    """The bytes of `hooks/hooks.json` as text: two-space indent, LF line ends, one final line feed."""
    return json.dumps(EXPECTED_HOOKS, indent=2, ensure_ascii=False) + "\n"


def read_text(root: Path, name: str, defects: list[str]) -> str | None:
    """Read a named file as UTF-8 with LF line ends (a Windows checkout may hold CRLF); a missing or
    non-UTF-8 file is a defect that names it."""
    try:
        raw = (root / name).read_bytes()
    except OSError as error:
        defects.append(f"{name}: cannot be read ({type(error).__name__})")
        return None
    try:
        return raw.decode("utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        defects.append(f"{name}: is not UTF-8")
        return None


def check_hook_file(root: Path, defects: list[str]) -> None:
    text = read_text(root, HOOKS, defects)
    if text is None:
        return
    try:
        parsed: object = json.loads(text)
    except ValueError:
        defects.append(f"{HOOKS}: is not valid JSON")
        return
    if parsed != EXPECTED_HOOKS:
        defects.append(f"{HOOKS}: does not equal the hook of ticket 82 item 1")
    elif text != expected_file_text():
        defects.append(f"{HOOKS}: does not hold the bytes of ticket 82 item 1")
    command = _first_command(parsed)
    if command is not None and not command.isascii():
        defects.append(f"{HOOKS}: the command must hold only ASCII")


def _first_command(parsed: object) -> str | None:
    """The command string of the first hook, or None when the shape is not the expected one."""
    if not isinstance(parsed, dict):
        return None
    hooks = parsed.get("hooks")
    if not isinstance(hooks, dict):
        return None
    groups = hooks.get("SessionStart")
    if not isinstance(groups, list) or not groups or not isinstance(groups[0], dict):
        return None
    inner = groups[0].get("hooks")
    if not isinstance(inner, list) or not inner or not isinstance(inner[0], dict):
        return None
    command = inner[0].get("command")
    return command if isinstance(command, str) else None


def check_guard(root: Path, defects: list[str]) -> None:
    """Each match condition of the old-plugin guard stands exactly once in the command and exactly once in the
    line of `SKILL.md` that begins `1. Before anything else`."""
    hook_text = read_text(root, HOOKS, [])
    command: str | None = None
    if hook_text is not None:
        try:
            command = _first_command(json.loads(hook_text))
        except ValueError:
            command = None
    if command is None:
        defects.append(f"{HOOKS}: holds no command to compare with the guard of {SKILL}")
    skill_text = read_text(root, SKILL, defects)
    if skill_text is None:
        return
    steps = [line for line in skill_text.split("\n") if line.startswith(SKILL_STEP_START)]
    if len(steps) != 1:
        defects.append(f"{SKILL}: exactly one line must begin {SKILL_STEP_START!r}")
        return
    for condition in GUARD_CONDITIONS:
        if steps[0].count(condition) != 1:
            defects.append(f"{SKILL}: step 1 must hold {condition!r} exactly once")
        if command is not None and command.count(condition) != 1:
            defects.append(f"{HOOKS}: the command must hold {condition!r} exactly once")


def check_anchors(root: Path, defects: list[str]) -> None:
    text = read_text(root, AGENTS, defects)
    if text is None:
        return
    lines = text.split("\n")
    lookup = f'<a id="{LOOKUP_ANCHOR_NAME}"></a>'
    if lines.count(lookup) != 1:
        defects.append(f"{AGENTS}: the anchor {lookup} must stand on its own line exactly once")
    index = f'<a id="{INDEX_ANCHOR_NAME}"></a>'
    if lines.count(index) != 1:
        defects.append(f"{AGENTS}: the anchor {index} must stand on its own line exactly once")
        return
    at = lines.index(index)
    if at == 0 or lines[at - 1] != "" or lines[at + 1 : at + 3] != ["", INDEX_HEADING]:
        defects.append(
            f"{AGENTS}: the anchor {index} must have a blank line before it and after it, "
            f"and stand directly above {INDEX_HEADING!r}"
        )


def check_payload(root: Path, defects: list[str]) -> None:
    text = read_text(root, MANIFEST, defects)
    if text is None:
        return
    try:
        manifest: object = json.loads(text)
    except ValueError:
        defects.append(f"{MANIFEST}: is not valid JSON")
        return
    payload = manifest.get("payload") if isinstance(manifest, dict) else None
    files = payload.get("files") if isinstance(payload, dict) else None
    trees = payload.get("trees") if isinstance(payload, dict) else None
    if not isinstance(files, list) or not isinstance(trees, list):
        defects.append(f"{MANIFEST}: payload.files and payload.trees must both be lists")
        return
    if HOOKS not in files:
        defects.append(f"{MANIFEST}: payload.files must list {HOOKS}")
    if "hooks" in trees:
        defects.append(f"{MANIFEST}: payload.trees must not carry the hooks tree")


def check_readme(root: Path, defects: list[str]) -> None:
    text = read_text(root, README, defects)
    if text is None:
        return
    if text.count(README_SENTENCE) != 1:
        defects.append(f"{README}: the sentence of ticket 82 item 4 must appear exactly once")
        return
    lines = text.split("\n")
    if lines.count(README_HEADING) != 1:
        defects.append(f"{README}: the heading {README_HEADING!r} must appear exactly once")
        return
    start = lines.index(README_HEADING) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    paragraphs = [block for block in "\n".join(lines[start:end]).split("\n\n") if block.strip()]
    if not paragraphs or paragraphs[-1].strip() != README_SENTENCE:
        defects.append(f"{README}: the sentence must be its own paragraph and the last one of {README_HEADING!r}")


def _section(lines: list[str], heading: str) -> tuple[int, int] | None:
    """The line range (start, end) of the section under `heading`, up to the next `## ` heading."""
    if lines.count(heading) != 1:
        return None
    start = lines.index(heading) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def _check_placed_paragraph(
    lines: list[str],
    heading: str,
    paragraph: str,
    before: tuple[str, str, str],
    after_start: str,
    defects: list[str],
) -> None:
    """The paragraph stands exactly once in the section, directly after `before` (a command line, a closing fence
    and a blank line) and directly before a blank line and a line that begins `after_start`."""
    found = _section(lines, heading)
    if found is None:
        defects.append(f"{README}: the heading {heading!r} must appear exactly once")
        return
    start, end = found
    if any(ch in paragraph for ch in FORBIDDEN_IN_PARAGRAPH):
        defects.append(f"{README}: the paragraph of {heading!r} must hold no code, path or link character")
    at = [i for i in range(start, end) if lines[i] == paragraph]
    if len(at) != 1 or lines.count(paragraph) != 1:
        defects.append(f"{README}: section {heading!r} must hold its paragraph exactly once")
        return
    i = at[0]
    if tuple(lines[i - 3 : i]) != before:
        defects.append(f"{README}: the three lines before the paragraph of {heading!r} are not {before!r}")
    if len(lines) < i + 3 or lines[i + 1] != "" or not lines[i + 2].startswith(after_start):
        defects.append(f"{README}: the paragraph of {heading!r} must be followed by a blank line and {after_start!r}")


def check_readme_paragraphs(root: Path, defects: list[str]) -> None:
    text = read_text(root, README, defects)
    if text is None:
        return
    lines = text.split("\n")
    _check_placed_paragraph(
        lines,
        README_SECTION_4,
        CODEX_TRUST_PARAGRAPH,
        ("codex plugin list --marketplace software-factory --json", "```", ""),
        "5. 要移除時",
        defects,
    )
    _check_placed_paragraph(
        lines,
        README_SECTION_5,
        SCOPE_PARAGRAPH,
        ("claude plugin marketplace remove johnny-ai-skill", "```", ""),
        "Codex：",
        defects,
    )


def hook_defects(root: Path) -> list[str]:
    """Every defect of the hook, its two anchors, the payload declaration and the README texts under `root`."""
    defects: list[str] = []
    check_hook_file(root, defects)
    check_guard(root, defects)
    check_anchors(root, defects)
    check_payload(root, defects)
    check_readme(root, defects)
    check_readme_paragraphs(root, defects)
    return defects


def copy_files(destination: Path) -> None:
    for name in FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / name, target)


def bash_command_line(command: str) -> list[str] | None:
    """The argument list that runs `command` in bash, or None when no bash is available. On Windows it is
    the Git Bash file, never a bare `bash` (that resolves to the WSL launcher)."""
    if sys.platform == "win32":
        configured = os.environ.get("CLAUDE_CODE_GIT_BASH_PATH")
        path = configured if configured else r"C:\Program Files\Git\bin\bash.exe"
        return [path, "-c", command] if Path(path).is_file() else None
    found = shutil.which("bash")
    return [found, "-c", command] if found is not None else None


def powershell_command_line(command: str) -> list[str] | None:
    found = shutil.which("powershell")
    if found is None:
        return None
    return [found, "-NoProfile", "-NonInteractive", "-Command", command]


class RepositoryHookTests(unittest.TestCase):
    """The committed files pass every check."""

    def test_the_committed_hook_has_no_defect(self) -> None:
        self.assertEqual(hook_defects(REPO), [])

    def test_the_hook_file_parses_and_equals_item_1(self) -> None:
        parsed: object = json.loads((REPO / HOOKS).read_text(encoding="utf-8"))
        self.assertEqual(parsed, EXPECTED_HOOKS)

    def test_the_command_holds_only_ascii(self) -> None:
        command = _first_command(json.loads((REPO / HOOKS).read_text(encoding="utf-8")))
        self.assertIsNotNone(command)
        assert command is not None
        self.assertTrue(command.isascii())

    def test_the_guard_conditions_match_the_skill_step_word_for_word(self) -> None:
        defects: list[str] = []
        check_guard(REPO, defects)
        self.assertEqual(defects, [])
        step = [
            line
            for line in (REPO / SKILL).read_text(encoding="utf-8").splitlines()
            if line.startswith(SKILL_STEP_START)
        ]
        self.assertEqual(len(step), 1)
        command = _first_command(json.loads((REPO / HOOKS).read_text(encoding="utf-8")))
        assert command is not None
        for condition in GUARD_CONDITIONS:
            with self.subTest(condition=condition):
                self.assertEqual(command.count(condition), 1)
                self.assertEqual(step[0].count(condition), 1)

    def test_each_anchor_it_names_stands_once_in_the_rules_file(self) -> None:
        defects: list[str] = []
        check_anchors(REPO, defects)
        self.assertEqual(defects, [])

    def test_the_payload_declares_the_hook_and_no_hooks_tree(self) -> None:
        defects: list[str] = []
        check_payload(REPO, defects)
        self.assertEqual(defects, [])

    def test_the_publication_tree_writes_the_same_bytes(self) -> None:
        payload = load_payload_declaration(REPO / MANIFEST)
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw) / "tree"
            destination.mkdir()
            materialise_publication_tree(REPO, payload, destination)
            written = destination / HOOKS
            self.assertTrue(written.is_file(), f"{HOOKS} is not in the publication tree")
            self.assertEqual(written.read_bytes(), (REPO / HOOKS).read_bytes())

    def test_the_codex_trust_and_scope_paragraphs_stand_at_their_places(self) -> None:
        defects: list[str] = []
        check_readme_paragraphs(REPO, defects)
        self.assertEqual(defects, [])

    def test_neither_new_paragraph_holds_code_a_path_or_a_link(self) -> None:
        for paragraph in (CODEX_TRUST_PARAGRAPH, SCOPE_PARAGRAPH):
            for character in FORBIDDEN_IN_PARAGRAPH:
                with self.subTest(paragraph=paragraph[:12], character=character):
                    self.assertNotIn(character, paragraph)

    def test_the_readme_sentence_is_the_last_paragraph_of_section_8(self) -> None:
        defects: list[str] = []
        check_readme(REPO, defects)
        self.assertEqual(defects, [])


class RunTheCommandTests(unittest.TestCase):
    """The command prints the expected text with the substituted path, in each shell it must work in."""

    def run_in(self, build: Callable[[str], list[str] | None], native: bool) -> None:
        command = _first_command(json.loads((REPO / HOOKS).read_text(encoding="utf-8")))
        self.assertIsNotNone(command)
        assert command is not None
        with tempfile.TemporaryDirectory() as raw:
            root = str(Path(raw)) if native else Path(raw).as_posix()
            substituted = command.replace(PLACEHOLDER, root)
            line = build(substituted)
            if line is None:
                self.skipTest("shell not found")
            result = subprocess.run(line, capture_output=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
            self.assertEqual(result.stderr, b"")
            printed = result.stdout.decode("utf-8").replace("\r\n", "\n")
            self.assertEqual(printed, EXPECTED_TEXT.format(root=root) + "\n")

    def test_bash_prints_the_text_with_the_forward_slash_path(self) -> None:
        if bash_command_line("echo") is None:
            self.skipTest("Git Bash not found")
        self.run_in(bash_command_line, native=False)

    @unittest.skipUnless(sys.platform == "win32", "PowerShell runs on Windows only")
    def test_powershell_prints_the_text_with_the_native_path(self) -> None:
        if powershell_command_line("echo") is None:
            self.skipTest("Windows PowerShell not found")
        self.run_in(powershell_command_line, native=True)


class InjectionTests(unittest.TestCase):
    """Each damage to one text of a temporary copy turns `hook_defects` red, naming the text."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)
        copy_files(self.root)

    def damaged(self, name: str, damage: Callable[[str], str]) -> list[str]:
        path = self.root / name
        original = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
        changed = damage(original)
        self.assertNotEqual(changed, original, "the damage changed nothing")
        path.write_bytes(changed.encode("utf-8"))
        return hook_defects(self.root)

    def assert_red(self, name: str, damage: Callable[[str], str], expected: str) -> None:
        defects = self.damaged(name, damage)
        self.assertTrue(any(expected in defect for defect in defects), f"{expected!r} not named in {defects}")

    def test_the_unmodified_copy_is_green(self) -> None:
        self.assertEqual(hook_defects(self.root), [])

    def test_a_missing_hook_file_is_a_named_defect(self) -> None:
        (self.root / HOOKS).unlink()
        self.assertTrue(any(HOOKS in d and "cannot be read" in d for d in hook_defects(self.root)))

    def test_an_unparsable_hook_file_is_a_named_defect(self) -> None:
        self.assert_red(HOOKS, lambda t: t[: len(t) // 2], "is not valid JSON")

    def test_a_missing_rules_file_is_a_named_defect(self) -> None:
        (self.root / AGENTS).unlink()
        self.assertTrue(any(AGENTS in d and "cannot be read" in d for d in hook_defects(self.root)))

    def test_an_empty_session_start_list_is_red(self) -> None:
        self.assert_red(
            HOOKS,
            lambda t: json.dumps({"hooks": {"SessionStart": []}}, indent=2) + "\n",
            "does not equal the hook",
        )

    def test_an_empty_command_is_red(self) -> None:
        self.assert_red(HOOKS, lambda t: t.replace(COMMAND.replace('"', '\\"'), ""), "does not equal the hook")

    def test_a_non_ascii_character_in_the_command_is_red(self) -> None:
        self.assert_red(HOOKS, lambda t: t.replace("Software Factory", "Software Factor\u00fd"), "only ASCII")

    def test_a_matcher_added_is_red(self) -> None:
        self.assert_red(HOOKS, lambda t: t.replace('      {\n        "hooks"', '      {\n        "matcher": "startup",\n        "hooks"'), "does not equal the hook")

    def test_the_old_plugin_sentence_removed_from_the_command_is_red(self) -> None:
        sentence = (
            " If this session also lists a skill whose name begins with johnny-ai-skill: or whose file lies in a "
            "folder named johnny-ai-skill, then before anything else tell the user that the old 0.4.x plugin is "
            "still installed and conflicts with this version, give the removal commands in section 5 of "
            "${CLAUDE_PLUGIN_ROOT}/README.md, ask the user to open a new session after removing it, and do "
            "nothing else in this session."
        )
        defects = self.damaged(HOOKS, lambda t: t.replace(sentence, ""))
        self.assertTrue(any("does not equal the hook" in d for d in defects), defects)
        self.assertTrue(any("must hold 'name begins with johnny-ai-skill:' exactly once" in d for d in defects), defects)

    def test_a_guard_condition_changed_in_the_command_is_red(self) -> None:
        self.assert_red(
            HOOKS,
            lambda t: t.replace("name begins with johnny-ai-skill:", "name begins with johnny-ai-skill-"),
            "the command must hold 'name begins with johnny-ai-skill:' exactly once",
        )

    def test_the_second_guard_condition_changed_in_the_command_is_red(self) -> None:
        self.assert_red(
            HOOKS,
            lambda t: t.replace("file lies in a folder named johnny-ai-skill", "file lies in a folder named johnny-ai"),
            "the command must hold 'file lies in a folder named johnny-ai-skill' exactly once",
        )

    def test_a_guard_condition_changed_in_the_skill_step_is_red(self) -> None:
        self.assert_red(
            SKILL,
            lambda t: t.replace("its name begins with johnny-ai-skill:", "its name starts with johnny-ai-skill:"),
            "step 1 must hold 'name begins with johnny-ai-skill:' exactly once",
        )

    def test_a_missing_skill_file_is_a_named_defect(self) -> None:
        (self.root / SKILL).unlink()
        self.assertTrue(any(SKILL in d and "cannot be read" in d for d in hook_defects(self.root)))

    def test_the_command_text_changed_by_one_word_is_red(self) -> None:
        self.assert_red(HOOKS, lambda t: t.replace("Do not locate", "Do not find"), "does not equal the hook")

    def test_the_hook_removed_from_the_payload_is_red(self) -> None:
        self.assert_red(MANIFEST, lambda t: t.replace('      "hooks/hooks.json",\n', ""), f"payload.files must list {HOOKS}")

    def test_a_hooks_tree_in_the_payload_is_red(self) -> None:
        self.assert_red(MANIFEST, lambda t: t.replace('      ".claude-plugin",\n', '      ".claude-plugin",\n      "hooks",\n'), "must not carry the hooks tree")

    def test_the_process_index_anchor_removed_is_red(self) -> None:
        anchor = f'<a id="{INDEX_ANCHOR_NAME}"></a>'
        self.assert_red(AGENTS, lambda t: t.replace(anchor + "\n\n", ""), f"the anchor {anchor}")

    def test_a_prefix_anchor_does_not_satisfy_the_name(self) -> None:
        anchor = f'<a id="{INDEX_ANCHOR_NAME}"></a>'
        self.assert_red(AGENTS, lambda t: t.replace(anchor, f'<a id="{INDEX_ANCHOR_NAME}-x"></a>'), f"the anchor {anchor}")

    def test_the_process_index_anchor_below_the_heading_is_red(self) -> None:
        anchor = f'<a id="{INDEX_ANCHOR_NAME}"></a>'
        self.assert_red(
            AGENTS,
            lambda t: t.replace(anchor + "\n\n" + INDEX_HEADING + "\n", INDEX_HEADING + "\n\n" + anchor + "\n"),
            "directly above",
        )

    def test_the_lookup_anchor_removed_is_red(self) -> None:
        anchor = f'<a id="{LOOKUP_ANCHOR_NAME}"></a>'
        self.assert_red(AGENTS, lambda t: t.replace(anchor + "\n\n", ""), f"the anchor {anchor}")

    def test_the_codex_trust_paragraph_removed_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace(CODEX_TRUST_PARAGRAPH + "\n\n", ""), "must hold its paragraph exactly once")

    def test_the_scope_paragraph_removed_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace(SCOPE_PARAGRAPH + "\n\n", ""), "must hold its paragraph exactly once")

    def test_the_codex_trust_paragraph_moved_is_red(self) -> None:
        self.assert_red(
            README,
            lambda t: t.replace(CODEX_TRUST_PARAGRAPH + "\n\n5. 要移除時", "5. 要移除時").replace(
                "\n\n## 5. 從舊版", "\n\n" + CODEX_TRUST_PARAGRAPH + "\n\n## 5. 從舊版"
            ),
            "the three lines before the paragraph",
        )

    def test_the_scope_paragraph_with_a_path_character_is_red(self) -> None:
        self.assert_red(
            README,
            lambda t: t.replace("project 或 local 範圍", "project/local 範圍"),
            "must hold its paragraph exactly once",
        )

    def test_the_readme_sentence_removed_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace(README_SENTENCE + "\n\n", ""), "must appear exactly once")

    def test_the_readme_sentence_twice_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace(README_SENTENCE + "\n", README_SENTENCE + "\n\n" + README_SENTENCE + "\n"), "must appear exactly once")

    def test_the_readme_sentence_inside_another_paragraph_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace("\n\n" + README_SENTENCE, "\n" + README_SENTENCE), "its own paragraph")

    def test_the_readme_sentence_not_last_in_the_section_is_red(self) -> None:
        self.assert_red(README, lambda t: t.replace(README_SENTENCE + "\n\n", README_SENTENCE + "\n\n- 之後又加的一段。\n\n"), "the last one")


if __name__ == "__main__":
    unittest.main()
