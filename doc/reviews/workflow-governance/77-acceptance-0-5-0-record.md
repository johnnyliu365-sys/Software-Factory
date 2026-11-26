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

The acceptance workflow has never run. On a runner, `py -3.11` with the `level2` environment, `claude` and `codex` from `npm install --global` on `PATH`, and the `.cmd` shims of the npm packages are untested.

## The cloud run

Not run. The control plane adds the run id, the artifact and the verdicts here after the owner's confirmation.

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
