# 80｜A read-only lookup goes through the 流程索引: the index gains the two P0 sections, the lookup never locates by search, and the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner finding and decision 2026-11-26 "A": a read-only lookup must go through the 流程索引, fixed before the 0.5.0 release） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision01 / receipt under `.worktrees/80-index-out/` / owner implementation seat / worktree `.worktrees/80-index` / branch `cp/wave3-80-index` / baseline the `cp/wave3` commit named in the dispatch |
| 實作語言 | Markdown governance text and JSON; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `PLANNED`（revision01; strict tier; rule-only review before dispatch） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/80-index` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/80-index-review` |
| 責任邊界 | one anchor, three index rows and one sentence of the lookup paragraph in `AGENTS.md`; the lookup test; the marketplace pin, the registered-failure reasons and one changelog row for the rebuilt publication commit |
| 禁止修改 | `Workflow.md`, `CodeReview.md`, `skills/`, `library/`, `commands/`, `template/`, `.claude-plugin/plugin.json`, `README.md`, `ci/acceptance/`, `.github/` |
| 環境 | `LOCAL` and GitHub Actions on the development repository; nothing is pushed to the publication repository |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
modify = AGENTS.md
modify = tests/test_entry_read_only_lookup.py
modify = .claude-plugin/marketplace.json
modify = ci/registered-failures.json
modify = doc/HARNESS-CHANGELOG.md
forbid = Workflow.md
forbid = CodeReview.md
forbid = skills/
forbid = library/
forbid = commands/
forbid = template/
forbid = .claude-plugin/plugin.json
forbid = README.md
forbid = ci/acceptance/
forbid = .github/
```

## 使用者拍板與可觀察結果

Process tier: strict.

**The problem.** The owner tested the 0.5.0 candidate in a desktop session, in an empty project with the plugin installed, and asked "P0 原始碼型別的規定是什麼？". The session went like this:
1. It searched the installed `AGENTS.md` for `read-only-lookup|唯讀|read-only`.
2. It searched "P0" across 4 files.
3. It read `AGENTS.md` lines 33 to 43.

The answer was right, but the path was a scan, and the lookup paragraph forbids scanning. The owner: "流程索引／很重要". The decision is quoted in `REQ-20261103-043`, row "Owner finding and decision 2026-11-26 (a read-only lookup must go through the 流程索引, "A")".

There are two causes:
- The 流程索引 has no row for the two P0 sections.
- The paragraph does not say that a keyword search is not a way to locate a rule.

After this ticket:

1. **`AGENTS.md`, an anchor.**
   - The anchor `<a id="p0-permissions"></a>` stands on its own line directly above the heading `## P0：權限與所有權`, with a blank line before it and after it, as `p0-source-type` stands above `## P0：原始碼型別`.
   - No other line around it changes.
2. **`AGENTS.md`, the 流程索引.** Three rows go directly below the table's separator line, above the row that begins "| 任一事件". They go in this order, exactly as written here:

   ```text
   | 唯讀查詢（文件內容、票的狀態、規則寫法） | [唯讀查詢](#read-only-lookup) | 不適用：只讀索引指到的那一節 |
   | P0 原始碼型別（強型別、外部輸入、strict checker） | [P0：原始碼型別](#p0-source-type) | [specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) + [implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |
   | P0 權限與所有權（治理文件歸屬、角色、worktree、Secret） | [P0：權限與所有權](#p0-permissions) | [implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) + [security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |
   ```

   - The table's header and its other rows do not change.
3. **`AGENTS.md`, the lookup paragraph.**
   - **The sentence replaced.** In the paragraph below the anchor `read-only-lookup`, this sentence:
     "本插件規則的查詢以本檔「流程索引」為索引，只讀含該規則的那一份（已安裝的插件版本），並註明檔案與版本。"
     becomes exactly:
     "本插件規則的查詢先讀本檔「流程索引」，依其中一列的連結解析到一份 leaf，只讀含該規則的那一節（已安裝的插件版本），並註明檔案、章節與版本。定位只經索引與其連結，不以關鍵字搜尋（grep、全文搜尋）或逐檔瀏覽來找；索引沒有該規則的列時，照下方「找不到」處理。"
   - **Everything else stays.** No other sentence of the paragraph changes, and the paragraph stays one line.
4. **`tests/test_entry_read_only_lookup.py`.**
   - The paragraph constant takes the new sentence.
   - **New checks:**
     - the three rows stand exactly as written, in order, directly below the separator;
     - the anchor `p0-permissions` stands on its own line with its blank lines, directly above `## P0：權限與所有權`;
     - every link in the three rows resolves: each `#anchor` names an anchor that exists once in `AGENTS.md`, and each reference path exists in the repository;
     - the no-search sentence is present word for word.
   - The existing checks stay.
5. **The rebuilt publication commit.** `AGENTS.md` is in the payload, so the publication commit changes.
   - **Generate.** Run the committed generator exactly as ticket 71 item 6 runs it: `python -m library.local_orchestration.plugin_publication --repo . --manifest .claude-plugin/plugin.json --marketplace .claude-plugin/marketplace.json --ref refs/heads/publication-0.5.0`. Run it twice; both runs must give the same new id.
   - **Repin.** The generator repins the development `marketplace.json`.
   - **Move the local ref.** The seat moves the local ref `refs/heads/publication-0.5.0` from `d355b4a26336cebbe4e8e28650ce0120d4c39a13` to the new commit with `git update-ref refs/heads/publication-0.5.0 <new> d355b4a26336cebbe4e8e28650ce0120d4c39a13`. The ref is local and was never pushed.
   - **Registered rows.** In `ci/registered-failures.json`, the reason text of the eight rows names the new pin instead of `d355b4a2…`. Nothing else in the file changes.
   - **Verify.** `--verify-only --ref refs/heads/publication-0.5.0` passes.
   - **Check the extracted package:**
     - its `AGENTS.md` holds the three rows and the new sentence;
     - `plugin.json` says `software-factory` and `0.5.0`;
     - it holds no `.codex-plugin` and none of the Level 2 files that ticket 71 item 7 lists;
     - its own marketplace copy holds forty zeros.
   - **Rebuild the local marketplace.** Rebuild `C:/Temp/claude/sf-050-local/plugins/software-factory/` from the extracted package. Remove the old tree first. Leave both marketplace files unchanged.
   - **The STATEMENT** gives the owner's commands to refresh the installed copies. The version stays `0.5.0`, so each host is uninstalled and installed again:
     - Claude Code, in `C:\Temp\claude\sf-test-project`: `claude plugin uninstall software-factory@software-factory --scope local`, then `claude plugin install software-factory@software-factory --scope local`;
     - Codex: `codex plugin remove software-factory@software-factory --json`, then `codex plugin add software-factory@software-factory --json`.
6. **`doc/HARNESS-CHANGELOG.md`.** One new row in the table: a read-only lookup goes through the 流程索引, and the index covers the two P0 sections (ticket 80). The `## 0.5.0` section gains one sentence saying the same.

**After review approval and integration, control-plane work, not this seat's:**
1. Rerun ticket 77's local lifecycle (`--host both --steps build,fresh,upgrade,uninstall,recover,level2`) at the integration commit, with `--expected-publication` set to the new id. Add it to ticket 77's acceptance record.
2. The owner refreshes the installed copies and asks the same P0 question again. The record notes which files the session read.

## 實作範圍、依賴與 ticket elements

### 角色指派（必填）

- 流程／Grill／ticket owner：control plane.
- implementation owner：`implementation-standard` seat in `.worktrees/80-index`.
- reviewer：`ticket-review` seat in `.worktrees/80-index-review`.
- **Owner override record**：N/A.
- `ImplementationHandoff`：this ticket; ticket 79 (the lookup paragraph and its test); ticket 71 items 6 to 8 (generator, package check, local marketplace).
- `ImplementationReturn`：`COMPLETED → ACTION_COMPLETED`／`BLOCKED → HALT`／`CHANGE_DETECTED → REQUIREMENT_CHANGED → Grill`。A test outside the boundary that pins the changed text is a `CHANGE_DETECTED` return naming the test.

### 前端組合與依賴注入

**N/A reason**：governance text, JSON and tests; no UI boundary.

- element 路徑：不適用
- 實際原始碼路徑：the paths in the boundary block
- 公開契約／資料模型：the three rows, the anchor and the sentence above.

## TDD 設計

1. 正常行為：the committed `AGENTS.md` passes every check of item 4.
2. 規則違反／輸入錯誤, each turning the test red:
   - one of the three rows removed;
   - two of the rows swapped;
   - the rows placed below "| 任一事件";
   - the anchor `p0-permissions` removed or renamed;
   - a row's link pointing to an anchor that does not exist;
   - the no-search sentence removed;
   - the old sentence put back.
3. 外部失敗／fail-closed：a missing `AGENTS.md`, or a table without a separator line, fails with a named defect, not with a traceback.
4. 回歸保護：
   - every check of ticket 79 still passes;
   - the payload closure test passes with the new links;
   - `--verify-only` passes with the new pin.

### 適用的缺陷類別

| # | 類別 | 是否適用 | 本工單的必要案例 |
| --- | --- | --- | --- |
| 1 | 路徑前綴誤匹配 | 是 | an anchor `p0-permissions-x` does not satisfy `#p0-permissions` |
| 2 | null／空字串／陣列 | 是 | an empty table, and a row with an empty link |
| 3 | 權限繞過 | 否 | no access rule changes |
| 4 | Token 格式與比較 | 是 | rows and the sentence are compared exactly; the pin is compared as 40 lower-case hex |
| 5 | 錯誤碼是否一致 | 否 | no exit codes change |
| 6 | 例外是否會拋出 | 是 | a missing file is a named defect |

## 完成定義與證據

- `python -m pytest tests/test_entry_read_only_lookup.py tests/test_plugin_publication.py tests/test_plugin_payload_boundary.py tests/test_governance_consistency.py -q` exits 0 on the host, with the local anchor ref, apart from registered base failures. `mypy --strict` on the lookup test exits 0.
- **G1**: the generator runs twice and gives the same new id. **V1**: `--verify-only` exits 0. **K1**: the package check of item 5. **L1**: a listing of the rebuilt local marketplace, plus a diff showing its plugin tree equals the extracted package.
- **反向突變證據**: every case of TDD 2, each restored after it turns a named test red.
- **CI evidence**: one run on a commit of this branch with both jobs `success`. The eight rows stay registered.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The release follows ticket 71's release order with the new publication commit. Each push waits for the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
