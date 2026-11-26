# Acceptance of 0.5.0: record

Ticket: `modules/tickets/workflow-governance/77-acceptance-0-5-0.md` (revision03). The script is `ci/acceptance/lifecycle.py`, its rules and allow-lists are in `ci/acceptance/README.md`. This record starts with the local run. The control plane adds the cloud run and the owner-assisted Codex session below.

## The local run

Seat: `implementation-standard`, run id `jas77-r2`. Both run roots were new empty directories under `C:/Temp/claude/`, outside every Git work tree. The commands are the ones in `ci/acceptance/README.md`; the raw `report.jsonl` of each run is the raw block of the receipt's cells L1 and L2.

Host CLI versions, as read by the script with `--version`, against the pins of `ci/acceptance/README.md`:

| Host | Run with | Pinned | Same |
| --- | --- | --- | --- |
| claude | 2.1.316 (Claude Code) | 2.1.316 | yes |
| codex | codex-cli 0.166.0 | 0.166.0 | yes |

**The `claude` on this host moved to 2.1.332 between the first and the second dispatch** (the host's own updater; the script sets `DISABLE_AUTOUPDATER=1` for its steps, but the installed binary was replaced by the user's own sessions). The cells of the receipt were run with the pinned 2.1.316, using a copy of the host's own `versions/2.1.316` binary placed first on `PATH` in a directory named with the run id. Under 2.1.332 two steps do not pass, for reasons in the host, not in the script:

- `uninstall claude` is `FAIL`: after the README's two commands, `.claude.json` holds `"declinedPlugins": ["software-factory@software-factory"]`, a line naming the plugin that 2.1.316 does not write.
- `recover claude` is `FAIL`: `claude plugin list --json` lists four built-in entries (`cc-plugin-agents-md@builtin`, `cc-plugin-plugin-authoring@builtin`, `cc-plugin-privacy@builtin`, `cc-plugin-telemetry@builtin`) beside `software-factory@software-factory`, so the list does not hold exactly one entry.

The other eight steps pass under 2.1.332. The cloud run installs the pinned 2.1.316 from npm and is not affected. If the pin is moved, the allow-list and the exactly-one rule need the owner's decision first.

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

The lines come from a run at commit `85e0e4ea`. The candidate of the receipt has the same `lifecycle.py` and adds this record. The receipt's cells L1 and L2 are the same two runs repeated at the candidate.

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
- **recover.** For Claude Code, `marketplace add` of a marketplace whose plugin source is a missing directory exits 0 and `install` exits 1 (`Source path does not exist`). For Codex, `marketplace add` exits 0 and `plugin add` exits 1 (`plugin source path is not a directory`). After the README's uninstall and marketplace remove, the good marketplace installs and the list shows exactly one entry, `software-factory@software-factory` `0.5.0`.
- **uninstall.** After the README's two commands, the only name `software-factory` left under the step directory is the plugin's own cache: for Claude Code `plugins/cache/software-factory` (the version directory carries an `.orphaned_at` marker), for Codex the empty directory `plugins/cache/software-factory`. Both are the two entries of the allow-list.
- **level2.** Both 0.4.9 assets match the approved sha256 values. `johnny-install.cmd` runs with the step directory as its working directory and the wrapper passed by absolute path, and exits 0 with `INSTALL` answered on standard input into the empty `<step>/root`. The runtime's own `uninstall` reports `{"status": "REMOVED", "removed": ["PLUGIN_PAYLOAD", "VENV", "LAUNCHER", "QUEUE", "TELEMETRY"], "root_deleted": true}`, so `JOHNNY_ROOT` holds no file and the Level 2 allow-list is empty. The environment is the allow-list, `HOME=<step>/home`, `JOHNNY_ROOT`, and no `USERPROFILE` (the `py` launcher exits 109 under any other value).

## Not tested

The acceptance workflow has never run. On a runner, `py -3.11` with the `level2` environment, `claude` and `codex` from `npm install --global` on `PATH`, and the `.cmd` shims of the npm packages are untested.

## The cloud run

Not run. The control plane adds the run id, the artifact and the verdicts here after the owner's confirmation.

## The owner-assisted Codex session

Not run. The control plane records each step here.
