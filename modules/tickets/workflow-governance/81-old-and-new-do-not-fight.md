# 81｜Old and new do not fight: the skill stops when the old plugin is still installed, the README explains the host's decline record, a version is never published twice, and the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner decisions 2026-11-26: host CLI drift "放寬", old and new must not fight "A"） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision03 / receipt under `.worktrees/81-coexist-out/` / owner implementation seat / worktree `.worktrees/81-coexist` / branch `cp/wave3-81-coexist` / baseline the `cp/wave3` commit named in the dispatch, after ticket 80 is integrated |
| 實作語言 | Markdown governance text and JSON; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `PLANNED`（revision02; strict tier; rule-only review of revision01 CHANGES_REQUESTED; revision02 applies the reviewer's exact fixes (`doc/reviews/workflow-governance/81-old-and-new-do-not-fight-ticket-review.md`); revision03 adds item 7 (owner decision 2026-11-26 "併進票 81 修", from S80-01 and S80-02), with a rule-only review of that item; after ticket 80） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/81-coexist` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/81-coexist-review` |
| 責任邊界 | the first 流程索引 row in `AGENTS.md`, one new start step in `SKILL.md`, two paragraphs in README section 5, a release runbook, the tests that pin them, and the marketplace pin, the registered-failure reasons and the changelog for the rebuilt publication commit |
| 禁止修改 | every other line of `AGENTS.md`; `Workflow.md`, `CodeReview.md`, `library/`, `commands/`, `template/`, `.claude-plugin/plugin.json`, `ci/acceptance/`, `.github/` |
| 環境 | `LOCAL` and GitHub Actions on the development repository; nothing is pushed to the publication repository |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
modify = AGENTS.md
modify = skills/johnny-project-takeover/SKILL.md
modify = README.md
modify = tests/test_entry_read_only_lookup.py
modify = tests/test_plugin_payload_boundary.py
modify = .claude-plugin/marketplace.json
modify = ci/registered-failures.json
modify = doc/HARNESS-CHANGELOG.md
create = doc/runbooks/release.md
forbid = Workflow.md
forbid = CodeReview.md
forbid = library/
forbid = commands/
forbid = template/
forbid = .claude-plugin/plugin.json
forbid = ci/acceptance/
forbid = .github/
```

## 使用者拍板與可觀察結果

Process tier: strict.

**The decisions** are quoted in `REQ-20261103-043`, row "Owner decisions 2026-11-26 (host CLI drift: relax; old and new must not fight, "A")". The owner: "放寬,殘留的怎麼清乾淨／使用者更新不能一直讓舊版本跟新版本打架", and "A 0.5.0 加 (Recommended)".

**The risks:**
- **Both plugins installed.** A user who installs `software-factory` without removing `johnny-ai-skill` has both. Each ships a skill named `johnny-project-takeover`, so an agent may follow the old plugin's Router rules. Rules a project copied from 0.4.x (its `AGENTS.md`, `Workflow.md`, an activation block) are wave 4 T2 (`REQ-20261120-044`), not this guard.
- **The decline record.** After an uninstall, Claude Code 2.1.332 wrote the host's own decline record (`declinedPlugins`) in the user's host configuration. An explicit install still works, but a project that asks for the plugin may show no prompt.
- **Version caching.** Both hosts cache an installed plugin by its version. A version published twice reaches users as the stale copy.

After this ticket:

1. **`skills/johnny-project-takeover/SKILL.md`, a new first start step.**
   - Under `## Start`, a new step 1 goes before today's step 1. The old steps 1 to 5 become steps 2 to 6, and their text does not change.
   - The new step is exactly:
     "1. Before anything else, look at the skills this session lists. If one of them belongs to the old plugin johnny-ai-skill (its name begins with johnny-ai-skill: or its file lies in a folder named johnny-ai-skill), stop: tell the user in plain words that the old 0.4.x plugin is still installed and that its rules conflict with this version, give the removal commands in section 5 of this plugin's README.md for the host in use, ask the user to open a new session after removing it, and do nothing else in this session. If the session lists no skills, go on to step 2."
   - The step holds no path token in backticks.
   - Today's step 1 links `../../AGENTS.md#read-only-lookup`. That link stays.
2. **README section 5 (從舊版 johnny-ai-skill 換過來).**
   - After the line that begins 舊版的 plugin id 是, with one blank line on each side, this paragraph is added exactly:
     "新舊兩版同時裝著時，agent 可能照舊版的規則做事。新版開工的第一步會檢查這件事：看到舊版還在，就停下來請你先移除舊版，移除後再開一個新的 session。"
   - After the fenced block `codex plugin marketplace remove johnny-ai-skill --json` and before the line that begins 專案裡從早期版本, with one blank line on each side, this paragraph is added exactly:
     "在 Claude Code 2.1.332 上，用 uninstall 移除插件後，Claude Code 會在它自己的設定裡留下一筆「已拒絕」這個插件的紀錄；這筆紀錄沒有擋住之後明確的安裝。如果某個專案要求安裝 Software Factory 卻沒有跳出提示，直接執行第 3 節的安裝指令即可。"
   - Neither paragraph holds inline code, a path, or a link.
3. **`doc/runbooks/release.md`, new.** It holds these sections:
   - **The rule.** It is stated exactly: "A version number is never published twice. Once tag `plugin-vX.Y.Z` is pushed to the publication repository, any change to the published plugin tree ships as a new version. Before a publish, run `git ls-remote --tags https://github.com/johnnyliu365-sys/software-factory-plugin.git "refs/tags/plugin-v*"`: it must list no `refs/tags/plugin-vX.Y.Z` for the new version, and the new version must be greater, in semantic-version order, than every version it lists. If either check fails, HALT before the push. Tags are immutable as `doc/adr/ADR-20260823-018-version-specific-publication-tag-payloads.md` decides."
   - **The order.** It names `modules/tickets/workflow-governance/71-publication-0-5.md`, the paragraph that begins "**The release, after review approval**" (steps 1 to 9), and copies none of its steps. It says that the publication commit is the one the released ticket's 正式環境移植 SOP names, in place of ticket 71's, as ticket 80's SOP first did, and that the rule above is checked before step 3. Each push waits for the owner's confirmation.
   - **Before release.** While the check above lists no tag for the version, the local candidate may be rebuilt under the same version, and every rebuild is reinstalled and its cached copies checked as ticket 80 item 5 says.
4. **Tests.**
   - `tests/test_entry_read_only_lookup.py`: `START_STEPS` takes the new step 1 and the renumbered steps. A new injection case checks that the guard step removed, or moved after the read-only step, turns the test red. In `test_the_start_steps_not_renumbered_are_red` the edit replaces `3. Read the target project's own` with `2. Read the target project's own`. `test_the_new_start_step_moved_after_the_original_first_step_is_red` swaps lines 2 and 3 of `START_STEPS` (indexes 1 and 2). The `## Start` defect message and the module docstring say: the guard step, then the read-only step, then the four original steps renumbered 3 to 6.
   - `tests/test_plugin_payload_boundary.py`: a check that README section 5 holds both paragraphs word for word.
5. **The rebuilt publication commit.** `SKILL.md` and `README.md` are in the payload, so the publication commit changes.
   - Rebuild it exactly as ticket 80 item 5 says, through these steps: the temporary ref `refs/heads/publication-0.5.0-t81`, the OLD check, `update-ref` with OLD, then deleting the temporary ref.
   - OLD is the sha that `.claude-plugin/marketplace.json` pins at this ticket's baseline commit (ticket 80's publication commit); in a correction round it is the id the previous round of this ticket recorded in G1. `git rev-parse refs/heads/publication-0.5.0` must print OLD; otherwise HALT. If this ticket is closed without integration, the control plane runs `git update-ref refs/heads/publication-0.5.0 <ticket 80's publication commit> <the id on the ref>`.
   - Each of the eight occurrences of OLD in `ci/registered-failures.json` becomes the new 40-hex id; no other byte changes.
   - Run `--verify-only`.
   - Check the extracted package. It holds the new step and both paragraphs.
   - Rebuild the local marketplace's plugin tree.
   - The STATEMENT gives the owner's refresh commands and cache checks, as ticket 80 item 5 does: the owner checks `%USERPROFILE%\.claude\plugins\cache\software-factory\software-factory\0.5.0\skills\johnny-project-takeover\SKILL.md` and `$CODEX_HOME\plugins\cache\software-factory\software-factory\0.5.0\skills\johnny-project-takeover\SKILL.md`, each for a line that begins `1. Before anything else, look at the skills this session lists.`; the rest as ticket 80 item 5.
6. **`doc/HARNESS-CHANGELOG.md`.**
   - Directly below the ticket 80 row: `| 2026-11-26 | The skill stops when the old plugin johnny-ai-skill is still installed; the README explains the host's decline record; a version is never published twice (ticket 81) | `REQ-20261103-043`, owner decisions 2026-11-26 | `modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md` |`.
   - In the `## 0.5.0` section, as the last bullet of the part about moving from `johnny-ai-skill`: `- With both plugins installed, the new skill stops at its first step and asks the user to remove the old one and open a new session.`
7. **`AGENTS.md`, the first 流程索引 row** (owner decision 2026-11-26 "併進票 81 修", quoted in `REQ-20261103-043`; ticket 80 review S80-01 and S80-02).
   - The row `| 唯讀查詢（文件內容、票的狀態、規則寫法） | [唯讀查詢](#read-only-lookup) | 不適用：只讀索引指到的那一節 |` becomes exactly `| 唯讀查詢本身的規則（怎麼查、查不到時怎麼回答） | [唯讀查詢](#read-only-lookup) | 不適用：規則即本檔該節 |`.
   - No other line of `AGENTS.md` changes.
   - `tests/test_entry_read_only_lookup.py`:
     - the expected first row takes the new text;
     - a new check requires each `#anchor` link of the 流程索引 to appear in exactly one row, so a duplicate row that points to an anchor another row already names is red;
     - the docstring says how many files `copy_texts` copies.
   - TDD 2 gains three cases: the old first row put back; a duplicate P0 row appended to the table; the first row's 情境 widened back with 「規則寫法」.
   - The extracted package's `AGENTS.md` holds the new first row (item 5's package check).

**After review approval and integration, control-plane and owner work, not this seat's:**
1. Ticket 77 goes to revision04 with the relaxed rules of the 2026-11-26 decision:
   - the host's decline record is in the residue allow-list, with its reason;
   - `@builtin` entries are not counted;
   - a reinstall succeeds while the record is present.
   Its local lifecycle then reruns with this ticket's publication commit. Ticket 77's cloud trigger passes `expected_publication` equal to this ticket's publication commit.
2. **The owner-assisted test** adds the two-versions case: with `johnny-ai-skill` 0.4.14 and `software-factory` 0.5.0 both installed, the session stops at the new step 1 and gives the removal commands. The owner invokes the new plugin's entry by its plugin-qualified name where the host offers one (`/software-factory:johnny-project-takeover` in Claude Code); if the session loads the old plugin's skill instead, the record says so.

## 實作範圍、依賴與 ticket elements

### 角色指派（必填）

- 流程／Grill／ticket owner：control plane.
- implementation owner：`implementation-standard` seat in `.worktrees/81-coexist`.
- reviewer：`ticket-review` seat in `.worktrees/81-coexist-review`.
- **Owner override record**：N/A.
- `ImplementationHandoff`：this ticket; tickets 79 and 80 (the start steps, the lookup test, the rebuild procedure); ticket 71 (README section 5).
- `ImplementationReturn`：`COMPLETED → ACTION_COMPLETED`／`BLOCKED → HALT`／`CHANGE_DETECTED → REQUIREMENT_CHANGED → Grill`。A test outside the boundary that pins the changed text is a `CHANGE_DETECTED` return naming the test.

### 前端組合與依賴注入

**N/A reason**：governance text, JSON and tests; no UI boundary.

- element 路徑：不適用
- 實際原始碼路徑：the paths in the boundary block
- 公開契約／資料模型：the step, the two paragraphs and the rule above.

## TDD 設計

1. 正常行為：the committed `SKILL.md` and README pass the new checks; every check of tickets 79 and 80 still passes.
2. 規則違反／輸入錯誤, each turning a named test red:
   - the guard step removed;
   - the guard step placed after the read-only step;
   - one word of the guard step changed;
   - one README paragraph removed;
   - one README paragraph changed.
3. 外部失敗／fail-closed：a missing `SKILL.md` or README is a named defect, not a traceback.
4. 回歸保護：the payload closure test passes; the publication route checks pass; `--verify-only` passes with the new pin.

### 適用的缺陷類別

| # | 類別 | 是否適用 | 本工單的必要案例 |
| --- | --- | --- | --- |
| 1 | 路徑前綴誤匹配 | 否 | no path matching changes |
| 2 | null／空字串／陣列 | 是 | an empty `## Start` section |
| 3 | 權限繞過 | 是 | the plugin never edits the user's host configuration; the README tells the user to install, not to edit it |
| 4 | Token 格式與比較 | 是 | texts compared exactly; the pin as 40 lower-case hex |
| 5 | 錯誤碼是否一致 | 否 | no exit codes change |
| 6 | 例外是否會拋出 | 是 | a missing file is a named defect |

## 完成定義與證據

- `python -m pytest tests/test_entry_read_only_lookup.py tests/test_plugin_payload_boundary.py tests/test_plugin_publication.py tests/test_governance_consistency.py -q` exits 0 on the host with the local anchor ref, apart from registered base failures; `mypy --strict` on the two changed test files exits 0.
- **G1**, **V1**, **K1**, **L1** as ticket 80 defines them.
- **反向突變證據**: every case of TDD 2, each restored after it turns a named test red.
- **CI evidence**: one run on a commit of this branch with both jobs `success`.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The release follows `doc/runbooks/release.md` with this ticket's publication commit in place of ticket 80's. Each push waits for the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
