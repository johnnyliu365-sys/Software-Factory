"""Ticket 79 and ticket 80: a read-only question goes from its index straight to its leaf, never by search; only a
change takes the start order.

Ticket 80 adds to `AGENTS.md` three anchors (`startup-order`, `p0-permissions`, `target-sources`), five rows at the
top of the 流程索引 table (directly below its separator line, above the row that begins "| 任一事件") and the two
sentences of the lookup paragraph that say how a rule is located. Every link in the five rows must resolve: a `#name`
to exactly one line `<a id="name"></a>` of `AGENTS.md`, a path to a file under the root. A missing `AGENTS.md`, or a
table without its separator line, is a named defect and never a traceback.

Four texts carry the rule, and this test pins each one exactly:

- `AGENTS.md`, the start order's condition line, with its read-only carve-out;
- `AGENTS.md`, the `read-only-lookup` anchor (on its own line, blank lines around it) and the paragraph,
  between step 5 of the start order and the paragraph that begins "狀態只保存";
- `skills/johnny-project-takeover/SKILL.md`, the frontmatter `description`, which must also be a valid YAML
  plain scalar (a colon and space inside it makes the skill fail to register);
- `skills/johnny-project-takeover/SKILL.md`, section `## Start`: the guard step, then the read-only step, then
  the four original steps renumbered 3 to 6, in order.

Ticket 81 changes the first 流程索引 row and the tie-break clause of the lookup paragraph, and adds the guard
step. The 流程索引 table is also pinned whole (`INDEX_TABLE`), and each link to an anchor of `AGENTS.md` itself
must appear in exactly one row.

The check is a function over a root directory (`find_defects`), so each injection case below runs it on a
temporary copy of the files with one text damaged, and must go red; the unmodified copy must stay green.
`copy_texts` copies six files: `AGENTS.md`, `SKILL.md` and the four references the rows name.
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

# Ticket 80 item 1: three anchors, each on its own line with a blank line before and after, directly above its heading.
ANCHORED_HEADINGS: tuple[tuple[str, str], ...] = (
    ("startup-order", "## 啟動順序"),
    ("p0-permissions", "## P0：權限與所有權"),
    ("target-sources", "## Target project 正式來源"),
)

# Ticket 80 item 2: the five rows, in this order, directly below the separator of the 流程索引 table.
INDEX_HEADING = "## 流程索引"
INDEX_HEADER = "| 情境 | Workflow 入口 | Router 指向的詳細 reference |"
INDEX_SEPARATOR = "| --- | --- | --- |"
ROW_AFTER_THE_FIVE_START = "| 任一事件"
INDEX_ROWS: tuple[str, ...] = (
    "| 唯讀查詢本身的規則（怎麼查、查不到時怎麼回答） | [唯讀查詢](#read-only-lookup) | 不適用：規則即本檔該節 |",
    "| P0 原始碼型別（強型別、外部輸入、strict checker） | [P0：原始碼型別](#p0-source-type) | "
    "[specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) + "
    "[implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |",
    "| P0 權限與所有權（治理文件歸屬、角色、worktree、Secret） | [P0：權限與所有權](#p0-permissions) | "
    "[implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) + "
    "[security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |",
    "| 啟動順序（動手前的讀取順序） | [啟動順序](#startup-order) | 不適用：規則即本檔該節 |",
    "| target project 正式來源的標準位置 | [Target project 正式來源](#target-sources) | 不適用：規則即本檔該節 |",
)
INDEX_BASE_ROWS: tuple[str, ...] = (
    "| 任一事件、完成、等待或 HALT | [Router](Workflow.md#workflow-router) | "
    "[router-control](skills/johnny-project-takeover/references/router-control.md) |",
    "| POC/MVP/COMMERCIAL、模型或 lane 數量、staging | [Profile](Workflow.md#workflow-router) | "
    "[delivery-profile](skills/johnny-project-takeover/references/delivery-profile.md) |",
    "| 架構 owner、supervisor、implementer 休眠／喚醒 | [Model lifecycle](Workflow.md#workflow-router) | "
    "[model-role-routing](skills/johnny-project-takeover/references/model-role-routing.md) |",
    "| 最小 Context、旁路引用、能力選擇 | [Router Context](Workflow.md#workflow-router) | "
    "[context-routing](skills/johnny-project-takeover/references/context-routing.md) |",
    "| artifact tree、Agent Context 建立／換票／關閉 | [Router Context](Workflow.md#workflow-router) | "
    "[artifact-tree-routing](skills/johnny-project-takeover/references/artifact-tree-routing.md) + "
    "[agent-context-lifecycle](skills/johnny-project-takeover/references/agent-context-lifecycle.md) |",
    "| PRD／CHG 建立、取代、封存 | [Change control](Workflow.md#change-control) | "
    "[requirement-lineage](skills/johnny-project-takeover/references/requirement-lineage.md) |",
    "| reusable module catalog 查找／分區 | [Router Context](Workflow.md#workflow-router) | "
    "[module-catalog-routing](skills/johnny-project-takeover/references/module-catalog-routing.md) |",
    "| 外部能力(map／craft／reduction)admission、tier／target 適配 | "
    "[Router Context](Workflow.md#workflow-router) | "
    "[capability-admission](skills/johnny-project-takeover/references/capability-admission.md) |",
    "| 新專案、需求、Bug、架構或變更 | [Discovery](Workflow.md#discovery) | "
    "[discovery-change](skills/johnny-project-takeover/references/discovery-change.md) |",
    "| Browser/WebView/DOM/JavaScript 不可信資料 | [XSS gate](Workflow.md#xss-review) | "
    "[xss-review](skills/johnny-project-takeover/references/xss-review.md) |",
    "| Secret、正式 Log、Provider、Webhook、外部 effect | [Security](Workflow.md#security) | "
    "[security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |",
    "| SPEC、ticket、DI、type preflight、dispatch | [Tickets](Workflow.md#tickets) | "
    "[specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) |",
    "| 低階模型 ticket 拆分或 admission | [Tickets](Workflow.md#tickets) | "
    "[ticket-decomposition](skills/johnny-project-takeover/references/ticket-decomposition.md) |",
    "| 正式 UI、Figma／截圖／brief／既有 design system | [Tickets](Workflow.md#tickets) | "
    "[ui-design-handoff](skills/johnny-project-takeover/references/ui-design-handoff.md) |",
    "| Owner、Agent control、task/worktree、correction | [Role boundary](Workflow.md#role-boundary) | "
    "[implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) |",
    "| TDD、strict type、smoke、completion | [Implementation](Workflow.md#implementation) | "
    "[implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |",
    "| TDD matrix 或獨立 review | [Review](Workflow.md#review-handoff) | "
    "[review-checks](skills/johnny-project-takeover/references/review-checks.md) + [CodeReview.md](CodeReview.md) |",
    "| 實作語言決策或驗證 | [SPEC/Tickets](Workflow.md#specification) | "
    "[language-policy](skills/johnny-project-takeover/references/language-policy.md) |",
)
# Ticket 81 item 7: the whole table, header to last row, pinned line for line (the five rows, then the eighteen
# rows that are lines 77 to 94 of `AGENTS.md` at the baseline commit 31f15b7c).
INDEX_TABLE: tuple[str, ...] = (INDEX_HEADER, INDEX_SEPARATOR, *INDEX_ROWS, *INDEX_BASE_ROWS)
# The reference files the five rows name; `copy_texts` copies them so the unmodified copy stays green.
ROW_REFERENCES: tuple[str, ...] = (
    "skills/johnny-project-takeover/references/specification-ticketing.md",
    "skills/johnny-project-takeover/references/implementation-tdd.md",
    "skills/johnny-project-takeover/references/implementation-authority.md",
    "skills/johnny-project-takeover/references/security-boundary.md",
)
LINK = re.compile(r"\[[^\]]*\]\(([^)]*)\)")

# The five steps of the start order, line for line as they are at the base commit 69b4cdfb (ticket item 1:
# "The five steps stay as they are").
START_ORDER_STEP_LINES: tuple[str, ...] = (
    "1. 讀取 target project 自己的 `AGENTS.md` 與本次 authority。",
    "2. 讀 [Workflow 流程圖](Workflow.md#workflow-flow) 定位目前 stage。",
    "3. 讀 [Router 路由表](Workflow.md#workflow-router)，取得唯一 action、owner、必要",
    "   artifact refs、skill reference、typed return 與 continuation。",
    "4. 完整讀取被指定的 skill reference；不要載入完整 Workflow、全部 references、",
    "   library 或聊天歷史。",
    "5. 完成一個動作後把 typed event 寫進受據，由下一個閘門腳本讀取狀態檔判定（Revision 04）；不得自行選下一關。",
)

# The sentences the review fixed (S79R-07, S79R-03, S79R-16); the paragraph is also pinned whole.
P0_SENTENCE = "P0 照常適用：不讀取或回覆 Secret、正式 Log，不讀 target repository 以外或其他 worktree 的檔案。"
NO_PROGRAM_SENTENCE = "不為定位而讀 Workflow 或 Router，不載入整棵樹，不寫受據，不執行閘門腳本、測試或其他程式。"
NOT_FOUND_SENTENCE = (
    "找不到該類索引、索引有歧義、leaf 不存在或索引與 leaf 記載的 revision 不符時，"
    "回答找不到並列出已查的路徑，不掃描、不憑記憶補答、不進入 Wayfinder。"
)
STOP_ON_CHANGE_SENTENCE = "查詢中發現需要改動時，回報後停下；只有使用者要求改動，才走上面的啟動順序。"
OLD_INDEX_SENTENCE = (
    "本插件規則的查詢以本檔「流程索引」為索引，只讀含該規則的那一份（已安裝的插件版本），並註明檔案與版本。"
)
INDEX_SENTENCE = (
    "本插件規則的查詢，使用者未指名確切檔案時，先讀本檔「流程索引」，取情境欄符合問題的一列"
    "（同時符合 P0 列與其他列時取 P0 列；其餘同時符合多列時，取表中較上面的一列），依該列解析到一份 leaf：第二欄連到本檔一節時即該節，"
    "否則為第三欄中含該規則的 reference；只讀含該規則的那一節（已安裝的插件版本），並註明檔案、章節與版本。"
)
NO_SEARCH_SENTENCE = (
    "定位只經索引與其連結，不以關鍵字搜尋（grep、全文搜尋）或逐檔瀏覽來找；"
    "索引沒有該規則的列時，照本段「找不到該類索引」那一句回答找不到並列出已查的路徑。"
)
NEXT_STEP_SENTENCE = "問下一步、能否派工、整合或核准，屬於推進流程，不是唯讀查詢。"

PARAGRAPH = (
    "唯讀查詢（只問某份文件的內容、某張票的狀態或某條規則的寫法，不要求改動）不走上面的啟動順序；"
    "target project 自己的治理檔另有規定時從其規定。"
    + P0_SENTENCE
    + "使用者指名確切檔案時只讀該檔；否則從該類文件的索引一次解析一條路徑到確切的 leaf。"
    + INDEX_SENTENCE
    + NO_SEARCH_SENTENCE
    + NO_PROGRAM_SENTENCE
    + "票的狀態以目前 checkout 已提交的 leaf 為準，不以索引列、其他 worktree 或未提交的檔案為準；"
    "回答附上 leaf 路徑與 commit；需要受據或佇列才能判定時照實說明，不推斷。"
    + NOT_FOUND_SENTENCE
    + STOP_ON_CHANGE_SENTENCE
    + NEXT_STEP_SENTENCE
)
REQUIRED_SENTENCES: tuple[tuple[str, str], ...] = (
    ("the P0 sentence", P0_SENTENCE),
    ("the sentence that sends a rule lookup through the 流程索引", INDEX_SENTENCE),
    ("the sentence that forbids locating a rule by search", NO_SEARCH_SENTENCE),
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
GUARD_STEP = (
    "1. Before anything else, look at the skills this session lists. If one of them belongs to the old plugin "
    "johnny-ai-skill (its name begins with johnny-ai-skill: or its file lies in a folder named johnny-ai-skill), "
    "stop: tell the user in plain words that the old 0.4.x plugin is still installed and that its rules conflict "
    "with this version, give the removal commands in section 5 of this plugin's README.md for the host in use, "
    "ask the user to open a new session after removing it, and do nothing else in this session. If the session "
    "lists no skills, go on to step 2."
)
START_STEPS = (
    GUARD_STEP + "\n"
    "2. A read-only question (the content of a document, the state of a ticket, the wording of a rule) is not a "
    "workflow action, unless the target project's own governing files route it otherwise: resolve it as the "
    "[read-only-lookup paragraph](../../AGENTS.md#read-only-lookup) of this plugin's `AGENTS.md` says, answer, "
    "and stop. Do not read `Workflow.md` for it. Asking for the next step, or whether something can be "
    "dispatched, integrated or approved, is a workflow action.\n"
    "3. Read the target project's own `AGENTS.md` and authority record.\n"
    "4. Read `../../Workflow.md` only far enough to identify the current stage and its routing row.\n"
    "5. Read exactly the reference named by that row, plus the minimum committed target artifacts it\n"
    "   requires. Do not load unrelated references, the full library or chat history.\n"
    "6. Execute one legal action, record its typed completion event in the receipt and let the next\n"
    "   gate script read the state files (Revision 04: the Router is the gate scripts over the state\n"
    "   files, not a process to re-enter). Do not select the next stage locally."
)

FRONTMATTER_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ ]+(.*?)[ \t]*$")
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


def check_anchored_headings(lines: list[str], defects: list[str]) -> None:
    """Each ticket 80 anchor stands on its own line, once, with a blank line before and after, above its heading."""
    for name, heading in ANCHORED_HEADINGS:
        anchor = f'<a id="{name}"></a>'
        if lines.count(anchor) != 1:
            defects.append(f"{AGENTS}: the anchor {anchor} must stand on its own line exactly once")
            continue
        at = lines.index(anchor)
        if at == 0 or lines[at - 1] != "" or lines[at + 1 : at + 3] != ["", heading]:
            defects.append(
                f"{AGENTS}: the anchor {anchor} must have a blank line before it and after it, "
                f"and stand directly above {heading!r}"
            )


def link_defects(root: Path, lines: list[str], row: str) -> list[str]:
    """Name each link of one index row that does not resolve: a `#name` needs exactly one anchor line of
    `AGENTS.md`, a path needs a file under `root`. An empty link is a defect."""
    found: list[str] = []
    for target in LINK.findall(row):
        if target in ("", "#"):
            found.append(f"{AGENTS}: the row {row[:40]!r} holds an empty link")
        elif target.startswith("#"):
            anchor = f'<a id="{target[1:]}"></a>'
            if lines.count(anchor) != 1:
                found.append(f"{AGENTS}: the link ({target}) resolves to no single line {anchor}")
        elif ".." in Path(target).parts or not (root / target).is_file():
            found.append(f"{AGENTS}: the link ({target}) names no file under the root")
    return found


def check_index_rows(lines: list[str], defects: list[str], root: Path) -> None:
    """The five rows stand exactly as written, in order, directly below the separator and above `| 任一事件`;
    every link in them resolves."""
    if lines.count(INDEX_HEADING) != 1:
        defects.append(f"{AGENTS}: the heading {INDEX_HEADING!r} must appear exactly once")
        return
    heading = lines.index(INDEX_HEADING)
    if lines[heading + 1 : heading + 4] != ["", INDEX_HEADER, INDEX_SEPARATOR]:
        defects.append(f"{AGENTS}: the 流程索引 table must keep its header line and its separator line")
        return
    first = heading + 4
    last = first + len(INDEX_ROWS)
    if lines[first:last] != list(INDEX_ROWS):
        defects.append(
            f"{AGENTS}: the five index rows must stand exactly as written, in order, directly below the separator line"
        )
    if not (last < len(lines) and lines[last].startswith(ROW_AFTER_THE_FIVE_START)):
        defects.append(f"{AGENTS}: the row that begins {ROW_AFTER_THE_FIVE_START!r} must follow the five rows")
    for row in lines[first:last]:
        defects.extend(link_defects(root, lines, row))
    check_index_table(lines, heading + 2, defects)


def index_table_lines(lines: list[str], header_at: int) -> list[str]:
    """The lines from the header to the first blank line after it."""
    end = header_at
    while end < len(lines) and lines[end] != "":
        end += 1
    return lines[header_at:end]


def check_index_table(lines: list[str], header_at: int, defects: list[str]) -> None:
    """The whole table equals `INDEX_TABLE`, and each link to an anchor of `AGENTS.md` itself (a target that
    begins with `#`, in any cell) appears in exactly one row; links into other files are not counted."""
    table = index_table_lines(lines, header_at)
    if table != list(INDEX_TABLE):
        defects.append(
            f"{AGENTS}: the 流程索引 table must equal INDEX_TABLE: the header, the separator, the five rows, "
            "then the eighteen base rows, in that order"
        )
    rows_per_anchor: dict[str, int] = {}
    for row in table[2:]:
        for target in {target for target in LINK.findall(row) if target.startswith("#")}:
            rows_per_anchor[target] = rows_per_anchor.get(target, 0) + 1
    for target, count in sorted(rows_per_anchor.items()):
        if count != 1:
            defects.append(
                f"{AGENTS}: the anchor link ({target}) appears in {count} rows of the 流程索引; it must be in exactly one"
            )


def check_agents(text: str, defects: list[str], root: Path) -> None:
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
    if OLD_INDEX_SENTENCE in text:
        defects.append(f"{AGENTS}: the old index sentence (one file, no section, no ban on search) is back")
    check_anchored_headings(lines, defects)
    check_index_rows(lines, defects, root)

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

    # The five steps stay as they were at the base: the block runs to the first blank line and is pinned whole.
    cursor = heading + 4
    while cursor < len(lines) and lines[cursor] != "":
        cursor += 1
    if lines[heading + 4 : cursor] != list(START_ORDER_STEP_LINES):
        defects.append(f"{AGENTS}: the start order must keep its five steps exactly as they were (ticket item 1)")
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
            f"{SKILL}: {START_HEADING!r} must be the guard step, then the read-only step, then the four "
            "original steps renumbered 3 to 6, in order, word for word"
        )


def find_defects(root: Path) -> list[str]:
    defects: list[str] = []
    agents = read_utf8(root, AGENTS, defects)
    if agents is not None:
        check_agents(agents, defects, root)
    skill = read_utf8(root, SKILL, defects)
    if skill is not None:
        check_skill(skill, defects)
    return defects


def remove_text(sentence: str) -> Callable[[str], str]:
    """An edit that deletes `sentence` from a text."""

    def edit(text: str) -> str:
        return text.replace(sentence, "")

    return edit


def replace_text(old: str, new: str) -> Callable[[str], str]:
    """An edit that replaces `old` with `new` in a text."""

    def edit(text: str) -> str:
        return text.replace(old, new)

    return edit


def copy_texts(root: Path) -> None:
    for name in (AGENTS, SKILL, *ROW_REFERENCES):
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

    def test_each_of_the_five_index_rows_removed_is_red(self) -> None:
        for row in INDEX_ROWS:
            with self.subTest(row=row[:30]):
                self.assert_red(AGENTS, remove_text(row + "\n"), "five index rows")

    def test_two_index_rows_swapped_are_red(self) -> None:
        first, second = INDEX_ROWS[0], INDEX_ROWS[1]
        self.assert_red(AGENTS, lambda t: t.replace(first + "\n" + second, second + "\n" + first), "five index rows")

    def test_the_rows_placed_below_the_any_event_row_are_red(self) -> None:
        block = "\n".join(INDEX_ROWS) + "\n"

        def move(text: str) -> str:
            lines = text.replace(block, "").split("\n")
            at = next(i for i, line in enumerate(lines) if line.startswith(ROW_AFTER_THE_FIVE_START))
            return "\n".join(lines[: at + 1] + block.rstrip("\n").split("\n") + lines[at + 1 :])

        self.assert_red(AGENTS, move, "five index rows")

    def test_an_anchor_removed_renamed_or_detached_is_red(self) -> None:
        for name, heading in ANCHORED_HEADINGS:
            anchor = f'<a id="{name}"></a>'
            with self.subTest(anchor=name, damage="removed"):
                self.assert_red(AGENTS, remove_text(anchor + "\n\n"), f"the anchor {anchor}")
            with self.subTest(anchor=name, damage="renamed"):
                self.assert_red(AGENTS, replace_text(anchor, f'<a id="{name}-x"></a>'), f"the anchor {anchor}")
            with self.subTest(anchor=name, damage="no blank line before the heading"):
                self.assert_red(AGENTS, replace_text(anchor + "\n\n" + heading, anchor + "\n" + heading), "blank line")

    def test_a_prefix_anchor_does_not_satisfy_the_link(self) -> None:
        self.assert_red(
            AGENTS,
            lambda t: t.replace('<a id="p0-permissions"></a>', '<a id="p0-permissions-x"></a>'),
            "(#p0-permissions) resolves to no single line",
        )

    def test_a_row_link_to_an_anchor_that_does_not_exist_is_red(self) -> None:
        self.assert_red(
            AGENTS,
            lambda t: t.replace("(#startup-order)", "(#start-order)"),
            "(#start-order) resolves to no single line",
        )

    def test_a_row_link_to_a_reference_that_does_not_exist_is_red(self) -> None:
        self.assert_red(
            AGENTS,
            lambda t: t.replace("references/implementation-tdd.md)", "references/implementation-tdd-x.md)"),
            "names no file under the root",
        )

    def test_a_row_with_an_empty_link_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace("](#startup-order)", "]()"), "empty link")

    def test_the_no_search_sentence_removed_is_red(self) -> None:
        self.assert_red(AGENTS, remove_text(NO_SEARCH_SENTENCE), "forbids locating a rule by search")

    def test_the_old_index_sentence_put_back_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace(INDEX_SENTENCE, OLD_INDEX_SENTENCE), "old index sentence")

    def test_a_table_without_its_separator_line_is_a_named_defect(self) -> None:
        self.assert_red(AGENTS, remove_text(INDEX_SEPARATOR + "\n"), "header line and its separator line")

    def test_an_empty_table_is_a_named_defect(self) -> None:
        def empty(text: str) -> str:
            head, separator, rest = text.partition(INDEX_SEPARATOR + "\n")
            return head + separator + "\n" + rest.split("\n\n", 1)[1]

        self.assert_red(AGENTS, empty, "five index rows")

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
        # Ticket 81: lines 2 and 3 of START_STEPS (indexes 1 and 2) swapped.
        first = START_STEPS.split("\n")[1]
        second = START_STEPS.split("\n")[2]
        self.assert_red(SKILL, lambda t: t.replace(first + "\n" + second, second + "\n" + first), "Start")

    def test_the_guard_step_removed_is_red(self) -> None:
        self.assert_red(SKILL, remove_text(GUARD_STEP + "\n"), "Start")

    def test_the_guard_step_placed_after_the_read_only_step_is_red(self) -> None:
        guard = START_STEPS.split("\n")[0]
        read_only = START_STEPS.split("\n")[1]
        self.assert_red(SKILL, lambda t: t.replace(guard + "\n" + read_only, read_only + "\n" + guard), "Start")

    def test_one_word_of_the_guard_step_changed_is_red(self) -> None:
        self.assert_red(
            SKILL, lambda t: t.replace("do nothing else in this session", "do little else in this session"), "Start"
        )

    def test_the_guard_step_holds_no_path_token_in_backticks(self) -> None:
        self.assertNotIn("`", GUARD_STEP)

    def test_an_empty_start_section_is_red_and_named(self) -> None:
        self.assert_red(SKILL, lambda t: t.replace(START_STEPS, ""), "Start")

    def test_a_start_order_step_reworded_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace("取得唯一 action", "取得 action"), "five steps")

    def test_a_start_order_step_deleted_is_red(self) -> None:
        self.assert_red(AGENTS, lambda t: t.replace(START_ORDER_STEP_LINES[1] + "\n", ""), "five steps")

    def test_the_start_steps_not_renumbered_are_red(self) -> None:
        self.assert_red(
            SKILL,
            lambda t: t.replace("3. Read the target project's own", "2. Read the target project's own"),
            "Start",
        )

    def test_the_old_first_index_row_put_back_is_red(self) -> None:
        old_row = (
            "| 唯讀查詢（文件內容、票的狀態、規則寫法） | [唯讀查詢](#read-only-lookup) | 不適用：只讀索引指到的那一節 |"
        )
        self.assert_red(AGENTS, replace_text(INDEX_ROWS[0], old_row), "five index rows")

    def test_a_duplicate_p0_row_linking_the_same_anchor_is_red(self) -> None:
        duplicate = (
            "| P0 原始碼型別（重複） | [P0：原始碼型別](#p0-source-type) | "
            "[implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |"
        )
        last = INDEX_BASE_ROWS[-1]
        self.assert_red(AGENTS, replace_text(last, last + "\n" + duplicate), "(#p0-source-type) appears in 2 rows")

    def test_a_duplicate_p0_row_linking_other_files_is_red(self) -> None:
        duplicate = (
            "| P0 原始碼型別（重複） | [Tickets](Workflow.md#tickets) | "
            "[language-policy](skills/johnny-project-takeover/references/language-policy.md) |"
        )
        last = INDEX_BASE_ROWS[-1]
        self.assert_red(AGENTS, replace_text(last, last + "\n" + duplicate), "must equal INDEX_TABLE")

    def test_two_base_rows_swapped_are_red(self) -> None:
        first, second = INDEX_BASE_ROWS[1], INDEX_BASE_ROWS[2]
        self.assert_red(
            AGENTS, lambda t: t.replace(first + "\n" + second, second + "\n" + first), "must equal INDEX_TABLE"
        )

    def test_the_first_row_widened_back_with_the_rule_wording_is_red(self) -> None:
        self.assert_red(
            AGENTS,
            replace_text("| 唯讀查詢本身的規則（怎麼查、", "| 唯讀查詢本身的規則（規則寫法、怎麼查、"),
            "five index rows",
        )

    def test_the_tie_break_clause_removed_is_red(self) -> None:
        self.assert_red(
            AGENTS,
            remove_text("；其餘同時符合多列時，取表中較上面的一列"),
            "the sentence that sends a rule lookup through the 流程索引",
        )

    def test_the_table_equals_the_pinned_table_and_each_anchor_link_stands_in_one_row(self) -> None:
        lines = (REPO / AGENTS).read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
        header_at = lines.index(INDEX_HEADER)
        self.assertEqual(index_table_lines(lines, header_at), list(INDEX_TABLE))
        anchors = [target for row in INDEX_TABLE[2:] for target in set(LINK.findall(row)) if target.startswith("#")]
        self.assertEqual(len(anchors), len(set(anchors)))

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
