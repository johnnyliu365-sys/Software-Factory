# Acceptance of 0.5.0: record

Ticket: `modules/tickets/workflow-governance/77-acceptance-0-5-0.md` (revision04). The script is `ci/acceptance/lifecycle.py`, its rules and allow-lists are in `ci/acceptance/README.md`. This record starts with the local run. The control plane adds the cloud run and the owner-assisted Codex session below.

## The local run

Seat: `implementation-standard`, run id `jas77-r3`. Both run roots were new empty directories under `C:/Temp/claude/`, outside every Git work tree. The commands are the ones in `ci/acceptance/README.md`; the raw `report.jsonl` of each run is the raw block of the receipt's cells L1 and L2.

Host CLI versions, as read by the script with `--version`, against the pins of `ci/acceptance/README.md`. The local run uses the host's own `claude` and `codex`, first on `PATH`, with no copied binary:

| Host | Run with | Pinned | Same |
| --- | --- | --- | --- |
| claude | 2.1.332 (Claude Code) | 2.1.332 | yes |
| codex | codex-cli 0.166.0 | 0.166.0 | yes |

The pin of Claude Code moved from 2.1.316 to 2.1.332, because the host's `claude` updated itself between two dispatches and real users run the newest host (owner decision of 2026-11-26, "放寬"). Under 2.1.332 two host behaviours differ from 2.1.316, and the rules now accept both versions:

- After `plugin uninstall`, `.claude.json` holds `"declinedPlugins": ["software-factory@software-factory"]`, the host's own decline record. The allow-list admits the value of that one top-level key and nothing else of the file. Any other key or line of `.claude.json` that names `software-factory` is `FAIL`. The `uninstall` step then adds the good marketplace and installs again with the record present; it exits 0 and the list shows `0.5.0`, installed and enabled. The plugin never edits the user's host configuration.
- `plugin list --json` lists the host's `@builtin` plugins (`cc-plugin-agents-md`, `cc-plugin-plugin-authoring`, `cc-plugin-privacy` and `cc-plugin-telemetry`). The exactly-one-entry rule of `recover` counts the entries outside them.

With 2.1.316 (revision03's run, with a copy of the host's `versions/2.1.316`) every step also passed: neither behaviour appears there.

### Run 1: `--host both --steps build,fresh,upgrade,uninstall,recover,level2` (condition 3)

The run exits 0 with every verdict `PASS`:

| Step | Host | Verdict |
| --- | --- | --- |
| build | none | PASS |
| fresh | claude | PASS |
| fresh | codex | PASS |
| upgrade | claude | PASS |
| upgrade | codex | PASS |
| uninstall | claude | PASS |
| uninstall | codex | PASS |
| recover | claude | PASS |
| recover | codex | PASS |
| level2 | none | PASS |

The lines come from a run at commit `8bb57b56`. The candidate of the receipt has the same `lifecycle.py`; it differs by this record only. The receipt's cells L1 and L2 are the same two runs repeated at the candidate, with the same verdicts.

The Codex half of `upgrade` (owner decision of 2026-11-26, "A"): Codex honours the forty-zero `sha` of the public 0.4.14 marketplace and refuses it (`git checkout 0000…0000 failed`, found by revision02's run). The step now writes `<step>/marketplace-0414/.claude-plugin/marketplace.json` byte for byte from `git show 01b810f096b1201005d26922e2c8a474bdd5a0a0:.claude-plugin/marketplace.json`, adds that directory with `codex plugin marketplace add`, installs `johnny-ai-skill@johnny-ai-skill`, and reads `git rev-parse HEAD` in the installed directory: `0b3afd3645946f97662c336f0e6ac0dcae502e69`. The list shows `0.4.14` installed and enabled. After the removal and the local install, the list shows only `software-factory` `0.5.0` and the marketplace list has no `johnny-ai-skill`. For Claude Code the step reads the public marketplace at `01b810f0` and finds the same commit in `installed_plugins.json`.

### Run 2: `--host codex --steps build,codex-ref,codex-files`

| Step | Verdict | Evidence |
| --- | --- | --- |
| build | PASS | the regenerated publication commit equals the expected `d355b4a2…` |
| codex-ref | NOT_SUPPORTED | `codex plugin marketplace add file:///…/remote.git --ref marketplace` exits 1: `Error: invalid marketplace source format; expected owner/repo, a git URL, or a local marketplace path`. The check moves to release step 8 of ticket 71. |
| codex-files | PASS | see the table below |

`codex-files`, Codex 0.166.0, each marketplace added, installed from, listed, and removed:

| Marketplace | `marketplace add` | `plugin add` | Version listed |
| --- | --- | --- | --- |
| both files, versions 0.5.0 (`.claude-plugin`) and 0.5.1 (`.agents/plugins`) | 0 | 0 | 0.5.1 |
| only `.claude-plugin/marketplace.json` | 0 | 0 | 0.5.0 |
| only `.agents/plugins/marketplace.json` | 0 | 0 | 0.5.0 |

When both files exist, Codex reads `.agents/plugins/marketplace.json`. Each file alone works, so the local marketplace of ticket 71 item 8 is valid for Codex under either.

## What the run settled

- **Ticket 71 item 8, first check: the Claude marketplace flow.** `claude plugin marketplace add <directory>`, `install --scope user`, `update --scope user` and `uninstall --scope user` all exit 0 on the local marketplace. `claude plugin list --json` exists and shows `software-factory@software-factory`, `0.5.0`, `enabled: true`. `update` answers that the plugin is read from its folder and has nothing to update, and exits 0.
- **Second check: which Codex file is read, and its schema.** Both schemas load; the `.agents` file wins when both exist (above).
- **Third check: `--ref` with a `url`+`sha` source in the same repository.** Not testable by `file://` on 0.166.0 (above). That Codex honours `sha` is settled by the `upgrade` step: it checked out the pin it was given.
- **recover.** For Claude Code, `marketplace add` of a marketplace whose plugin source is a missing directory exits 0 and `install` exits 1 (`Source path does not exist`). For Codex, `marketplace add` exits 0 and `plugin add` exits 1 (`plugin source path is not a directory`). After the README's uninstall and marketplace remove, the good marketplace installs and the list shows exactly one entry outside the host's `@builtin` plugins, `software-factory@software-factory` `0.5.0`.
- **uninstall.** After the README's two commands, the names `software-factory` left under the step directory are the plugin's own cache (for Claude Code `plugins/cache/software-factory`, the version directory carries an `.orphaned_at` marker; for Codex the empty directory `plugins/cache/software-factory`) and, under Claude Code 2.1.332, the value of `declinedPlugins` in `.claude.json`. These are the three entries of the allow-list. A reinstall with the record present succeeds.
- **level2.** Both 0.4.9 assets match the approved sha256 values. `johnny-install.cmd` runs with the step directory as its working directory and the wrapper passed by absolute path, and exits 0 with `INSTALL` answered on standard input into the empty `<step>/root`. The runtime's own `uninstall` reports `{"status": "REMOVED", "removed": ["PLUGIN_PAYLOAD", "VENV", "LAUNCHER", "QUEUE", "TELEMETRY"], "root_deleted": true}`, so `JOHNNY_ROOT` holds no file and the Level 2 allow-list is empty. The environment is the allow-list, `HOME=<step>/home`, `JOHNNY_ROOT`, and no `USERPROFILE` (the `py` launcher exits 109 under any other value).

## Not tested

Run 1 of the acceptance workflow stopped at `build`, before any of the following. Run 2 (section "The cloud run") passed all ten verdicts on the runner, so the three items below are now tested there. On a runner, `py -3.11` with the `level2` environment, `claude` and `codex` from `npm install --global` on `PATH`, and the `.cmd` shims of the npm packages are untested.

## The cloud run

**The development `main`.** The owner fast-forwarded `main` from `74b658e8` to `f1d04039a10539fb8353d3374faf030054a4f672` on 2026-11-26T15:32:55Z. CI run 45850194264 on that commit ended `success` on both jobs, `test (linux)` and `test (windows)`.

**Run 1, 2026-11-27: FAIL at `build`.** The owner confirmed the trigger in words ("跑"). The control plane first read back the remote `main` (`f1d04039`) and the local ref `refs/heads/publication-0.5.0` (`e08e82d3373547a5448040638fb22b1810dc9cf3`).

- Run id 45920193720, `workflow_dispatch` on `main`, head `f1d04039a10539fb8353d3374faf030054a4f672`, started 2026-11-27T01:01:57Z, ended 01:02:38Z, conclusion `failure`.
- Inputs: `candidate=f1d04039a10539fb8353d3374faf030054a4f672`, `expected_publication=e08e82d3373547a5448040638fb22b1810dc9cf3`.
- Artifact `acceptance-report` (`report.jsonl`, ten lines). `build` is `FAIL`; the other nine verdicts are `FAIL: not run, because build did not pass in this run`.
- The `build` step cloned the repository and checked out the candidate (both exit 0). The publication generator then exited 1 with `ModuleNotFoundError: No module named 'pydantic'`, raised by `library/local_orchestration/contracts.py` line 8.
- **Cause.** `.github/workflows/acceptance.yml` installs the two host CLIs and no Python package. The generator imports `library.local_orchestration`, which needs `pydantic` (`requirements-dev.txt`). `ci.yml` has the step `python -m pip install -r requirements-dev.txt`; the acceptance workflow has no such step. `ci/acceptance/README.md` says "or any Python 3.11", which is wrong for the `build` step.
- **Why the local runs passed.** Both local interpreters (the test venv and `py -3.11`) already hold `pydantic`. No local run used an interpreter that holds only what the workflow installs.
- **Reproduced locally (2026-11-27).** A new venv from `py -3.11` with no package: the generator with `--verify-only --ref refs/heads/publication-0.5.0` exits 1 with the same `ModuleNotFoundError`. After `pip install -r requirements-dev.txt` into that venv, the same command prints `verified e08e82d3373547a5448040638fb22b1810dc9cf3` and exits 0.
- **What the run did not reach.** No host CLI ran on the runner. Of the items under "Not tested", the parity run below covers the `.cmd` shims of the npm packages on this host. `py -3.11` with the `level2` environment on a runner, and `claude` and `codex` from `npm install --global` on the runner's `PATH`, stay untested.
- **Not rerun.** The fix to the workflow and a second run wait for the owner's decision.

**Parity run (2026-11-27, control plane).** The local runs above used this host's own `claude.exe` and `codex.exe` (`where claude codex` names two `.exe` files outside npm) and interpreters that already held `pydantic`. This run installs the Python packages and the host CLI versions that the workflow installs.

- Candidate `f1d04039a10539fb8353d3374faf030054a4f672`, expected publication `e08e82d3373547a5448040638fb22b1810dc9cf3`, started 2026-11-27T01:07:33Z, ended 01:08:08Z.
- Directories: venv `C:/Temp/claude/acc-clean-venv-20261127`, npm prefix `C:/Temp/claude/acc-parity-npm-20261127`, run root `C:/Temp/claude/acc-parity-run-20261127`.
- Install lines: `py -3.11 -m venv <venv>`; `<venv>/Scripts/python.exe -m pip install -r requirements-dev.txt`; `npm install --prefix <npm prefix> --no-audit --no-fund @anthropic-ai/claude-code@2.1.332 @openai/codex@0.166.0`. The host's npm is 11.16.0 on node 24.18.0; it did not run the `claude-code` package's postinstall script and printed a notice about it.
- Command: `<venv>/Scripts/python.exe ci/acceptance/lifecycle.py --candidate <candidate> --expected-publication <expected> --host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root <run root>`, with `<npm prefix>/node_modules/.bin` first on `PATH`. Exit 0.
- Verdicts, from `report.jsonl`: `build` `PASS`; `fresh`, `upgrade`, `uninstall` and `recover` `PASS` for `claude` and for `codex`; `level2` `PASS`. Ten of ten.
- Resolved commands, from `report.jsonl`: the generator ran as `C:\Temp\claude\acc-clean-venv-20261127\Scripts\python.exe -m library.local_orchestration.plugin_publication` and printed `publication commit e08e82d3373547a5448040638fb22b1810dc9cf3`. Every Claude Code command ran as `C:\Temp\claude\acc-parity-npm-20261127\node_modules\.bin\claude.CMD` (`--version`: `2.1.332 (Claude Code)`), and every Codex command as `…\node_modules\.bin\codex.CMD` (`--version`: `codex-cli 0.166.0`).
- Not covered: `git`, `node`, `npm` and the `py` launcher are this host's. The runner's `py` launcher, which the `level2` step's installer calls, stays untested.

**Ticket 77 revision06.** The fix was integrated at `34583ba2` (the workflow installs `requirements-dev.txt` before the host CLIs; `wave3-integration-2026-11-18.md`, section "Ticket 77 revision06"). The record commit `fe0b12450eac4a1d13ad018df127ccecedf545ea` followed, with CI run 45938394711 `success` on both jobs.

**Parity run at `fe0b1245` (2026-11-27, control plane).** Done as `ci/acceptance/README.md`, section "The parity run", says, with a new venv, a new npm prefix and a new run root under `C:/Temp/claude/` (removed afterwards; the report is kept by the control plane). Started 2026-11-27T04:11:21Z, ended 04:12:05Z, exit 0. Ten of ten verdicts `PASS`. The generator ran under the venv's interpreter, and every host command ran as `claude.CMD` (`2.1.332 (Claude Code)`) or `codex.CMD` (`codex-cli 0.166.0`) under the npm prefix.

**The development `main`, second fast-forward.** The control plane showed the rehearsal (`f1d04039..fe0b1245`) and the command in a runnable block once CI on `fe0b1245` was green (REQ-044 T4 rule (d) as rewritten on 2026-11-27). The owner ran it; the control plane read back `refs/heads/main` as `fe0b12450eac4a1d13ad018df127ccecedf545ea` at 2026-11-27T04:41:28Z.

**Run 2, 2026-11-27: PASS, ten of ten.** The owner started it from a runnable block after the control plane had read back the remote `main`, the install step in `main`'s workflow file and the local publication ref.

- Run id 45941477324, `workflow_dispatch` on `main`, head `fe0b12450eac4a1d13ad018df127ccecedf545ea`, started 2026-11-27T04:42:12Z, ended 04:44:40Z, conclusion `success`. Every step of the job is `success`, the new step `Install development requirements` among them.
- Inputs: `candidate=fe0b12450eac4a1d13ad018df127ccecedf545ea`, `expected_publication=e08e82d3373547a5448040638fb22b1810dc9cf3`.
- Artifact `acceptance-report` (`report.jsonl`, ten lines, sha256 `29eb38c5b9ff0d39946c1e2897311e6d4048054e4b0427772d0afa7b039825ab`). Verdicts: `build` `PASS`; `fresh`, `upgrade`, `uninstall` and `recover` `PASS` for `claude` and for `codex`; `level2` `PASS`.
- `build`: the clone checked out `fe0b1245`, and the generator printed `publication commit e08e82d3373547a5448040638fb22b1810dc9cf3`, the expected one. The runner regenerated the same package from the candidate.
- Resolved commands on the runner: the generator under `C:\hostedtoolcache\windows\Python\3.11.9\x64\python.exe`; the host CLIs as `C:\npm\prefix\claude.CMD` (`2.1.332 (Claude Code)`) and `C:\npm\prefix\codex.CMD` (`codex-cli 0.166.0`), the shims of `npm install --global`.
- `level2`: both 0.4.9 assets matched their approved sha256 values; the install exited 0 and `JOHNNY_ROOT` held 3523 paths; after the uninstall `JOHNNY_ROOT` held no file outside the allow-list. So the runner's `py` launcher works for the 0.4.9 installer.
- Conditions (1) to (4) of `ci/acceptance/README.md` held at the trigger. The acceptance of ticket 77 on a GitHub-hosted Windows runner is met.
- The rule that the cloud run happens once: run 1 failed and run 2 followed the owner decision of 2026-11-27 ("A"). No third run was needed, so decision 2 of that day stays unanswered and unused.

## The owner-assisted Codex session

Not run. The control plane records each step here.

## Control-plane rerun with the final publication commit (2026-11-26)

Tickets 80 and 81 assign this rerun to the control plane, at the first `cp/wave3` commit that holds tickets 77, 80 and 81.

| Field | Value |
| --- | --- |
| Commit | `e87bc5cba1f4313b2db0b6bfd55e5ab6eb10fcc1` (ticket 77 integrated after tickets 80 and 81) |
| Expected publication | `6d04fa6d0cf0c1e7134a312894adc219f44bf4a9` (ticket 81) |
| Command | `python ci/acceptance/lifecycle.py --candidate e87bc5cb… --expected-publication 6d04fa6d… --host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root C:/Temp/claude/cp77-final-L1` |
| Host CLIs | the host's own `claude` 2.1.332 and `codex` 0.166.0, as pinned in `ci/acceptance/README.md` |
| Result | exit 0. Every verdict is `PASS`: build; fresh, upgrade, uninstall and recover on both hosts; level2 |

## Owner-assisted local test of the candidate (2026-11-26)

These are the owner's own sessions on this host, recorded from the owner's screenshots:
- **Codex, local marketplace.** `codex plugin add software-factory@software-factory --json` installed 0.5.0. It went into the owner's default Codex home, not a fresh `CODEX_HOME`.
- **Claude Code, `--plugin-dir`.** Both skills are listed. Their descriptions still say "Johnny's"; that wording is S71R-25, carried to wave 4.
- **Claude desktop, plugin installed with `--scope local` into an empty test project.** The first install landed in the development repository, because the Run button gives each block its own shell. The control plane moved it.
- **Takeover in the empty project.** `/software-factory:johnny-project-takeover` read `SKILL.md` and `delivery-profile.md`. It reported that the project has no `AGENTS.md` or `Workflow.md`, put the project at INTAKE, and named the goal, the authority and the Profile as needed. It returned `WAIT_FOR_HUMAN` and created nothing.
- **Read-only lookup at publication commit `d355b4a2`.** Asked about P0, the session searched with keywords before it read `AGENTS.md` lines 33 to 43. The owner judged that a defect ("流程索引／很重要"), which led to tickets 80 and 81.
- **Retest on `6d04fa6d`.** Still to come: the P0 and target-sources lookups, and two versions installed together.

## Owner-assisted retest with ticket 82's hook (2026-11-26, local candidate `838bb354`)

This test ran in a desktop session in the empty test project, with the plugin installed `--scope local` from the local marketplace:
- **The hook runs in the desktop app.** Asked what it received at session start, the session quoted `SessionStart:startup hook success` and the hook text word for word. The path was `C:/Temp/claude/sf-050-local/plugins/software-factory/AGENTS.md`: a plugin from a local-path marketplace loads in place. `/hooks` is not available in the desktop app, so README section 8's sentence holds for the terminal only.
- **"P0 原始碼型別的規定是什麼？" and "target project 的 PRD 放哪？"** The tool record shows two reads, `AGENTS.md` and `.claude-plugin/plugin.json`, with no grep or search. Both answers went through the 流程索引:
  - P0 to the row 「P0 原始碼型別」 and `#p0-source-type`;
  - PRD to the row 「target project 正式來源的標準位置」 and `#target-sources`. The session also said why the PRD／CHG row does not apply to a "where" question.

  Each answer cited the file, the section and version 0.5.0. The owner's finding of the same day ("流程索引／很重要") is closed in use for Claude Code.
- **Still open:** the two-versions case, and whether Codex runs the plugin's hook.
- **Codex runs the plugin's hook (owner test, 2026-11-26, Codex 0.166.0, local candidate `838bb354`).** In a Codex session in the test project, asked what it received at session start, Codex quoted the hook text word for word. It named the rules file `C:\Users\User\.codex\plugins\cache\software-factory\software-factory\0.5.0\AGENTS.md`. Codex therefore reads `hooks/hooks.json` from a plugin, runs the SessionStart hook, and substitutes `${CLAUDE_PLUGIN_ROOT}` with its own cache path. The rendered answer showed `User.codex`, because the markdown renderer dropped the backslash before `.codex`; the path is right. The release condition of ticket 82 for Codex (S82R-09) holds.
- **The old-plugin guard fires from the hook on a plain question (owner test, 2026-11-26, Claude desktop, local candidate `9cda3f9e`).** With `johnny-ai-skill` 0.4.14 and `software-factory` 0.5.0 both installed `--scope local` in the test project, the owner asked "這個專案目前有什麼？" in a new session and invoked no skill. The session refused to answer. It named the two old skills it saw, gave the README section 5 removal commands, asked for a new session after removal, and said it would do nothing else. Before the guard joined the hook, the same plain question was answered without a stop (`838bb354`). One gap: README section 5 removes the old plugin with `--scope user`, the scope the 0.4.x README installed it with. This test installed it with `--scope local`, so the command given does not remove it.

## Control-plane rerun with ticket 82's publication commit (2026-11-26)

Ticket 82 rebuilt the publication commit, so the lifecycle was run again at the first `cp/wave3` commit that holds it.

| Field | Value |
| --- | --- |
| Commit | `f0ba49952f7846802066a3379a89af3cc94e6808` (ticket 82 integrated) |
| Expected publication | `3ab86d439f236880db92648ab28724a626dc360b` (ticket 82 revision06) |
| Command | `python ci/acceptance/lifecycle.py --candidate f0ba4995… --expected-publication 3ab86d43… --host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root C:/Temp/claude/cp77-r82-L1`, run in the fresh integration clone |
| Host CLIs | the host's own `claude` and `codex`, as pinned in `ci/acceptance/README.md` |
| Result | exit 0. Every verdict is `PASS`: build; fresh, upgrade, uninstall and recover on both hosts; level2 |

## Control-plane rerun with ticket 82 revision08's publication commit (2026-11-26)

Ticket 82 revision08 rebuilt the publication commit again, so the lifecycle was run again at the `cp/wave3` commit that holds it.

| Field | Value |
| --- | --- |
| Commit | `3e54da2cf7d057ba8b7501a203646ff7526dad55` (ticket 82 revision08 integrated and merged forward) |
| Expected publication | `e08e82d3373547a5448040638fb22b1810dc9cf3` (ticket 82 revision08) |
| Command | `python ci/acceptance/lifecycle.py --candidate 3e54da2c… --expected-publication e08e82d3… --host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root C:/Temp/claude/cp77-r82b-L1`, run in the fresh integration clone |
| Host CLIs | `claude` 2.1.332 and `codex` 0.172.0. Codex updated itself from 0.166.0 on 2026-11-26, so it differs from the version pinned in `ci/acceptance/README.md`; the owner's decision "放寬" on host CLI drift (REQ-043, 2026-11-26) covers it |
| Result | exit 0. Every verdict is `PASS`: build; fresh, upgrade, uninstall and recover on both hosts; level2 |

## Owner-assisted tests of 2026-11-26 on `3ab86d43` (ticket 82 revision06)

- **Two versions, Claude desktop app.** With `johnny-ai-skill` 0.4.14 installed at local scope, a plain question was stopped by the hook's guard. The answer gave README section 5's removal commands and the paragraph on project and local scope, and asked for a new session. After the owner removed the old plugin, a plain question was answered normally.
- **Codex desktop app, hook not trusted again.** The P0 and PRD questions were answered by searching the project with `rg`; no hook text had reached the session. `codex exec` in the test project printed `hook: SessionStart Failed` on Codex 0.166.0 and on 0.172.0, while the hook command exits 0 under cmd and Windows PowerShell.
- **Codex after trusting from the terminal.** The owner ran the terminal `codex` once and was asked to trust the changed hook ("有問要不要信任 然後quit"). Afterwards `codex exec` printed `hook: SessionStart Completed`, and a Codex desktop session answered the P0 and PRD questions from the plugin's `AGENTS.md` alone. Observation, not a violation: Codex searched its own memory file first, which is host behaviour.
- **Result.** Ticket 82 revision07 and revision08 rewrite README section 4 (owner decision "A"). The owner's retest of `e08e82d3` follows below when it is done.

## Owner-assisted retest of `e08e82d3` (ticket 82 revision08, 2026-11-26)

The owner reinstalled both hosts from the local marketplace. The control plane checked both `0.5.0` cache folders afterwards: each holds the README line that begins `安裝或更新 Software Factory 之後，請先在終端機裡`, and each equals the local marketplace's plugin tree.

- **Claude desktop app, test project, "P0 權限規則是什麼？".** The session read the plugin's `AGENTS.md`, looked for an `AGENTS.md` of the target project by file name (none), and read `plugin.json` for the version. It answered from the section `P0：權限與所有權` and named the file, the anchor `#p0-permissions`, the lines and the version 0.5.0. No grep and no full-text search.
- **Codex desktop app, test project, the same question.** The session read only the plugin's `AGENTS.md` and answered from the same section, naming the file and the version. No search of the project.
- **Codex trust.** After the reinstall, Codex's trust record for the hook holds a new content hash while the hook command is unchanged, so a reinstall renews the trust even when the hook text is the same. This agrees with README section 4, which sends the user to the terminal after each install or update.
- **Result.** The lookups go through the 流程索引 on both hosts with the final publication commit.

