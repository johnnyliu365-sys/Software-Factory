# Acceptance of 0.5.0: the install lifecycle

`lifecycle.py` installs, updates, upgrades, uninstalls and recovers the plugin with the real Claude Code and
Codex command lines, each step in its own new directory, and writes one JSON line per step to
`<run-root>/report.jsonl`. It uses only the standard library. `.github/workflows/acceptance.yml` runs the same
script once on a GitHub-hosted Windows runner. Nothing here runs a prompt, `-p`, `exec`, a session or a login on
either host: the only host commands are `--version`, `plugin` and `plugin marketplace`.

## Host CLI versions

The workflow installs these exact versions. They are the versions that `--version` printed on this host at the
local run: the local run uses the `claude` and `codex` that come first on `PATH`, with no copied binary, and
the versions pinned here are the ones it printed. A run on another version is recorded with both versions (the
acceptance record, and the receipt's STATEMENT). Claude Code 2.1.332 differs from 2.1.316 in two ways that the
rules accept (owner decision of 2026-11-26): an uninstall leaves the host's own decline record, the key
`declinedPlugins` of `.claude.json`, and `plugin list --json` shows the host's `@builtin` plugins, which the
exactly-one-entry rule of `recover` does not count.

| Host | Version | npm package |
| --- | --- | --- |
| claude | 2.1.332 | `@anthropic-ai/claude-code@2.1.332` |
| codex | 0.166.0 | `@openai/codex@0.166.0` |

The 0.5.0 README says Codex needs the `plugin add` command, which `0.167.0-alpha.3.2` has and
`0.130.0-alpha.5` lacks. `0.166.0` has it too.

## The local run (condition 3)

The run root is a new empty directory outside every Git work tree (the 0.4.9 installer refuses to run inside
one). Use an interpreter that holds the packages of `requirements-dev.txt`: the `build` step runs the publication generator, which imports `pydantic`, and a Python 3.11 without it fails `build`.

```
python ci/acceptance/lifecycle.py --candidate <40 hex> --expected-publication <40 hex> --host both --steps build,fresh,upgrade,uninstall,recover,level2 --run-root <new empty directory>
python ci/acceptance/lifecycle.py --candidate <40 hex> --expected-publication <40 hex> --host codex --steps build,codex-ref,codex-files --run-root <another new empty directory>
```

The first run must exit 0. The second is recorded; a `NOT_SUPPORTED` there does not block completion.

| Argument | Rule |
| --- | --- |
| `--candidate`, `--expected-publication` | 40 lower-case hexadecimal characters, compared exactly |
| `--host` | `claude`, `codex` or `both` |
| `--steps` | a comma list of `build`, `fresh`, `upgrade`, `uninstall`, `recover`, `level2`, `codex-ref`, `codex-files`; `build` comes first and no step runs without it |
| `--run-root` | not empty as a path, not inside a Git work tree, not inside a configuration directory of the user, and empty or absent |

`build` and `level2` run once with host `none`. `fresh`, `upgrade`, `uninstall` and `recover` run for each
requested host. `codex-ref` and `codex-files` run for Codex only, and `--host claude` with either is refused.
A refused argument exits 2 and starts nothing.

Exit codes: 0 when every requested step is `PASS`; 1 when any step is `FAIL` or `NOT_SUPPORTED`; 2 when an
argument is refused. `NOT_SUPPORTED` is never a `PASS`.

## The parity run

The local run uses the interpreter and the host CLIs this host already has. The parity run installs the
Python packages and the host CLI versions that the workflow installs, so a Python package or a host CLI that
only this host has cannot hide a failure: cloud run 45920193720 failed at `build` because the workflow
installed no Python package, while every local interpreter already held `pydantic`. The control plane does
the parity run at the candidate before the cloud run.

`<A>` and `<B>` are two new empty directories outside every Git work tree. Run the commands from the root of
the work tree at the candidate.

```
py -3.11 -m venv <A>
<A>/Scripts/python.exe -m pip install -r requirements-dev.txt
npm install --prefix <B> --no-audit --no-fund @anthropic-ai/claude-code@2.1.332 @openai/codex@0.166.0
```

Then put `<B>/node_modules/.bin` first on `PATH` and run the first command of the local run with
`<A>/Scripts/python.exe`. It must exit 0. In `report.jsonl`, the generator's command names the interpreter
under `<A>`, and every host command names `claude.CMD` or `codex.CMD` under `<B>`.

The parity run does not cover the runner's `py` launcher, which the `level2` step's installer calls.

## Isolation

Each step runs in `<run-root>/<step>` (`<run-root>/<step>-<host>` for a host step) as its working directory.
For Claude Code that directory is `CLAUDE_CONFIG_DIR`, for Codex it is `CODEX_HOME`. A host CLI runs with
`PATH`, `SYSTEMROOT`, `WINDIR`, `COMSPEC`, `PATHEXT`, `TEMP`, `TMP`, `LOCALAPPDATA`, `APPDATA` and
`PROGRAMDATA` from the caller, plus the step's own variables: `HOME` and `USERPROFILE` set to `<step>/home`,
`GIT_CONFIG_GLOBAL` set to an empty file there, `GIT_TERMINAL_PROMPT=0` and `DISABLE_AUTOUPDATER=1`. Nothing
else is inherited.

The `level2` step runs the 0.4.9 installer, which is not a host CLI. Its downloads go to `<step>/download`,
and `JOHNNY_ROOT` is `<step>/root`, a new empty directory. Its environment is the allow-list, `HOME` set to
`<step>/home`, `JOHNNY_ROOT`, and no `USERPROFILE`: the `py` launcher that the installer calls exits 109 under
any `USERPROFILE` other than the real one, and the step must not expose the real profile. The install runs
with the step directory as its working directory, and the wrapper is passed by absolute path.

The Codex half of `upgrade` installs 0.4.14 from a local marketplace, `<step>/marketplace-0414/`, whose only
file is `.claude-plugin/marketplace.json`, written byte for byte from
`git show 01b810f096b1201005d26922e2c8a474bdd5a0a0:.claude-plugin/marketplace.json` in the build clone. The public
publication marketplace pins forty zeros and Codex honours that `sha`, so it cannot be used (owner decision of
2026-11-26, "A"). The step passes only when `git rev-parse HEAD` in the installed directory is
`0b3afd3645946f97662c336f0e6ac0dcae502e69`. Claude Code reads the public 0.4.14 marketplace at that commit.

The host state that a step may still write outside its step directory:

- the pip cache (`%LOCALAPPDATA%\pip\Cache`), written by the 0.4.9 installer's hash-locked `pip install`;
- `%TEMP%` staging: `johnny-install-wrapper-*`, `johnny-bootstrap-*` and `johnny-uninstall-*` directories, which
  the 0.4.9 installer creates and removes itself;
- the Codex update check, which the Codex CLI may run when it starts;
- anything the host CLI keeps under `%LOCALAPPDATA%` and `%APPDATA%`, which are inherited because the host CLIs
  and the installer need them.

## The Level 2 step and the INSTALL prompt

The 0.4.9 installer asks a person to type `INSTALL` and says an agent's answer is not consent. The owner
decided on 2026-11-26 (S77R-01, option A) that `lifecycle.py` answers that prompt on standard input, only for an
install into a `JOHNNY_ROOT` that is new and empty, made for this acceptance, on this host and on the runner.
The script checks that `JOHNNY_ROOT` is empty before the install and answers nowhere else. The authorization
covers this test use only.

## Allow-lists

`lifecycle.py` reads these two fenced blocks. Each entry is judged exactly; anything else is `FAIL`. The lists are
reviewed under condition (4).

The `uninstall` step scans every path and every line of a `.json` or `.toml` file under the step directory for
the name `software-factory` as a whole name: a match is not preceded or followed by a letter, a digit, `_` or
`-`, so `software-factory-plugin` and `my-software-factory` do not match, and `software-factory.json` does.
Entry fields are `kind | host | path relative to the step directory | reason`. A `path` entry admits the path
and everything below it, an `emptydir` entry admits a directory that holds no file at any depth, and a `line`
entry admits the lines of one file. A `key` entry names `<file>#<top-level key>` and admits that key's value
and nothing else of the file: any other key or line of the file that names `software-factory` is `FAIL`. The
one `key` entry is the value of `declinedPlugins` in `.claude.json`, which Claude Code 2.1.332 writes on
uninstall. The `uninstall` step then adds the good marketplace and installs again with the record present; it
must exit 0 and the list must show 0.5.0, installed and enabled.

```lifecycle-allowlist
path | claude | plugins/cache/software-factory | Claude Code keeps the uninstalled plugin's cache and marks the version directory with an .orphaned_at file, to remove it after a delay; it is the plugin's own copy, not a registration
key | claude | .claude.json#declinedPlugins | the host's own decline record (owner decision 2026-11-26, 放寬)
emptydir | codex | plugins/cache/software-factory | Codex removes the plugin's files and leaves the empty marketplace directory of its cache
```

The `level2` step requires that `JOHNNY_ROOT` holds no file after `uninstall`, apart from the entries below.
Each entry is a path relative to `JOHNNY_ROOT`, then a quotation from section 6 of the repository `README.md`
(`舊版 Level 2 runtime 的移除`) that says why it stays. The list is empty: on the local run, the 0.4.9
`uninstall` reported `REMOVED` for the plugin, venv, launcher, queue and telemetry folders and deleted the root,
as section 6 says ("全部移除後，再清掉安裝日誌與已空的根目錄"). The downloaded installer and zip are in
`<step>/download`, not in the root ("下載來的安裝檔與 zip，它們在下載資料夾，不在根目錄").

```lifecycle-level2-allowlist
```

## The four conditions

The cloud run happens once, and only when all four hold. The control plane checks them, then asks the owner.

| # | Condition | Where its evidence lives |
| --- | --- | --- |
| 1 | Ticket 71 is approved and integrated with its package check | `doc/reviews/workflow-governance/71-publication-0-5-code-review.md`, and the integration commit `f53ecc6a` on `cp/wave3` |
| 2 | The job triggers by `workflow_dispatch` only, never on push | `.github/workflows/acceptance.yml`, pinned by `tests/test_acceptance_lifecycle.py` (`WorkflowTests`) |
| 3 | Each lifecycle step has passed locally in isolated directories | `doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md`, section "The local run", and the receipt of ticket 77 (cell L1) |
| 4 | The job itself has been reviewed | the review record of ticket 77 under `doc/reviews/workflow-governance/` |

The trigger, once the conditions hold and the owner has confirmed the fast-forward of the development `main`:

```
gh workflow run acceptance.yml --ref main -f candidate=<the main commit after the fast-forward> -f expected_publication=<ticket 71's publication commit>
```
