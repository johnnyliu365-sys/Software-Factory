# 81｜Old and new do not fight: the skill stops when the old plugin is still installed, the README explains the host's decline record, a version is never published twice, and the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner decisions 2026-11-26: host CLI drift "放寬", old and new must not fight "A"） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision01 / receipt under `.worktrees/81-coexist-out/` / owner implementation seat / worktree `.worktrees/81-coexist` / branch `cp/wave3-81-coexist` / baseline the `cp/wave3` commit named in the dispatch, after ticket 80 is integrated |
| 實作語言 | Markdown governance text and JSON; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `PLANNED`（revision01; strict tier; rule-only review before dispatch; after ticket 80） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/81-coexist` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/81-coexist-review` |
| 責任邊界 | one new start step in `SKILL.md`, two paragraphs in README section 5, a release runbook, the tests that pin them, and the marketplace pin, the registered-failure reasons and the changelog for the rebuilt publication commit |
| 禁止修改 | `AGENTS.md`, `Workflow.md`, `CodeReview.md`, `library/`, `commands/`, `template/`, `.claude-plugin/plugin.json`, `ci/acceptance/`, `.github/` |
| 環境 | `LOCAL` and GitHub Actions on the development repository; nothing is pushed to the publication repository |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
modify = skills/johnny-project-takeover/SKILL.md
modify = README.md
modify = tests/test_entry_read_only_lookup.py
modify = tests/test_plugin_payload_boundary.py
modify = .claude-plugin/marketplace.json
modify = ci/registered-failures.json
modify = doc/HARNESS-CHANGELOG.md
create = doc/runbooks/release.md
forbid = AGENTS.md
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
- **Both plugins installed.** A user who installs `software-factory` without removing `johnny-ai-skill` has both. Each ships a skill named `johnny-project-takeover`, so an agent may follow the old plugin's Router rules.
- **The decline record.** After an uninstall, Claude Code writes the host's own decline record (`declinedPlugins`) in the user's host configuration. An explicit install still works, but a project that asks for the plugin may show no prompt.
- **Version caching.** Both hosts cache an installed plugin by its version. A version published twice reaches users as the stale copy.

After this ticket:

1. **`skills/johnny-project-takeover/SKILL.md`, a new first start step.**
   - Under `## Start`, a new step 1 goes before today's step 1. The old steps 1 to 5 become steps 2 to 6, and their text does not change.
   - The new step is exactly:
     "1. Before anything else, look at the skills this session lists. If a skill of the old plugin johnny-ai-skill is listed beside this plugin's skills, stop: tell the user in plain words that the old 0.4.x plugin is still installed and that its rules conflict with this version, give the removal commands of README section 5 for the host in use, and do nothing else until the user says it is removed."
   - The step holds no path token in backticks.
   - Today's step 1 links `../../AGENTS.md#read-only-lookup`. That link stays.
2. **README section 5 (從舊版 johnny-ai-skill 換過來).**
   - After its first paragraph, this paragraph is added exactly:
     "新舊兩版同時裝著時，新版開工的第一步會停下來，請你先移除舊版；移除之前它不會做任何事。"
   - After the Codex block, this paragraph is added exactly:
     "用 uninstall 移除插件後，Claude Code 會在它自己的設定裡記下「已拒絕」這個插件。這筆紀錄不會擋住之後明確的安裝；如果某個專案要求安裝這個插件卻沒有跳出提示，直接執行第 3 節的安裝指令即可。"
   - Neither paragraph holds inline code, a path, or a link.
3. **`doc/runbooks/release.md`, new.** It holds these sections:
   - **The rule.** It is stated exactly: "A version number is never published twice. Once tag `plugin-vX.Y.Z` is pushed to the publication repository, any change ships as a new version. Before a publish, the publication repository has no tag for the new version, and the plugin `version` is above the last pushed one."
   - **The order.** It cites, without restating it, ticket 71's release section as amended by ticket 80's 正式環境移植 SOP and by the REQ-043 decisions of 2026-11-26. Each push waits for the owner's confirmation.
   - **Before release.** One sentence: the local candidate may be rebuilt under the same unreleased version, and every rebuild is reinstalled as ticket 80 item 5 says.
4. **Tests.**
   - `tests/test_entry_read_only_lookup.py`: `START_STEPS` takes the new step 1 and the renumbered steps. A new injection case checks that the guard step removed, or moved after the read-only step, turns the test red.
   - `tests/test_plugin_payload_boundary.py`: a check that README section 5 holds both paragraphs word for word.
5. **The rebuilt publication commit.** `SKILL.md` and `README.md` are in the payload, so the publication commit changes.
   - Rebuild it exactly as ticket 80 item 5 says, through these steps: the temporary ref `refs/heads/publication-0.5.0-t81`, the OLD check, `update-ref` with OLD, then deleting the temporary ref.
   - OLD is the commit ticket 80 recorded.
   - The eight registered reasons name the new id.
   - Run `--verify-only`.
   - Check the extracted package. It holds the new step and both paragraphs.
   - Rebuild the local marketplace's plugin tree.
   - The STATEMENT gives the owner's refresh commands and cache checks, as ticket 80 item 5 does, with the line to look for in the cached `SKILL.md` being the new step 1.
6. **`doc/HARNESS-CHANGELOG.md`.**
   - Directly below the ticket 80 row: `| 2026-11-26 | The skill stops when the old plugin johnny-ai-skill is still installed; the README explains the host's decline record; a version is never published twice (ticket 81) | `REQ-20261103-043`, owner decisions 2026-11-26 | `modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md` |`.
   - In the `## 0.5.0` section, as the last bullet of the part about moving from `johnny-ai-skill`: `- With both plugins installed, the new skill stops at its first step until the old one is removed.`

**After review approval and integration, control-plane and owner work, not this seat's:**
1. Ticket 77 goes to revision04 with the relaxed rules of the 2026-11-26 decision:
   - the host's decline record is in the residue allow-list, with its reason;
   - `@builtin` entries are not counted;
   - a reinstall succeeds while the record is present.
   Its local lifecycle then reruns with this ticket's publication commit.
2. **The owner-assisted test** adds the two-versions case: with `johnny-ai-skill` 0.4.14 and `software-factory` 0.5.0 both installed, the session stops at the new step 1 and gives the removal commands.

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
