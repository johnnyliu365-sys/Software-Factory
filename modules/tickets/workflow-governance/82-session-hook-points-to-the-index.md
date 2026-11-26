# 82｜The plugin ships a SessionStart hook that tells every session where its rules are and that a read-only lookup starts at the 流程索引; the 0.5.0 publication commit is rebuilt

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner finding and decision 2026-11-26 "A 0.5.0 加插件 hook"） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision06 / receipt under `.worktrees/82-hook-out/` / owner implementation seat / worktree `.worktrees/82-hook` / branch `cp/wave3-82-hook` / baseline the `cp/wave3` commit named in the dispatch |
| 實作語言 | JSON and Markdown; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `IN_PROGRESS`; dispatch=sha256:5c60d9a305ab3f107cee8abd93e15e33ed93a9cf9c608c8d8cb118abbd5b3208 (`doc/handoffs/2026/workflow-governance/dispatch/JAS-82-2.yaml`)（revision06; strict tier; rule-only review of revision01 CHANGES_REQUESTED; revision02 applies the reviewer's exact fixes and the owner's answer "接受" on the scope (S82R-02); the initial review of revision02 APPROVED `bea29f4b`; revision03 adds the old-plugin guard to the hook text by owner decision 2026-11-26 "放進 hook", and says the terminal for /hooks; revision04 applies the exact fixes of the revision03 delta review (S82R-12 to S82R-18); revision05 adds item 4b, the Codex trust sentence, from the owner finding of 2026-11-26, and item 4c, the install-scope sentence of README section 5, by owner decision 2026-11-26 "併進票 82"; revision06 applies the exact fixes of the revision05 delta review (S82R-19 to S82R-25)） |
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

**Revision03.** The owner retested `838bb354`. The hook ran, and both lookups went through the 流程索引 with no search. With `johnny-ai-skill` also installed, a plain question did not trigger ticket 81's guard, which sits in `SKILL.md`, and the owner said "舊版裝了／他沒有叫我刪". The owner decided "放進 hook" (REQ-043 row "Owner finding and decision 2026-11-26 (the old-plugin guard also goes into the hook, "放進 hook")"). The hook text gains the guard sentence, and the `SKILL.md` guard stays as a second line. Because `/hooks` does not exist in the desktop app, the README sentence names the terminal. Revision03 is carried by additive commits on the same branch; OLD for its rebuild is `838bb3540960f1cbb3a086c411136766235277d5`, the id revision02 recorded in G1. On the branch, revision03 replaces in place the revision02 command in `hooks/hooks.json` and in the tests, the README section 8 sentence, the changelog row of item 7 and its `What to read instead` bullet; none of them is added a second time. The seat reads this revision from the `cp/wave3` commit named in the correction dispatch (`git show <commit>:modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md`); the copy in its worktree stays at revision02 and is not edited.

**Scope against the decision.** Option A said each session receives the 流程索引, the read-only-lookup paragraph and the installed plugin path (about 2 to 3 KB). This ticket injects only the path and the first step (about 0.4 KB; with the old-plugin sentence of revision03, 777 printed characters), in ASCII. When Git Bash is missing, the command runs in Windows PowerShell 5.1, which does not print UTF-8 text reliably, and a second copy of the index would drift from `AGENTS.md`. The session reads the paragraph and the index from the file. Codex is tested in the owner-assisted test, not before this ticket. The owner accepted this ("接受", row "Owner decision 2026-11-26 (ticket 82 scope, "接受")" of `REQ-20261103-043`).

**Facts this ticket relies on.** These are from the Claude Code plugin documentation (`code.claude.com/docs/en/plugins/components.md`, `manifest-reference.md`, `hooks.md`):
- A plugin's hooks live in `hooks/hooks.json` at the plugin root, under a top-level `"hooks"` key.
- `${CLAUDE_PLUGIN_ROOT}` is substituted anywhere in the command with the installed plugin directory: with forward slashes when Git Bash runs it, with native backslashes when PowerShell runs it.
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
               "command": "echo \"Software Factory plugin: its rules are in ${CLAUDE_PLUGIN_ROOT}/AGENTS.md. To answer a read-only question about one of those rules, read that file: its paragraph at the anchor read-only-lookup says how, and its table at the anchor process-index gives the one row and the one section to read. Do not locate a rule with grep, a full-text search or by browsing files. If this session also lists a skill whose name begins with johnny-ai-skill: or whose file lies in a folder named johnny-ai-skill, then before anything else tell the user that the old 0.4.x plugin is still installed and conflicts with this version, give the removal commands in section 5 of ${CLAUDE_PLUGIN_ROOT}/README.md, ask the user to open a new session after removing it, and do nothing else in this session.\""
             }
           ]
         }
       ]
     }
   }
   ```

   - **The command is ASCII only.** It works the same in Git Bash and in PowerShell: `echo` is a command in both, the path is substituted before the shell runs, and the text is inside one pair of double quotes in both shells.
   - **No matcher,** so the hook also fires after `resume`, `clear` and `compact`.
2. **`.claude-plugin/plugin.json`.** The `payload.files` list gains the line `      "hooks/hooks.json",` directly after the line `      "Workflow.md",`. `payload.trees` does not change, so no other file under `hooks/` ships. No other line changes.
3. **`AGENTS.md`.** The anchor `<a id="process-index"></a>` goes directly above `## 流程索引`. It stands on its own line, with a blank line before it and after it, as `p0-source-type` does. No other line changes.
4. **README section 8 (它怎麼運作).** This sentence is added at the end of the section, exactly, as its own paragraph:

   "每次開新的 session，插件會用一個 SessionStart hook 告訴 agent 規則檔在哪裡、查本插件規則的唯讀查詢要先查流程索引，以及舊版 johnny-ai-skill 還裝著時要先停下來；在 Claude Code 終端機裡輸入 /hooks 可以看到它。"

   It holds no inline code, no path and no link.
4b. **README section 4 (安裝：Codex), revision05.** Directly after the fenced block `codex plugin list --marketplace software-factory --json` and before the line that begins `5. 要移除時`, with one blank line on each side, this paragraph is added exactly:

   "安裝或更新 Software Factory 之後開 Codex 時，如果它詢問是否信任 Software Factory 的 hook，請選信任。沒有信任的話，Codex 開場時不會知道插件的規則檔在哪裡，查規則時可能改用搜尋，也不會在舊版還裝著時先停下來。"

   It holds no inline code, no path and no link, and the numbered steps do not change. The new test file checks that section 4 holds it exactly once at that place, and TDD 2 gains the case "the Codex trust paragraph removed". Item 7's row already holds "; README section 4 tells a Codex user to trust the hook"; it is not added again.

4c. **README section 5, revision05.** Directly after the fenced block `claude plugin marketplace remove johnny-ai-skill` and before the line `Codex：`, with one blank line on each side, this paragraph is added exactly:

   "上面的 uninstall 指令針對裝在 user 範圍的舊版（0.4.x 的 README 就是這樣教的）。如果當初裝在 project 或 local 範圍，請到那個專案的資料夾裡執行上面兩個指令，並把 uninstall 的 --scope user 換成 --scope project 或 --scope local。"

   It holds no inline code, no path and no link. The two paragraphs of section 5 that ticket 81 pins do not change. The new test file checks the paragraph exactly once at that place, and TDD 2 gains the case "the scope paragraph removed". Item 7's row already holds "; README section 5 names the other install scopes"; it is not added again.

5. **Tests.**
   - **New `tests/test_plugin_session_hook.py`:**
     - `hooks/hooks.json` parses and equals item 1;
     - its command holds only ASCII;
     - each anchor it names stands exactly once in `AGENTS.md`: `read-only-lookup`, and `process-index` directly above `## 流程索引`;
     - the payload declaration lists `hooks/hooks.json`, and `materialise_publication_tree(<repository root>, <payload>, <temporary directory>)` writes `hooks/hooks.json` with the same bytes as the repository's file (the pinned commit is checked by K1, not by this test);
     - README section `## 8. 它怎麼運作` holds the sentence of item 4 exactly once, as its own paragraph and as the section's last paragraph;
     - README section `## 4. 安裝：Codex` holds the paragraph of item 4b exactly once; the three lines before it are `codex plugin list --marketplace software-factory --json`, ```` ``` ```` and a blank line, and the two lines after it are a blank line and a line that begins `5. 要移除時`;
     - README section `## 5. 從舊版 johnny-ai-skill 換過來` holds the paragraph of item 4c exactly once; the three lines before it are `claude plugin marketplace remove johnny-ai-skill`, ```` ``` ```` and a blank line, and the two lines after it are a blank line and the line `Codex：`;
     - neither paragraph holds `` ` ``, `](`, `/` or `\`;
     - the old-plugin sentence of the command holds the two match conditions of `SKILL.md` step 1 word for word: `name begins with johnny-ai-skill:` and `file lies in a folder named johnny-ai-skill` each stand exactly once in the command and once in the line of `skills/johnny-project-takeover/SKILL.md` that begins `1. Before anything else`;
     - with `${CLAUDE_PLUGIN_ROOT}` replaced by a temporary directory (forward slashes for bash, native separators for PowerShell), the command is run and must exit 0, write nothing to stderr, and print the expected text with that path followed by one line feed, after its stdout is decoded as UTF-8 and each CRLF is replaced by LF. The bash case runs `shutil.which("bash")` on Linux. On Windows it runs the file named by `CLAUDE_CODE_GIT_BASH_PATH` when that variable is set, otherwise `C:\Program Files\Git\bin\bash.exe`, and never a bare `bash`. It is skipped with the reason `Git Bash not found` when that file does not exist. On Windows only, the PowerShell case runs `[shutil.which("powershell"), "-NoProfile", "-NonInteractive", "-Command", command]`, and is skipped with the reason `Windows PowerShell not found` when `shutil.which("powershell")` is None.
   - `tests/test_entry_read_only_lookup.py`: `ANCHORED_HEADINGS` gains `("process-index", "## 流程索引")` between the `p0-permissions` and `target-sources` entries, and the module docstring's "three anchors" sentence gains "; ticket 82 adds `process-index` above `## 流程索引`".
   - `tests/test_plugin_payload_boundary.py`: `PayloadDeclarationTests` gains `def test_the_session_hook_is_carried(self) -> None:`, asserting `"hooks/hooks.json"` is in `_payload_entries(self.payload, "files")` and `"hooks"` is not in `_payload_entries(self.payload, "trees")`.
6. **The rebuilt publication commit.** It is rebuilt exactly as ticket 80 item 5 says:
   - with the temporary ref `refs/heads/publication-0.5.0-t82`;
   - OLD is `6d04fa6d0cf0c1e7134a312894adc219f44bf4a9` in the first round; in a correction round it is the id the previous round of this ticket recorded in G1; `git rev-parse refs/heads/publication-0.5.0` must print OLD, otherwise HALT;
   - `update-ref` with OLD, then the temporary ref is deleted;
   - each of the eight occurrences of OLD in `ci/registered-failures.json` becomes the new id;
   - `--verify-only` is run;
   - the extracted package holds `hooks/hooks.json` and the anchor;
   - the local marketplace's plugin tree is rebuilt;
   - the STATEMENT gives the owner's refresh commands. The cache check looks, in each host's `0.5.0` cache folder, for `README.md` holding a line that begins `上面的 uninstall 指令針對裝在 user 範圍的舊版`. A cache without that line holds an earlier build (`9cda3f9e` already ships the hook with the old-plugin sentence), so that host was not refreshed; the owner removes that host's `0.5.0` cache folder and installs again.
   - If this ticket is closed without integration, the control plane runs `git update-ref refs/heads/publication-0.5.0 6d04fa6d0cf0c1e7134a312894adc219f44bf4a9 <the id on the ref>`.
7. **`doc/HARNESS-CHANGELOG.md`.**
   - Directly below the ticket 81 row, replacing the revision02 row of ticket 82: `| 2026-11-26 | The plugin ships a SessionStart hook that names its rules file, sends a read-only lookup to the 流程索引 first, and stops a session that also lists the old plugin johnny-ai-skill; README section 4 tells a Codex user to trust the hook; README section 5 names the other install scopes (ticket 82) | `REQ-20261103-043`, owner decisions 2026-11-26 "A", "放進 hook" and "併進票 82" | `modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md` |`.
   - In `## 0.5.0`, replacing the revision02 bullet, as the last bullet of `### What to read instead`: `- Each session receives, from the plugin's SessionStart hook, the path of its rules file, the instruction to start a lookup at the 流程索引, and the instruction to stop when the old plugin johnny-ai-skill is also listed.`

**After review approval and integration, control-plane and owner work, not this seat's:**
1. Rerun ticket 77's local lifecycle at the integration commit with `--expected-publication` set to this ticket's commit, and add it to ticket 77's record.
2. **The owner-assisted test** records:
   - whether the hook's text reaches a desktop session, and whether `/hooks` in the Claude Code terminal lists the hook;
   - the same P0 and PRD questions, with the files the session read. The expected route is the 流程索引, then the one linked section, with no search;
   - whether Codex, once the hook is trusted as README section 4 says, prints the hook text with its installed plugin directory as the path (REQ-043 row "Owner finding 2026-11-26 (Codex asks to trust the plugin hook)" records that it ran on `838bb354`), and whether the two-versions case stops in Codex too;
   - the two-versions case of ticket 81, asked as a plain question without invoking the skill: the expected answer is the stop, the removal commands from README section 5, and nothing else.
3. Ticket 77's cloud trigger passes `expected_publication` equal to this ticket's publication commit.
4. Repin the `agents` row of `doc/handoffs/2026/workflow-governance/control-plane-worklog.md` and run `index_pins.py --check`.

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
   - the README sentence removed;
   - the old-plugin sentence removed from the command;
   - the Codex trust paragraph removed;
   - the scope paragraph removed.
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
