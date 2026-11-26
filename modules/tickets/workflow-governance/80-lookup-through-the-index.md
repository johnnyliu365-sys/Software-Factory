# 80｜A read-only lookup goes through the 流程索引: the index gains rows for every rule section of AGENTS.md, the lookup never locates by search, and the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner finding and decision 2026-11-26 "A": a read-only lookup must go through the 流程索引, fixed before the 0.5.0 release; owner decision 2026-11-26 "一起補" on the index scope） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision02 / receipt under `.worktrees/80-index-out/` / owner implementation seat / worktree `.worktrees/80-index` / branch `cp/wave3-80-index` / baseline the `cp/wave3` commit named in the dispatch |
| 實作語言 | Markdown governance text and JSON; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `INTEGRATED`; dispatch=sha256:f63daf3a038b415f33939b0ac0ad560433541d92d75f812b372ea3366e819ea1 (`doc/handoffs/2026/workflow-governance/dispatch/JAS-80-1.yaml`)（candidate `7ec1f539`; initial review `APPROVED`） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/80-index` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/80-index-review` |
| 責任邊界 | three anchors, five index rows and one sentence of the lookup paragraph in `AGENTS.md`; the lookup test; the marketplace pin, the registered-failure reasons and the changelog for the rebuilt publication commit |
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

The answer was right, but the path was a scan, and the lookup paragraph forbids scanning. The owner: "流程索引／很重要". There are two causes:
- The 流程索引 has no row for the rule sections of `AGENTS.md` itself.
- The paragraph does not say that a keyword search is not a way to locate a rule.

The decisions are quoted in `REQ-20261103-043`, in the row "Owner finding and decision 2026-11-26 (a read-only lookup must go through the 流程索引, "A")" and the row after it, on the index scope ("一起補"). The rule-only review of revision01 is in `doc/reviews/workflow-governance/80-lookup-through-the-index-ticket-review.md`.

After this ticket:

1. **`AGENTS.md`, three anchors.**
   - `<a id="startup-order"></a>` goes directly above `## 啟動順序`.
   - `<a id="p0-permissions"></a>` goes directly above `## P0：權限與所有權`.
   - `<a id="target-sources"></a>` goes directly above `## Target project 正式來源`.
   - Each anchor stands on its own line, with a blank line before it and after it, as `p0-source-type` stands above `## P0：原始碼型別`.
   - No other line around them changes.
2. **`AGENTS.md`, the 流程索引.** Five rows go directly below the table's separator line, above the row that begins "| 任一事件". They go in this order, exactly as written here:

   ```text
   | 唯讀查詢（文件內容、票的狀態、規則寫法） | [唯讀查詢](#read-only-lookup) | 不適用：只讀索引指到的那一節 |
   | P0 原始碼型別（強型別、外部輸入、strict checker） | [P0：原始碼型別](#p0-source-type) | [specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) + [implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |
   | P0 權限與所有權（治理文件歸屬、角色、worktree、Secret） | [P0：權限與所有權](#p0-permissions) | [implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) + [security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |
   | 啟動順序（動手前的讀取順序） | [啟動順序](#startup-order) | 不適用：規則即本檔該節 |
   | target project 正式來源的標準位置 | [Target project 正式來源](#target-sources) | 不適用：規則即本檔該節 |
   ```

   - The table's header and its other rows do not change.
3. **`AGENTS.md`, the lookup paragraph.**
   - **The sentence replaced.** In the paragraph below the anchor `read-only-lookup`, this sentence:
     "本插件規則的查詢以本檔「流程索引」為索引，只讀含該規則的那一份（已安裝的插件版本），並註明檔案與版本。"
     becomes exactly:
     "本插件規則的查詢，使用者未指名確切檔案時，先讀本檔「流程索引」，取情境欄符合問題的一列（同時符合 P0 列與其他列時取 P0 列），依該列解析到一份 leaf：第二欄連到本檔一節時即該節，否則為第三欄中含該規則的 reference；只讀含該規則的那一節（已安裝的插件版本），並註明檔案、章節與版本。定位只經索引與其連結，不以關鍵字搜尋（grep、全文搜尋）或逐檔瀏覽來找；索引沒有該規則的列時，照本段「找不到該類索引」那一句回答找不到並列出已查的路徑。"
   - **Everything else stays.** No other sentence of the paragraph changes, and the paragraph stays one line.
4. **`tests/test_entry_read_only_lookup.py`.**
   - The paragraph constant takes the new text.
   - Two new constants, `INDEX_SENTENCE` (the first sentence above) and `NO_SEARCH_SENTENCE` (from 「定位只經」 to the end), both go in `REQUIRED_SENTENCES`.
   - **New checks:**
     - the five rows stand exactly as written, in order, directly below the separator;
     - each of the anchors `startup-order`, `p0-permissions` and `target-sources` stands on its own line with its blank lines, directly above its heading;
     - every link in the rows resolves:
       - each `#name` matches exactly one line `<a id="name"></a>` in `AGENTS.md`;
       - each reference path exists under the root that `find_defects` reads;
       - `copy_texts` also copies the four reference files the rows name, so the unmodified copy stays green.
   - The existing checks stay.
5. **The rebuilt publication commit.** `AGENTS.md` is in the payload, so the publication commit changes.
   - **Generate.**
     - Items 1 to 4 are committed, and `git status --porcelain` prints nothing.
     - OLD is `d355b4a26336cebbe4e8e28650ce0120d4c39a13` in the first round; in a correction round it is the id the previous round recorded in G1.
     - `git rev-parse refs/heads/publication-0.5.0` must print OLD; otherwise HALT.
     - Run `python -m library.local_orchestration.plugin_publication --repo . --manifest .claude-plugin/plugin.json --marketplace .claude-plugin/marketplace.json --ref refs/heads/publication-0.5.0-t80` twice. Both runs must print the same new id.
     - The generator moves the ref it is given without an old value, so it is never given `refs/heads/publication-0.5.0`. The id does not depend on the ref name.
   - **Repin.** The generator repins the development `marketplace.json`.
   - **Move the local ref.**
     - Run `git update-ref refs/heads/publication-0.5.0 <new> OLD`, then `git update-ref -d refs/heads/publication-0.5.0-t80 <new>`.
     - Afterwards `git rev-parse refs/heads/publication-0.5.0` prints `<new>`, and `git show-ref refs/heads/publication-0.5.0-t80` prints nothing.
     - The ref is shared by every worktree. From the move until this ticket integrates, the four publication tests run on this host fail in any checkout that still pins `d355b4a2…`, so the STATEMENT gives the time of the move.
     - If this ticket is closed without integration, the control plane runs `git update-ref refs/heads/publication-0.5.0 d355b4a26336cebbe4e8e28650ce0120d4c39a13 <the id on the ref>`.
   - **Registered rows.** In `ci/registered-failures.json`, each of the eight occurrences of `d355b4a26336cebbe4e8e28650ce0120d4c39a13` becomes the new 40-hex id. No other byte of the file changes.
   - **Verify.** `--verify-only --ref refs/heads/publication-0.5.0` passes.
   - **Check the extracted package:**
     - its `AGENTS.md` holds the five rows and the new sentence;
     - `plugin.json` says `software-factory` and `0.5.0`;
     - it holds no `.codex-plugin` and none of the Level 2 files that ticket 71 item 7 lists;
     - its own marketplace copy holds forty zeros.
   - **Rebuild the local marketplace.**
     - Rebuild `C:/Temp/claude/sf-050-local/plugins/software-factory/` from the extracted package. Remove the old tree first.
     - If the old tree cannot be removed completely, HALT naming the path that remains; do not build over it.
     - Leave both marketplace files unchanged.
   - **The STATEMENT** gives the owner's commands to refresh the installed copies. The version stays `0.5.0`, so each host is uninstalled and installed again:
     - Claude Code, in `C:\Temp\claude\sf-test-project`: `claude plugin uninstall software-factory@software-factory --scope local`, then `claude plugin install software-factory@software-factory --scope local`;
     - Codex: `codex plugin remove software-factory@software-factory --json`, then `codex plugin add software-factory@software-factory --json`.
     - After both refreshes, the owner checks two files, each for a line that begins `| P0 原始碼型別`:
       - `%USERPROFILE%\.claude\plugins\cache\software-factory\software-factory\0.5.0\AGENTS.md`;
       - `$CODEX_HOME\plugins\cache\software-factory\software-factory\0.5.0\AGENTS.md` (`$CODEX_HOME` defaults to `%USERPROFILE%\.codex`).
       If a file lacks that line, that host was not refreshed. The owner removes that host's `0.5.0` cache folder and installs again.
6. **`doc/HARNESS-CHANGELOG.md`.**
   - Directly below the ticket 79 row: `| 2026-11-26 | A read-only lookup goes through the 流程索引, and the index gains rows for the two P0 sections, the start order and the target project's sources (ticket 80) | `REQ-20261103-043`, owner decision 2026-11-26 "A" | `modules/tickets/workflow-governance/80-lookup-through-the-index.md` |`.
   - As the last bullet of `### What to read instead`: `- A question about a rule is answered through the 流程索引 of `AGENTS.md`: its row links the one section to read, and a keyword search is not a way to find a rule.`

**After review approval and integration, control-plane work, not this seat's:**
1. Rerun ticket 77's local lifecycle (`--host both --steps build,fresh,upgrade,uninstall,recover,level2`) at the first `cp/wave3` commit that holds both ticket 77 and this ticket, with `--expected-publication` set to this ticket's publication commit. Add it to ticket 77's acceptance record.
2. The owner refreshes the installed copies and asks the same P0 question again. The record notes which files the session read.
3. Ticket 77's cloud trigger passes `expected_publication` equal to this ticket's publication commit. Under ticket 77, the text `<ticket 71's publication commit>` in `ci/acceptance/README.md` becomes `<the publication commit the development marketplace.json pins>`. This ticket forbids `ci/acceptance/`.

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
- 公開契約／資料模型：the five rows, the three anchors and the sentence above.

## TDD 設計

1. 正常行為：the committed `AGENTS.md` passes every check of item 4.
2. 規則違反／輸入錯誤, each turning the test red:
   - one of the five rows removed;
   - two of the rows swapped;
   - the rows placed below "| 任一事件";
   - one of the anchors `startup-order`, `p0-permissions` or `target-sources` removed or renamed;
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

- The release follows ticket 71's release order (`71-publication-0-5.md` lines 187 to 195), with this ticket's publication commit in place of `d355b4a2…`:
  - Step 3 pushes this ticket's commit with tag `plugin-v0.5.0`.
  - Step 4's `marketplace` branch holds the development `marketplace.json` at this ticket's integration, which pins this ticket's commit.
  - Step 5 pushes `refs/heads/publication-0.5.0` at this ticket's commit.
  - Each push waits for the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
