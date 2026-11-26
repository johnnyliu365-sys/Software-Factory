# 82｜The plugin ships a SessionStart hook that tells every session where its rules are and that a read-only lookup starts at the 流程索引; the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner finding and decision 2026-11-26 "A 0.5.0 加插件 hook"） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision01 / receipt under `.worktrees/82-hook-out/` / owner implementation seat / worktree `.worktrees/82-hook` / branch `cp/wave3-82-hook` / baseline the `cp/wave3` commit named in the dispatch |
| 實作語言 | JSON and Markdown; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `PLANNED`（revision01; strict tier; rule-only review before dispatch） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/82-hook` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/82-hook-review` |
| 責任邊界 | a new `hooks/hooks.json`, the payload declaration of `plugin.json`, one anchor in `AGENTS.md`, one README sentence, the tests that pin them, and the marketplace pin, the registered-failure reasons and the changelog for the rebuilt publication commit |
| 禁止修改 | every other line of `AGENTS.md` and `plugin.json`; `Workflow.md`, `CodeReview.md`, `skills/`, `library/`, `commands/`, `template/`, `ci/acceptance/`, `.github/` |
| 環境 | `LOCAL` and GitHub Actions on the development repository; nothing is pushed to the publication repository |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
create = hooks/hooks.json
create = tests/test_plugin_session_hook.py
modify = .claude-plugin/plugin.json
modify = AGENTS.md
modify = README.md
modify = tests/test_entry_read_only_lookup.py
modify = tests/test_plugin_payload_boundary.py
modify = .claude-plugin/marketplace.json
modify = ci/registered-failures.json
modify = doc/HARNESS-CHANGELOG.md
forbid = Workflow.md
forbid = CodeReview.md
forbid = skills/
forbid = library/
forbid = commands/
forbid = template/
forbid = ci/acceptance/
forbid = .github/
```

## 使用者拍板與可觀察結果

Process tier: strict.

**The problem.** The decision is quoted in `REQ-20261103-043`, row "Owner finding and decision 2026-11-26 (the written lookup rule is not followed; the plugin ships a hook, "A")". In the owner's retest of the final candidate (`6d04fa6d`), a read-only lookup still located the rule by keyword search. The agent does not know where the installed plugin's `AGENTS.md` is, so it searches for the rule that forbids searching. Only a mechanism fixes that: the host must put the location and the first step in front of every session.

**Facts this ticket relies on.** These are from the Claude Code plugin documentation (`code.claude.com/docs/en/plugins/components.md`, `manifest-reference.md`, `hooks.md`):
- A plugin's hooks live in `hooks/hooks.json` at the plugin root, under a top-level `"hooks"` key.
- `${CLAUDE_PLUGIN_ROOT}` is substituted in the command with the installed plugin directory, using forward slashes in shell form.
- A SessionStart hook's plain stdout, with exit 0, becomes context the model sees, capped at 10,000 characters.
- With no matcher, the hook fires on `startup`, `resume`, `clear`, `compact` and `fork`.
- On Windows a command runs in Git Bash, or in PowerShell when Git Bash is missing.

After this ticket:

1. **`hooks/hooks.json`, new.** It is exactly:

   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "echo \"Software Factory plugin: its rules are in ${CLAUDE_PLUGIN_ROOT}/AGENTS.md. For a read-only question (the content of a document, the state of a ticket, the wording of a rule), open that file at the anchor process-index, take the one row that fits the question, and read only the section that row links. Do not locate a rule with grep, a full-text search or by browsing files.\""
             }
           ]
         }
       ]
     }
   }
   ```

   - **The command is ASCII only.** It works the same in Git Bash and in PowerShell: `echo` is a command in both, and the path is substituted before the shell runs.
   - **No matcher,** so the hook also fires after `resume`, `clear` and `compact`.
2. **`.claude-plugin/plugin.json`.** The `payload` declaration gains `hooks/hooks.json`, in the form its other entries use. No other field changes.
3. **`AGENTS.md`.** The anchor `<a id="process-index"></a>` goes directly above `## 流程索引`. It stands on its own line, with a blank line before it and after it, as `p0-source-type` does. No other line changes.
4. **README section 8 (它怎麼運作).** This sentence is added at the end of the section, exactly, as its own paragraph:

   "每次開新的 session，插件會用一個 SessionStart hook 告訴 agent 規則檔在哪裡，以及唯讀查詢要先查流程索引；在 Claude Code 裡輸入 /hooks 可以看到它。"

   It holds no inline code, no path and no link.
5. **Tests.**
   - **New `tests/test_plugin_session_hook.py`:**
     - `hooks/hooks.json` parses and equals item 1;
     - its command holds only ASCII;
     - the anchor it names (`process-index`) stands exactly once in `AGENTS.md`, directly above `## 流程索引`;
     - the payload declaration lists `hooks/hooks.json`, and the extracted publication tree holds it;
     - with `${CLAUDE_PLUGIN_ROOT}` replaced by a temporary directory, the command run through `bash -c` prints exactly the expected text with that path, and exits 0. On Windows the test also runs it through `powershell -NoProfile -Command` and expects the same text. A case that needs a shell the runner lacks is skipped, and the skip names the shell.
   - `tests/test_entry_read_only_lookup.py`: the anchor checks include `process-index`.
   - `tests/test_plugin_payload_boundary.py`: the expected payload takes `hooks/hooks.json`.
6. **The rebuilt publication commit.** It is rebuilt exactly as ticket 80 item 5 says:
   - with the temporary ref `refs/heads/publication-0.5.0-t82`;
   - OLD is `6d04fa6d0cf0c1e7134a312894adc219f44bf4a9`; `git rev-parse refs/heads/publication-0.5.0` must print OLD, otherwise HALT;
   - `update-ref` with OLD, then the temporary ref is deleted;
   - each of the eight occurrences of OLD in `ci/registered-failures.json` becomes the new id;
   - `--verify-only` is run;
   - the extracted package holds `hooks/hooks.json` and the anchor;
   - the local marketplace's plugin tree is rebuilt;
   - the STATEMENT gives the owner's refresh commands. The cache check looks for `hooks/hooks.json` in each host's `0.5.0` cache folder.
   - If this ticket is closed without integration, the control plane runs `git update-ref refs/heads/publication-0.5.0 6d04fa6d0cf0c1e7134a312894adc219f44bf4a9 <the id on the ref>`.
7. **`doc/HARNESS-CHANGELOG.md`.**
   - Directly below the ticket 81 row: `| 2026-11-26 | The plugin ships a SessionStart hook that names its rules file and sends a read-only lookup to the 流程索引 first (ticket 82) | `REQ-20261103-043`, owner decision 2026-11-26 "A" | `modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md` |`.
   - In `## 0.5.0`, as the last bullet of `### What to read instead`: `- Each session receives, from the plugin's SessionStart hook, the path of its rules file and the instruction to start a lookup at the 流程索引.`

**After review approval and integration, control-plane and owner work, not this seat's:**
1. Rerun ticket 77's local lifecycle at the integration commit with `--expected-publication` set to this ticket's commit, and add it to ticket 77's record.
2. **The owner-assisted test** records:
   - whether a desktop session in the test project shows the hook (in `/hooks`) and its text;
   - the same P0 and PRD questions, with the files the session read. The expected route is the 流程索引, then the one linked section, with no search;
   - whether Codex runs the plugin's hook. Codex 0.166.0 has hooks that need persisted trust. If it does not run it, README section 4 gains a sentence in a later ticket, and wave 4 T3 takes the Codex path;
   - the two-versions case of ticket 81.
3. Ticket 77's cloud trigger passes `expected_publication` equal to this ticket's publication commit.

## 實作範圍、依賴與 ticket elements

### 角色指派（必填）

- 流程／Grill／ticket owner：control plane.
- implementation owner：`implementation-standard` seat in `.worktrees/82-hook`.
- reviewer：`ticket-review` seat in `.worktrees/82-hook-review`.
- **Owner override record**：N/A.
- `ImplementationHandoff`：this ticket; ticket 80 item 5 (the rebuild procedure); ticket 81 (the current `AGENTS.md`, README and tests).
- `ImplementationReturn`：`COMPLETED → ACTION_COMPLETED`／`BLOCKED → HALT`／`CHANGE_DETECTED → REQUIREMENT_CHANGED → Grill`。A test outside the boundary that breaks is a `CHANGE_DETECTED` return naming the test. A shell that prints the hook text differently is a `CHANGE_DETECTED` return with the output.

### 前端組合與依賴注入

**N/A reason**：a hook declaration, governance text and tests; no UI boundary.

- element 路徑：不適用
- 實際原始碼路徑：the paths in the boundary block
- 公開契約／資料模型：the hook command text above.

## TDD 設計

1. 正常行為：`hooks/hooks.json` equals item 1, and running its command prints the expected text with the substituted path.
2. 規則違反／輸入錯誤, each turning a named test red:
   - `hooks/hooks.json` removed from the payload;
   - a non-ASCII character in the command;
   - a matcher added;
   - the anchor `process-index` removed or moved below `## 流程索引`;
   - the command text changed by one word;
   - the README sentence removed.
3. 外部失敗／fail-closed：a missing or unparsable `hooks/hooks.json` is a named defect, not a traceback.
4. 回歸保護：every check of tickets 79, 80 and 81 still passes; `--verify-only` passes with the new pin.

### 適用的缺陷類別

| # | 類別 | 是否適用 | 本工單的必要案例 |
| --- | --- | --- | --- |
| 1 | 路徑前綴誤匹配 | 是 | an anchor `process-index-x` does not satisfy `process-index` |
| 2 | null／空字串／陣列 | 是 | an empty `SessionStart` list; an empty command |
| 3 | 權限繞過 | 是 | the hook only prints text: it reads no file, runs no other program, and needs no network or secret |
| 4 | Token 格式與比較 | 是 | the hook file and the command compared exactly; the pin as 40 lower-case hex |
| 5 | 錯誤碼是否一致 | 否 | no exit codes change |
| 6 | 例外是否會拋出 | 是 | a missing hook file is a named defect |

## 完成定義與證據

- `python -m pytest tests/test_plugin_session_hook.py tests/test_entry_read_only_lookup.py tests/test_plugin_payload_boundary.py tests/test_plugin_publication.py tests/test_governance_consistency.py -q` exits 0 on the host, with the local anchor ref, apart from registered base failures. `mypy --strict` on the new and changed test files exits 0.
- **G1**, **V1**, **K1** and **L1**, as ticket 80 defines them.
- **A1**: `git diff --unified=0 <baseline> <candidate> -- AGENTS.md .claude-plugin/plugin.json` shows only the anchor lines and the payload entry.
- **反向突變證據**: every case of TDD 2, each restored after it turns a named test red.
- **CI evidence**: one run on a commit of this branch with both jobs `success`. The PowerShell case runs on the Windows job.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The release follows `doc/runbooks/release.md`, with this ticket's publication commit in place of ticket 81's. Each push waits for the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
