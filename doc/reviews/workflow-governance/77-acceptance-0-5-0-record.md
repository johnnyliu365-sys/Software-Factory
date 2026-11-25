# Acceptance of 0.5.0: record

Ticket: `modules/tickets/workflow-governance/77-acceptance-0-5-0.md` (revision02). The script is `ci/acceptance/lifecycle.py`, its rules and allow-lists are in `ci/acceptance/README.md`. This record starts with the local run. The control plane adds the cloud run and the owner-assisted Codex session below.

## The local run

Seat: `implementation-standard`, run id `jas77-r1`. Both run roots were new empty directories under `C:/Temp/claude/`, outside every Git work tree. The commands are the ones in `ci/acceptance/README.md`; the raw `report.jsonl` of each run is the raw block of the receipt's cells L1 and L2.

Host CLI versions read with `--version` by the script, against the pins of `ci/acceptance/README.md`:

| Host | Read locally | Pinned | Same |
| --- | --- | --- | --- |
| claude | 2.1.316 (Claude Code) | 2.1.316 | yes |
| codex | codex-cli 0.166.0 | 0.166.0 | yes |

The lines below come from runs at commit `d91c7447`. The candidate of the receipt has the same `lifecycle.py` and adds this record and a repair of the test's temporary path (CI showed that a Windows runner's 8.3 short temp path differs from the resolved run root the script reports). The receipt's cells L1 and L2 are the same two runs repeated at the candidate; their verdicts are the same.

### Run 1: `--host both --steps build,fresh,upgrade,uninstall,recover,level2` (condition 3)

| Step | Host | Verdict |
| --- | --- | --- |
| build | none | PASS |
| fresh | claude | PASS |
| fresh | codex | PASS |
| upgrade | claude | PASS |
| upgrade | codex | FAIL |
| uninstall | claude | PASS |
| uninstall | codex | PASS |
| recover | claude | PASS |
| recover | codex | PASS |
| level2 | none | PASS |

The run exits 1, so condition (3) is not met. The one `FAIL` is a `CHANGE_DETECTED`, not a defect of the script:

- **Step and command:** `upgrade`, host codex, `codex plugin add johnny-ai-skill@johnny-ai-skill --json`, after `codex plugin marketplace add johnnyliu365-sys/Johnny_AI_Skill_publication`. The marketplace add exits 0.
- **Output (exit 1):** `Error: git checkout 0000000000000000000000000000000000000000 failed with status exit code: 128`, then `fatal: unable to read tree (0000000000000000000000000000000000000000)`.
- **What it shows:** the public publication marketplace pins forty zeros, and Codex 0.166.0 honours `sha`: it tries to check that commit out and refuses the install. The ticket expected Codex either to install the default branch (`0b3afd36…`, the publication `main`) or to be told apart by the recorded commit; it does neither, so no 0.4.14 can be installed through Codex from that marketplace. The ticket says a refusal is `FAIL` and a `CHANGE_DETECTED` return. The same behaviour will fail the cloud run's `upgrade` step for Codex.

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
- **Third check: `--ref` with a `url`+`sha` source in the same repository.** Not testable by `file://` on 0.166.0 (above).
- **recover.** For Claude Code, `marketplace add` of a marketplace whose plugin source is a missing directory exits 0 and `install` exits 1 (`Source path does not exist`). For Codex, `marketplace add` exits 0 and `plugin add` exits 1 (`plugin source path is not a directory`). After the README's uninstall and marketplace remove, the good marketplace installs and the list shows exactly one entry, `software-factory@software-factory` `0.5.0`.
- **uninstall.** After the README's two commands, the only name `software-factory` left under the step directory is the plugin's own cache: for Claude Code `plugins/cache/software-factory` (the version directory carries an `.orphaned_at` marker), for Codex the empty directory `plugins/cache/software-factory`. Both are the two entries of the allow-list.
- **level2.** Both 0.4.9 assets match the approved sha256 values. `johnny-install.cmd` exits 0 with `INSTALL` answered on standard input into the empty `JOHNNY_ROOT`. The runtime's own `uninstall` reports `{"status": "REMOVED", "removed": ["PLUGIN_PAYLOAD", "VENV", "LAUNCHER", "QUEUE", "TELEMETRY"], "root_deleted": true}`, so `JOHNNY_ROOT` holds no file and the Level 2 allow-list is empty.

## Deviations from the wording of the ticket and the dispatch, with the reason

- **The run roots are not under the scratch directory.** The scratch directory `.worktrees/77-acceptance-scratch` is inside the main work tree (`git rev-parse --is-inside-work-tree` prints `true` there), and the ticket requires the script to refuse a run root inside a Git work tree, which the 0.4.9 installer also refuses (`INSTALL_BLOCKED_INSIDE_REPOSITORY`). The run roots are `C:/Temp/claude/jas77-r1-*`.
- **`JOHNNY_ROOT` is `<step>/root`, not the step directory.** The owner decision authorizes the answer to `INSTALL` for an empty `JOHNNY_ROOT`. With the downloads and `home` in the step directory it would not be empty, so they sit beside it.
- **The `level2` step leaves `USERPROFILE` out of the environment.** The `py` launcher that `install.ps1` calls exits 109 under any `USERPROFILE` other than the real one, and the step must not expose the real profile. `HOME` stays the step's own. With `USERPROFILE` set to `<step>/home` the install ends `PYTHON_311_UNAVAILABLE`.

## The cloud run

Not run. The control plane adds the run id, the artifact and the verdicts here after the owner's confirmation.

## The owner-assisted Codex session

Not run. The control plane records each step here.
