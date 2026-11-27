# Ticket 77 review: acceptance of 0.5.0, closure revision02

- Ticket: `modules/tickets/workflow-governance/77-acceptance-0-5-0.md`, revision02, read at `0cfb563b`. The only difference from the worktree copy is the state row.
- Dispatch: `doc/handoffs/2026/workflow-governance/dispatch/JAS-77-1.yaml` at `0cfb563b`. Its sha256 is `bc21737c…c7095` (recomputed), the same digest as the state row.
- Base: `f53ecc6a44e608492130e8e686284879657eb2cc`.
- Candidate: `504e517761c5085eb953cd7db46afc9c57e825dd`, three commits on `cp/wave3-77-acceptance` (`d91c7447`, `ca66d505`, `504e5177`). The candidate equals `origin/cp/wave3-77-acceptance` (`git ls-remote`).
- Receipt: `.worktrees/77-acceptance-out/RETURN.md`. The appended USAGE cell is its only difference from `RETURN.as-returned.md`.
- Review label: the initial review of closure revision02, labelled by the control plane before dispatch. Process tier: strict.
- Reviewer: `ticket-review` seat, run id `R77-1` (claude-opus-5-5).
- References read in full: `CodeReview.md` and `skills/johnny-project-takeover/references/review-checks.md`. Also read: `Workflow.md` §7, `skills/johnny-project-takeover/scripts/rework_report.py`, the S77R table of `doc/reviews/workflow-governance/77-acceptance-0-5-0-ticket-review.md`, and `modules/tickets/TEMPLATE.md` (boundary block).

## Revision02 returned CHANGE_DETECTED before review

The seat returned `CHANGE_DETECTED` with commit `504e5177`, before any review. Under CodeReview §3, that return counts as a round, and its `RETURN` block stands before the first review section. The rule says the control plane writes the block. It is placed here, at the control plane's request, so it can be copied unchanged into the code-review record.

```rework-record
candidate: 504e517761c5085eb953cd7db46afc9c57e825dd
round: 1
kind: RETURN
verdict: CHANGE_DETECTED
causes: DESIGN_UNFORESEEN
```

## Initial review of closure revision02

### Findings

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S77-01 | `REQUIREMENT_CHANGED` | High, blocking | ticket item 2 `upgrade` (Codex); `ci/acceptance/lifecycle.py` `old_install`; `.github/workflows/acceptance.yml` step list | **The seat's `CHANGE_DETECTED` is confirmed, and its evidence is true and complete.** The public publication marketplace pins `sha` `0000…0000`. Codex 0.166.0 honours `sha`, so `codex plugin add johnny-ai-skill@johnny-ai-skill --json` exits 1. The ticket's Codex `PASS` rule (0.4.14 installed from `0b3afd36…`) cannot be met. As a result, L1 exits 1 and condition (3) is not met. The cloud workflow runs the same `upgrade` step for Codex, so as written it would fail too. The seat stopped correctly: `old_install` raises `StepFail` at once, with no retry, other source or edited rule. The ticket wording (a refusal is `FAIL` and a `CHANGE_DETECTED` return) was followed, and the return names the step, the command and its output. | (1) `gh api repos/johnnyliu365-sys/Johnny_AI_Skill_publication/contents/.claude-plugin/marketplace.json`: the plugin source is `{"source":"url","url":"…Johnny_AI_Skill_publication.git","sha":"0000000000000000000000000000000000000000"}`. There is no `.agents/plugins/marketplace.json`. Publication `main` is `0b3afd36…`. (2) The reviewer's own run, V1 (`--host codex --steps build,upgrade`, run root `C:/Temp/claude/R77-1-upgrade`): build `PASS` with `d355b4a2…`; `marketplace add johnnyliu365-sys/Johnny_AI_Skill_publication` exits 0; `plugin add` exits 1 with `git checkout 0000000000000000000000000000000000000000 failed … fatal: unable to read tree`. This is the same output as receipt L1 line 62. (3) The Claude marketplace at `01b810f0` pins `0b3afd36` directly, which is why `upgrade claude` passes. | This is not decided here; the owner decides it. Revision03 must restate the Codex half of `upgrade`, meaning its source and its `PASS` rule, and the cloud step list to match. Until then neither the local condition (3) nor the cloud run can pass. |
| S77-02 | `TICKET_DEFECT` | High, blocking integration | ticket revision02, `johnny-boundary` block | The boundary block has `create` and `forbid` lines but no `modify` line. `document_mutation_gate.read_boundary` returns `UNPARSABLE`, with the message 缺少必要欄位 'modify'：沒有宣告可讀邊界的票不得整合. `modules/tickets/TEMPLATE.md` line 46 also requires at least one `modify` entry. As committed, the ticket cannot pass the boundary gate before integration. The dispatch lint `--ticket` run at `0cfb563b` did not catch it. | Reviewer script `R77-1-boundary.py`: `read_boundary` on the ticket blob at `0cfb563b` gives `UNPARSABLE`. With one reviewer-added line (`modify = doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md`), it gives `DECLARED`. `parse_raw_diff(git diff --raw -z --no-renames f53ecc6a 504e5177)` then gives five `CREATE 100644` changes, each `evaluate_change` → `None`, and `evaluate_changes` → `(None, None)`. No forbidden path is touched. | In revision03, add one `modify =` line. The acceptance record is the natural entry, because the control plane later appends the cloud run and the Codex session to it. |
| S77-03 | `EVIDENCE_DEFECT` | Medium | `tests/test_acceptance_lifecycle.py` `test_no_variable_outside_the_allow_list_reaches_a_host_cli` | **The environment allow-list is pinned against a copy, not against the ticket.** The test builds `allowed` from `lifecycle.ENV_ALLOW_LIST`, the production constant itself. Adding a credential name to that constant changes both sides, so the test stays green even when the credential is in the caller's environment and reaches every host CLI. Only `GITHUB_TOKEN` and a sentinel are named. The code is correct today, but a regression would let a credential through. | Reviewer mutation RM1: `"ANTHROPIC_API_KEY", "OPENAI_API_KEY"` were added to `ENV_ALLOW_LIST`, and pytest ran with both variables set. Result: **55 passed, exit 0** (zero red). This is the "copy" misalignment of review-checks. | Assert `lifecycle.ENV_ALLOW_LIST` equals a literal tuple of the ticket's ten names, or build `allowed` from that literal. Optionally also set `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` in the test's `environ` and assert both are absent. |
| S77-04 | `EVIDENCE_DEFECT` | Medium | `tests/test_acceptance_lifecycle.py` `ResidueTests`; `lifecycle._path_allowed` | **The allow-list `path` entry is not pinned as a path component.** If the entry is matched as a plain string prefix, a sibling such as `plugins/cache/software-factory.old/…` is admitted. That sibling names `software-factory` as a whole name (a `.` is a boundary), so it is residue. The code is correct today (it compares `== target` or `startswith(target + "/")`), but no test fails if that changes. This is the path-prefix row of the defect table, applied to the allow-list side. | Reviewer mutation RM2: `relative == entry.target or relative.startswith(entry.target + "/")` → `relative.startswith(entry.target)`. Result: **55 passed, exit 0** (zero red). | In `test_the_scan_honours_each_kind_of_allow_entry`, write `plugins/cache/software-factory.old/a.json` and assert `path plugins/cache/software-factory.old` is among the findings. |
| S77-05 | `EVIDENCE_DEFECT` | Low | `tests/test_acceptance_lifecycle.py` (fake CLI); `PluginEntry.is_installed_and_enabled` | "Installed and enabled" (`fresh`, `upgrade`, `recover`) is not pinned on the `enabled` side. The fake always lists `enabled: true`, so a read-back that accepts a disabled or flagless entry passes. | Reviewer mutation RM4: `self.enabled is True` → `self.enabled is not False`. Result: **55 passed, exit 0** (zero red). | Add a fake mode that lists `"enabled": false`, and assert `fresh` is `FAIL`. |
| S77-06 | `TICKET_DEFECT` | Low | ticket item 5 ("Both run roots are under its scratch directory"); dispatch `scratch` and `run_root_rule` | Item 5 and the dispatch put the run roots under `.worktrees/77-acceptance-scratch`, which is inside the main work tree. Item 1, and the 0.4.9 installer, refuse a run root inside a work tree, so the two rules cannot both hold. The seat ran under `C:/Temp/claude/jas77-r1-*` and stated this in the receipt and the record. It is the only reading that satisfies item 1. | `check_run_root` walks the root and its parents for `.git`. The seat reports that `git rev-parse --is-inside-work-tree` is true in scratch, and the path layout confirms it (`.worktrees/` sits under the repository root). | In revision03, and in the next dispatch, name the run roots as a run-id-tagged directory under `C:/Temp/claude/`, outside every work tree. |
| S77-07 | `TICKET_DEFECT` | Low | ticket item 2 `level2` ("`JOHNNY_ROOT` set to the step's directory") | The ticket's wording conflicts with the owner decision of 2026-11-26, which authorizes the `INSTALL` answer only into an *empty* `JOHNNY_ROOT`. The step directory already holds `home` (made by `build_environment`) and the downloads. The seat used `<step>/root`, which is new and checked empty, and stated this in the receipt, the README and the record. That resolution is correct. | `step_level2`: `root.mkdir()` (no `exist_ok`), then `any(root.iterdir())` refuses, then `JOHNNY_ROOT=<step>/root`. Test `test_the_install_prompt_…` asserts `root_entries: []`. | In revision03, word it as `JOHNNY_ROOT` = `<step>/root`, a new empty directory, with the downloads in `<step>/download`. |
| S77-08 | `TICKET_DEFECT` | Low | ticket item 1 environment sentence; `step_level2` `omit=("USERPROFILE",)` | Item 1 sets `HOME` and `USERPROFILE` to `<step>/home` for each **host CLI**. It does not say what environment the 0.4.9 installer (not a host CLI) gets. The seat leaves `USERPROFILE` out for `level2` only (`HOME` stays the step's own), because `py` exits 109 under a foreign `USERPROFILE`. This does not break item 1 as written. It is acceptable: the real profile is never passed, and `APPDATA` and `LOCALAPPDATA` are inherited for every step under the ticket's own allow-list. It is stated in the receipt (STATEMENT item 9), in `ci/acceptance/README.md` § Isolation, and in the record. The runner behaviour of `py -3.11` with this environment is untested, and the seat says so. | `build_environment(..., omit)`; the fake installer logs `has_userprofile: False`, which the test asserts. README § Isolation, paragraph 2. | In revision03, state the `level2` environment explicitly: the allow-list, `HOME=<step>/home`, no `USERPROFILE`, and `JOHNNY_ROOT`. |
| S77-09 | `IMPLEMENTATION_DEFECT` | Low | `ci/acceptance/lifecycle.py` `step_level2`, `run_command(..., cwd=downloads, ...)` | Item 1 says every command runs with its step directory as the working directory. The 0.4.9 install runs in `<step>/download`. The other commands follow the rule: `build`'s generator runs "there" in `repo`, which the ticket itself names, and the uninstall uses `ctx.step_dir`. Isolation is unaffected because the directory is inside the step directory. The deviation is not stated in the receipt or the README. | Line 1054: `cwd=downloads`. | Use `cwd=ctx.step_dir`, since the wrapper is passed by absolute path. If the wrapper needs its own directory, state that deviation in `ci/acceptance/README.md` § Isolation instead. |
| S77-10 | `EVIDENCE_DEFECT` | Low | `RETURN.md` STATEMENT items 3 and 4 | The STATEMENT names the run roots `C:/Temp/claude/jas77-r1-L1` and `…-L2`, but the raw blocks of cells L1 and L2 show `C:\Temp\claude\jas77-r1-L1b` and `…-L2b`. This is a receipt statement that its own evidence contradicts. The verdicts themselves are unaffected. | `RETURN.md` lines 58–67 and 85–87 (`…jas77-r1-L1b\build\…`, `…jas77-r1-L2b\…`) against lines 519–520. | In the corrected receipt, name the run roots exactly as the raw blocks show them. |
| S77-11 | `OUT_OF_SCOPE_HARDENING` | Low | `lifecycle._WHOLE_NAME` | The residue match is case-sensitive, and Windows paths are not. A residue spelled `Software-Factory` would not be found. The ticket does not fix case, and both hosts write the lower-case marketplace name, so the current closure is not violated. | Regex `(?<![A-Za-z0-9_-])software-factory(?![A-Za-z0-9_-])`, no `re.I`. | Follow-up hardening: match case-insensitively, and add one test row. |

### Checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Admission | PASS | Ticket blob at `0cfb563b` is equal to the worktree copy apart from the state row. Dispatch sha256 recomputed equal. Base..candidate is three commits, all authored `Johnny Liu <johnny.liu365@gmail.com>` with trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (dispatch model `claude-sonnet-5-5`). The review worktree is detached at the candidate with porcelain 0. |
| 2 | Arguments and pairings (item 1) | PASS | `validate_plan`: both SHAs fullmatch `[0-9a-f]{40}`; host ∈ {claude, codex, both}; steps are non-empty, known and unique, and `build` comes first; `--host claude` with `codex-ref` or `codex-files` is refused. `hosts_for` runs `build` and `level2` with `none`, and the codex-only steps for `codex`. A refusal exits 2. Tests: `RuleViolationTests` (eight cases). |
| 3 | Run-root refusals | PASS | `check_run_root` refuses: an empty or blank path; any `.git` at the root or a parent; a path inside `~/.claude`, `~/.codex`, `~/.config/{claude,codex}` or `%LOCALAPPDATA%\JohnnyRouter`; a non-directory; and a non-empty directory. Tests cover each case. The seat's mutation of the non-empty check is red (M1). |
| 4 | Allow-listed environment | PASS in code; test gap S77-03 | `build_environment` copies only the ten names, then sets `HOME`/`USERPROFILE=<step>/home`, `GIT_CONFIG_GLOBAL` (an empty file), `GIT_TERMINAL_PROMPT=0`, `DISABLE_AUTOUPDATER=1` and the host variable. Each host CLI's working directory is its step directory, which the test asserts for `fresh`. The `level2` deviation is covered in S77-08. |
| 5 | Report line | PASS | `report_line` writes the keys `step`, `host`, `verdict`, `commands[argv, exit, output(, error)]` and `evidence`. `redact` removes e-mail addresses and token shapes, and is tested. The exit code is 0 only when every step is `PASS`; the seat's mutation that let `NOT_SUPPORTED` pass is red (3 tests). |
| 6 | Steps, commands and `PASS` rules (S77R-04 to S77R-13) | PASS apart from S77-01, S77-09 | **build:** `--no-hardlinks` clone, detached checkout, exact generator command, exact commit comparison (mutation red), `git archive` plus a safe extract, and the ticket 71 item 8 layout with both files; later steps fail when build fails. **fresh:** the README commands, with `plugin list --json` and `plugin list --marketplace … --json`; a missing `--json` gives `NOT_SUPPORTED`; Claude runs `update` and lists again. **upgrade:** the exact URL and repo; the commit is read from `installed_plugins.json` for Claude and from `git rev-parse` of `installedPath` for Codex; then section (5) removal, local install, and both lists. **uninstall:** the fresh state, the README's two commands, then the residue scan. **recover:** the first non-zero command is the expected failure; both exiting 0 is `FAIL` (tested); cleanup exits are recorded but not judged; exactly one entry afterwards. **level2:** covered in rows 8 and 9. **codex-ref:** a bare repository whose default tip differs from the pin, a marketplace branch holding only `.claude-plugin/marketplace.json`, `file://` plus `--ref marketplace`, and a tree comparison; a refused add is `NOT_SUPPORTED`. **codex-files:** three marketplaces; `FAIL` only on a crash or timeout. |
| 7 | Allow-lists in `ci/acceptance/README.md` (condition 4) | PASS as reviewed | Claude: `path plugins/cache/software-factory`, the orphaned cache marked `.orphaned_at`, with a reason. Codex: `emptydir plugins/cache/software-factory`, with a reason. Both match what L1 found. Level 2: the list is empty, and the README quotes section (6) twice; `ReadmeTests` checks both quotes against the shipped `README.md`. The whole-name regex is pinned (reviewer RM3 is red, 2 tests); path-component matching is not (S77-04). |
| 8 | The `INSTALL` answer, as limited by the owner | PASS | `LEVEL2_CONFIRMATION` is passed to `stdin` at exactly one call site (`step_level2`, line 1056). `root` is freshly made and checked empty before the call. No other `run_command` passes `stdin`. |
| 9 | `v0.4.9` sha256 values | PASS | `LEVEL2_ASSETS` equals the ticket: zip `2365b6f7…54aef`, cmd `906b0672…f532b`. `urllib` downloads without a token; a mismatch is `FAIL` before anything runs (tested). L1 shows the installer printing the same bundle digest. |
| 10 | Workflow | PASS | The trigger is `workflow_dispatch` only, with inputs `candidate` and `expected_publication`. Also: `permissions: contents: read`, `windows-latest`, `timeout-minutes: 60`. Checkout `d23441a4…` (v6.1.0) and setup-python `ece7cb06…` are equal to `ci.yml`. upload-artifact `cf430e03…` is the tag `v7.0.2` (`gh api repos/actions/upload-artifact/git/ref/tags/v7.0.2`). `fetch-depth: 0` and `persist-credentials: false` are set. There is no `secrets.`, token name, `id-token` or login. Inputs reach the script through `env`, never inline. `--host both` with the six steps, `--run-root "$RUNNER_TEMP/acceptance"` (outside the checkout), and `report.jsonl` uploaded `if: always()`. The npm versions equal the README (tested). `gh run list --workflow acceptance.yml` gives 404 because the file is not on the default branch: it has never run. Untested on a runner, as the seat says: `py -3.11` with this environment, and the npm `.cmd` shims. |
| 11 | The test | PASS with gaps S77-03, S77-04, S77-05 | The fakes are Python files run through `sys.executable`. The one Windows-only case is `skipUnless(win32)` with a reason. `ci/registered-failures.json` is not in the diff. CI run 45688874046 on `504e5177` succeeded on both jobs (`gh run view`). The downloaded log (14,989 lines) has no `UNREGISTERED_FAILURE` or `REGISTERED_NOT_FAILING`. Reviewer counter-mutations, each run on the full file, with unfiltered output read directly (no wrapper), in a disposable `--no-hardlinks` clone, porcelain 0 after each: baseline 55 passed; **RM1** credential names in the allow-list: 55 passed (zero red, S77-03); **RM2** path entry as a string prefix: 55 passed (zero red, S77-04); **RM3** residue name matched as a substring: 2 failed (`test_names_that_only_start_or_end_like_the_plugin_are_not_residue`, `test_the_name_matches_as_a_whole_name_…`), red as intended; **RM4** `enabled` ignored: 55 passed (zero red, S77-05). |
| 12 | Local run (L1, L2, record) | PASS; each verdict follows from its evidence | L1: nine `PASS` and `upgrade codex` `FAIL`, exit 1. Each `PASS` row holds the read-back that the rule needs. Example: `uninstall` notes "no residue … outside the 2 allow-listed entries"; `level2` shows the runtime reporting `REMOVED` and `root_deleted: true`. L2: build `PASS`; `codex-ref` `NOT_SUPPORTED`, because the `file://` add exits 1 with `invalid marketplace source format`; `codex-files` `PASS` (both files: 0.5.1 from `sf-agents`, so Codex reads `.agents/plugins/marketplace.json`; each file alone: 0.5.0). The record matches these, and it states that Codex honoured `sha`. The reviewer's V1 reproduces the Codex refusal. V1's `CODEX_HOME` holds `config.toml` with `[marketplaces.johnny-ai-skill]`, so the state stayed in the step directory. |
| 13 | Seat-flagged items | Judged | (1) Run roots outside scratch: correct, see S77-06. (2) `level2` layout: correct, see S77-07. (3) `USERPROFILE` left out: acceptable and stated in the receipt, the README and the record, see S77-08. (4) Direct `--version` calls are permitted by the dispatch and by item 5. The `plugin --help` probes are the `plugin` subcommand run in the script's isolated environment. Neither ran a prompt, session or login. Not a finding. (5) The L2 results are as stated in row 12. |
| 14 | Boundary (`document_mutation_gate`) | FAIL as committed (S77-02); the diff is otherwise inside | See S77-02. The five created paths are exactly the five `create` entries, and no path is `forbid`. |
| 15 | Receipt truth | PASS apart from S77-10 | P1 rerun at the candidate: 166 passed, 392 subtests, the same as the receipt. T1 rerun: `Success: no issues found in 2 source files`. M1 read: four mutations, each red for its intended test, porcelain 0. C1: as above. E1 rerun with `--candidate 504e5177`: `cells=9 defects=0`, exit 0. The `tool_digest` values equal the sha256 at the candidate for `dispatch_lint.py`, `receipt_fence_check.py` and `index_pins.py`; that is the set P9's checker requires. F1: one failure, which is registered. Residue: no `jas77-r1-*` under `C:/Temp/claude`, `77-acceptance-scratch` is empty, and there is no host lock. The STATEMENT's `return: CHANGE_DETECTED` and `items: 15` match its 15 items. |
| 16 | P0 strong types | PASS | `mypy --strict` is clean. There is no `Any` and no `type: ignore` in either file. Dynamic JSON is narrowed at the boundary (`_as_text`, `_as_flag`, `read_json_object`). |
| 17 | XSS, Agent control, profile fan-out | Not applicable | No browser, WebView or DOM is involved (ticket XSS row). No Agent-to-Agent control is involved. There is one implementer seat under `implementation-standard`. |
| 18 | Full suite | Not rerun | No host lock was taken. The seat's F1 (under the lock) and both CI jobs cover it. |

### Verdict

`BLOCKED`. The candidate implements items 1 to 4 faithfully, and the seat's `CHANGE_DETECTED` is true and complete. The completion definition still cannot be met. L1 must exit 0 for condition (3), and the Codex half of `upgrade` cannot pass under revision02 (S77-01, owner decision pending). The ticket's boundary block is also unparsable by the integration gate (S77-02, control plane). Revision03 should carry S77-06 to S77-08. The seat's next correction should close S77-03, S77-04, S77-05, S77-09 and S77-10 together. Under the review label rule, the first review of revision03 starts a new count.

```review-verdict
candidate: 504e517761c5085eb953cd7db46afc9c57e825dd
verdict: BLOCKED
round: initial
closure_revision: revision02
reviewer: ticket-review seat R77-1 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 504e517761c5085eb953cd7db46afc9c57e825dd
round: 2
kind: INITIAL
verdict: BLOCKED
causes: CONTROL_PLANE_RULE,RETURN_UNTRUE,DESIGN_UNFORESEEN,IMPLEMENTATION_DETAIL
```

### Commands and captures

- Boundary: a reviewer script that imports `library.local_orchestration.document_mutation_gate` and runs `read_boundary`, `parse_raw_diff` and `evaluate_changes`, as quoted in S77-02.
- V1: `python ci/acceptance/lifecycle.py --candidate 504e5177… --expected-publication d355b4a2… --host codex --steps build,upgrade --run-root C:/Temp/claude/R77-1-upgrade` printed `PASS build none`, `FAIL upgrade codex` and `exit=1`. The capture is `V1-reviewer.txt`, beside this file. Only the `plugin` and `plugin marketplace` subcommands and `--version` ran, all through `lifecycle.py`. No prompt, `-p`, `exec`, session or login ran, and the user's configuration was not touched.
- Counter-mutations: the full diffs and unfiltered pytest output are in `M-reviewer.txt`, beside this file.
- `gh api` reads of public repositories: the publication marketplace, the 0.4.14 Claude marketplace at `01b810f0`, and the upload-artifact tag. `gh run view 45688874046` and its `--log`. No workflow was run or dispatched.
- Validation of this file's blocks: `rework_report.py` on this file.

### Residue

Removed: `C:/Temp/claude/R77-1-upgrade`, `C:/Temp/claude/R77-1-mypycache`, and every `R77-1-*` entry in `.worktrees/77-acceptance-review-scratch` (the disposable clone `R77-1-m`, the driver and boundary scripts, the CI log, and the captures, which were copied here first without the run id). Nothing carrying `R77-1` is left. The candidate branch, the other worktrees and the out directory of the seat were not modified. `PROCESSES_LEFT=0`.

## Revision03 initial review

- Ticket: revision03, read at `origin/cp/wave3`. The ticket's last change is commit `73338063`.
- Dispatch: `JAS-77-2.yaml`. Its sha256 is `a5bd4e9d…c8c59bb` (recomputed), the same digest as the state row.
- Owner decision: the REQ-043 row "Owner decision 2026-11-26 (ticket 77 CHANGE_DETECTED: the Codex upgrade from 0.4.14, "A")".
- Candidate: `9d4ccf63f1d9632c430d5f50dcb36d567bbda14f`, four additive commits on `504e5177` (`85e0e4ea`, `1617da7d`, `5895815e`, `9d4ccf63`).
  - All four are authored `Johnny Liu <johnny.liu365@gmail.com>`, with the trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
  - The candidate equals `origin/cp/wave3-77-acceptance`.
  - `lifecycle.py` is unchanged after `85e0e4ea`. Later commits change only the record and the test, as the record says.
- Label: the initial review of closure revision03. The count restarts here (CodeReview §5, `rule-review-label`).
- Reviewer: `ticket-review` seat, run id `R77-2` (claude-opus-5-5).

### Closure of the revision02 findings (diff `504e5177..9d4ccf63`)

| id | status | evidence |
| --- | --- | --- |
| S77-01 | Closed | The owner decision is implemented word for word against revision03 item 2. `old_marketplace_source` writes `<step>/marketplace-0414/.claude-plugin/marketplace.json` from `git cat-file blob 01b810f0…:.claude-plugin/marketplace.json` in the build clone. `cat-file` applies no filter, so the bytes are exact (1026 bytes, matching `git cat-file -s` in the main repository). That file is the only one in the directory. Codex adds that directory and installs the plugin. The step records the commit from `git rev-parse HEAD` in `installedPath`, `PASS` needs `OLD_PINNED_COMMIT`, and a refusal is `StepFail`. Claude still uses the public URL at `01b810f0`. In L1, `upgrade codex` is `PASS` with `rev-parse` = `0b3afd36…`. The `01b810f0` blob pins `0b3afd36` with the publication-repository URL, as read in round 1 via `gh api`. `01b810f0` is an ancestor of the candidate, so a `fetch-depth: 0` runner clone holds it. Reviewer RM5 (blob re-serialized) turns `test_codex_installs_0414_from_a_local_marketplace_written_byte_for_byte` red. |
| S77-02 | Closed | Revision03 adds `modify = doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md`. `document_mutation_gate.read_boundary` → `DECLARED`. `parse_raw_diff(git diff --raw -z --no-renames f53ecc6a 9d4ccf63)` gives five `CREATE 100644` changes, each with `evaluate_change` `None`, and `evaluate_changes` gives `(None, None)`. |
| S77-03 | Closed | The test pins `ENV_ALLOW_LIST == TICKET_ENV_ALLOW_LIST`, a literal tuple of the ten names. It also injects `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. Reviewer RM1 now fails `test_no_variable_outside_the_allow_list_reaches_a_host_cli`. |
| S77-04 | Closed | The scan test now has a `software-factory.old` sibling. Reviewer RM2 now fails `test_the_scan_honours_each_kind_of_allow_entry`. |
| S77-05 | Closed | Two new fake modes, `disabled` and `flagless`. Reviewer RM4 (`enabled is not False`) now fails `test_an_entry_that_does_not_say_it_is_enabled_is_not_enabled`. |
| S77-06 | Closed | Ticket item 5 and the dispatch `run_root_rule` now name `C:/Temp/claude/<run id>`. The run roots used were `C:\Temp\claude\jas77-r2-L1` and `-L2`. |
| S77-07 | Closed | Ticket item 2 now says `JOHNNY_ROOT=<step>/root`, checked empty, with the downloads in `<step>/download`. The code was already correct. |
| S77-08 | Closed | Ticket item 2 now states the installer's environment. The test asserts the environment's names ⊆ allow-list ∪ {`HOME`, `GIT_*`, `DISABLE_AUTOUPDATER`, `JOHNNY_ROOT`}, with no `USERPROFILE` and `HOME=<step>/home`. Reviewer RM7 (keep `USERPROFILE`) is red. |
| S77-09 | Closed | The install now runs with `cwd=ctx.step_dir`, and the wrapper is `.resolve()`d. The test asserts the working directory and an absolute wrapper. Reviewer RM6 (back to `cwd=downloads`) is red. |
| S77-10 | Closed | The STATEMENT names `C:\Temp\claude\jas77-r2-L1` and `-L2`, the same names the raw blocks show. |
| S77-11 | Carried | Hardening: the residue match is case-sensitive. It is not part of this correction, and it does not block. |

### Findings of this round

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S77-12 | `EVIDENCE_DEFECT` | Medium | `tests/test_acceptance_lifecycle.py` `LifecycleCase.run_script` (`mock.patch.object` of `LEVEL2_ASSETS`, `OLD_MARKETPLACE_COMMIT`, `OLD_PINNED_COMMIT`); `lifecycle.py` lines 170 and 178–181 | **The ticket's literal identities are not pinned by any test.** Every lifecycle case patches the 0.4.9 sha256 values and the two 0.4.14 commits with fixture values, and no test compares the production constants with the ticket's text. A wrong `OLD_PINNED_COMMIT`, or a changed approved digest of the downloaded installer, stays green. The installer is the executable whose `INSTALL` prompt the script answers. For `0b3afd36` this is a regression made by this correction: in revision02, the fake Claude CLI wrote the literal `0b3afd36…`, so the constant was pinned through it. In revision03 the fake receives the patched value instead. The sha256 door was open already in revision02. My round-1 check 9 confirmed the values by reading them but did not mutate them, so I missed it then. | Reviewer **RM8**: `OLD_PINNED_COMMIT` → `"1"*40` gives **58 passed, exit 0**. Reviewer **RM9**: the zip's approved sha256 `2365b6f7…` → `3365b6f7…` gives **58 passed, exit 0**. Both counts are zero red, judged on unfiltered output (`M-reviewer-rev03.txt`). The source has no other occurrence of `0b3afd36`, `01b810f0`, `2365b6f7` or `906b0672`. | Add one unpatched test, like `TICKET_ENV_ALLOW_LIST`, asserting the ticket's literals: `OLD_PINNED_COMMIT == "0b3afd3645946f97662c336f0e6ac0dcae502e69"`, `OLD_MARKETPLACE_COMMIT == "01b810f096b1201005d26922e2c8a474bdd5a0a0"`, `CLAUDE_OLD_MARKETPLACE_URL` equal to the ticket's URL, and `LEVEL2_ASSETS` equal to the two ticket digests (and `LEVEL2_RELEASE_URL`). No new mechanism. |
| S77-13 | `OUT_OF_SCOPE_HARDENING` | Low, for the owner before any pin move | ticket item 2 `uninstall` (residue allow-list) and `recover` ("exactly one entry"); `ci/acceptance/README.md` host versions and local-run commands | **Claude Code 2.1.332 behaves differently from the pinned 2.1.316.** Per the seat, `.claude.json` gains `"declinedPlugins": ["software-factory@software-factory"]` after uninstall, and `plugin list --json` lists four `@builtin` entries. This does not violate the current closure. The README and the workflow pin 2.1.316, and the cloud run installs 2.1.316 from npm with `DISABLE_AUTOUPDATER=1`. Both behaviours are host bookkeeping, not plugin residue. They would turn `uninstall claude` and `recover claude` red if the pin moved. A local run on this host now also depends on putting the pinned binary first on `PATH`, which the README's local-run commands do not say. | The reviewer's V2 run (`--host claude --steps build,fresh`, host `claude` 2.1.332, run root `C:/Temp/claude/R77-2-fresh`) gives build and fresh `PASS`. Its `plugin list --json` shows `cc-plugin-agents-md@builtin` beside `software-factory@software-factory` (the rest is cut off by the report's excerpt), which confirms the `@builtin` half. The `declinedPlugins` half is the seat's evidence alone: the reviewer's permission covered `build,fresh` only. | This is not decided here. Before moving the pin, the owner decides two things. First, a `line \| claude \| .claude.json \| <reason>` allow-list entry; note that a `line` entry admits every line of that one file, which is broad, and anything narrower would be a new mechanism. Second, rewording `recover` to "exactly one entry outside the host's `@builtin` plugins", which is a one-line filter in `step_recover`. Until then, `ci/acceptance/README.md` should say that the local run needs the pinned `claude` first on `PATH`. |

### Checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Codex upgrade against revision03 item 2 | PASS | See S77-01 above. One more point: for Codex, `old_install` keeps the read-back of `johnny-ai-skill` 0.4.14 installed and enabled. |
| 2 | Level 2 environment and working directory | PASS | `cwd=ctx.step_dir` for both the install and the uninstall, and the wrapper path is absolute. The environment is `build_environment` with `JOHNNY_ROOT` and with `USERPROFILE` omitted. `INSTALL` goes to `stdin` at exactly one call site, after the empty-root check. RM6 and RM7 are red. |
| 3 | RM1, RM2 and RM4 again | PASS | Each turns one test red (baseline 58 passed). |
| 4 | New doors | RM5, RM6, RM7 red; RM8, RM9 zero red (S77-12) | Nine reviewer mutations, each run on the full file, in a disposable `--no-hardlinks` clone, with unfiltered output read directly and porcelain 0 after each. The capture is `M-reviewer-rev03.txt`. |
| 5 | Boundary | PASS | See S77-02 above. |
| 6 | Local run with the copied 2.1.316 binary | Faithful, and truly stated | The README and the workflow pin 2.1.316, and the ticket requires the run versions to be read and stated. Every L1 `claude` argv is `C:\Temp\claude\jas77-r2-claude316\claude.EXE`, and `--version` prints `2.1.316 (Claude Code)`. The STATEMENT (item 1) and the record name the copy, its source (`~/.local/share/claude/versions/2.1.316`, a program directory and not a configuration directory, which holds `2.1.316` and `2.1.332`), the run-id directory, and the two 2.1.332 failures. Nothing was downloaded. The host's `~/.local/bin/claude.exe` reports `2.1.332`. |
| 7 | L1, L2 and the record | PASS | L1 exits 0 with ten `PASS` verdicts. Each row carries the read-back its rule needs. Codex upgrade: `cat-file` 1026 bytes, add of `marketplace-0414`, `plugin add` 0.4.14, `rev-parse` `0b3afd36…`, removal, local install, and both lists. L2: build `PASS`, codex-ref `NOT_SUPPORTED` (`invalid marketplace source format`), codex-files `PASS`. The record matches the receipt. |
| 8 | The foreign pytest at F1 | Acceptable, truly stated | pid 37340 ran a pytest from `C:\Temp\codex\vd2-026-c10\…` against `C:/VerifyPool/slot-6`, a different checkout, so it is not the same-checkout C1/B2 family. The STATEMENT names it, as the F1 assert requires. F1 shows only the one registered failure. |
| 9 | Receipt truth | PASS | P1 rerun: 169 passed, 392 subtests, the same as the receipt. T1 rerun: `Success: no issues found in 2 source files`. M1: the seat's eight mutations are each red. C1: run 45740935047 has headSha `9d4ccf63`, conclusion success, and both jobs success (`gh run view`). E1 rerun with `--candidate 9d4ccf63`: `cells=9 defects=0`, exit 0. `RETURN.md` differs from `RETURN.as-returned.md` only by the USAGE cell. `items: 13` matches the 13 items. Residue: no `jas77-r2*` under `C:/Temp/claude`, scratch is empty, and there is no host lock. |
| 10 | P0 types | PASS | `mypy --strict` is clean. There is no `Any` and no `type: ignore`. |
| 11 | Full suite | Not rerun | No host lock was taken. The seat's F1 and both CI jobs cover it. |

Disclosure: once, outside `lifecycle.py`, I ran `~/.local/bin/claude.exe --version` directly to read the host's version. No other host command ran outside the script. No prompt, session or login ran, and the user's configuration was not read or written.

### Verdict

`CHANGES_REQUESTED`. Every revision02 finding except the carried hardening S77-11 is closed, and L1 now meets condition (3). One gap is open: S77-12. The test does not pin the ticket's commits or the approved installer digests, and the `0b3afd36` pin was lost by this correction. Closing it takes one assertion test, added as an additive commit on the same branch. S77-13 goes to the owner, with no change to this closure.

```review-verdict
candidate: 9d4ccf63f1d9632c430d5f50dcb36d567bbda14f
verdict: CHANGES_REQUESTED
round: initial
closure_revision: revision03
reviewer: ticket-review seat R77-2 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 9d4ccf63f1d9632c430d5f50dcb36d567bbda14f
round: 3
kind: INITIAL
verdict: CHANGES_REQUESTED
causes: IMPLEMENTATION_DETAIL
```

### Residue (R77-2)

Removed: `C:/Temp/claude/R77-2-fresh`, `C:/Temp/claude/R77-2-mypycache`, and every `R77-2-*` entry in `.worktrees/77-acceptance-review-scratch` (the clone `R77-2-m`, the driver and boundary scripts, and the captures, which were copied here first as `M-reviewer-rev03.txt` and `V2-reviewer-rev03.txt`). `PROCESSES_LEFT=0`.

## Revision04 initial review

- Ticket: revision04, read at `origin/cp/wave3`. The ticket's last change is commit `2d6b25aa`.
- Dispatch: `JAS-77-3.yaml`. Its sha256 is `2d5bb809…eddec` (recomputed), the same digest as the state row.
- Owner decision: the REQ-043 row "Owner decisions 2026-11-26 (host CLI drift: relax; old and new must not fight, "A")".
- Candidate: `2290bf4fac5d688cd21b31d9d84869708d34784a`, two additive commits on `9d4ccf63`: `8bb57b56` (the fix) and `2290bf4f` (the record only).
  - Both are authored `Johnny Liu <johnny.liu365@gmail.com>`, with the trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
  - The candidate equals `origin/cp/wave3-77-acceptance`.
- Label: the initial review of closure revision04 (CodeReview §5).
- Reviewer: `ticket-review` seat, run id `R77-3` (claude-opus-5-5).

### Closure of the revision03 findings (diff `9d4ccf63..2290bf4f`)

| id | status | evidence |
| --- | --- | --- |
| S77-12 | Closed | `TicketLiteralTests` compares the unpatched constants with the ticket's literals: `OLD_PINNED_COMMIT`, `OLD_MARKETPLACE_COMMIT`, `CLAUDE_OLD_MARKETPLACE_URL`, `LEVEL2_RELEASE_URL`, both `LEVEL2_ASSETS` digests, the versions and `LEVEL2_CONFIRMATION`. Reviewer RM8 now fails `test_the_old_install_commits_and_url_are_the_tickets`. Reviewer RM9 now fails `test_the_level2_assets_and_their_digests_are_the_tickets`. |
| S77-13 | Closed, now in scope under the owner's relax decision | **Pins:** the README and the workflow say `claude` 2.1.332 and `codex` 0.166.0. In L1, every `--version` printed `2.1.332 (Claude Code)` from `~/.local/bin/claude.EXE` and `codex-cli 0.166.0` (four times each), with no copied binary. `npm view` confirms both versions exist. **Residue:** a `key` entry `key \| claude \| .claude.json#declinedPlugins \| the host's own decline record (owner decision 2026-11-26, 放寬)`. This is the reason text revision04 item 2 words. **Reinstall:** after the scan, `install_from_local` and `require_listed(… "after the reinstall" …)`. **recover:** the count excludes ids that end in `@builtin`. My V3 run (`--host claude --steps build,fresh,uninstall`, host `claude` 2.1.332, run root `C:/Temp/claude/R77-3-V3`) gives all three `PASS`, with evidence "no residue … outside the 3 allow-listed entries" and "after the reinstall: … 0.5.0 … enabled=True". Afterwards the step's `.claude.json` has the top-level key `declinedPlugins`, which the reinstall had emptied to `[]`. I did not see the record's value at scan time; that it held the plugin id is the seat's evidence. |
| S77-11 | Carried | Hardening: the residue match is case-sensitive. It is not part of this correction. |

### Findings of this round

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S77-14 | `EVIDENCE_DEFECT` | Low | `tests/test_acceptance_lifecycle.py` `test_a_key_entry_admits_one_top_level_value_and_is_not_a_line_rule`; `lifecycle._admitted_keys` | Revision04 item 2 limits the `key` entry to `.claude.json` **under the step's `CLAUDE_CONFIG_DIR`**. The code is correct: it compares the target with the path relative to the step directory (`file_part == relative`). But no test puts a second `.claude.json` deeper in the tree, so matching by file name alone would pass. A regression would then admit the `declinedPlugins` value of any nested `.claude.json`, for example one in a cache or project directory. | Reviewer **KR1**: `file_part == relative` → `file_part == relative.rsplit("/", 1)[-1]` gives **65 passed, exit 0** (zero red). The output was unfiltered (`M-reviewer-rev04.txt`). | In that test, write `sub/.claude.json` holding `{"declinedPlugins": ["software-factory@software-factory"]}` and assert `line sub/.claude.json:…` is a finding. |
| S77-15 | `EVIDENCE_DEFECT` | Low | `tests/test_acceptance_lifecycle.py` fake mode `extra`; `step_recover` filter | The `@builtin` filter is correct: `endswith("@builtin")`. My probe confirms that `builtin-tool@elsewhere` and `a@builtins` are kept and only `x@builtin` is dropped. But the "second entry fails" test uses `other@elsewhere`, which contains no `builtin`, so matching by substring would pass. A regression would hide a non-builtin plugin whose name contains `builtin`. This answers the coordinator's question: as committed, no such plugin is hidden; the property is just not pinned. Note: an entry from a marketplace literally named `builtin` is dropped by design. That matches the ticket's wording "the host's `@builtin` plugins", and the isolated step adds no such marketplace. | Reviewer **BR1**: `not item.plugin_id.endswith(BUILTIN_SUFFIX)` → `"builtin" not in item.plugin_id` gives **65 passed, exit 0** (zero red). | Rename the `extra` fake entry to `builtin-helper@elsewhere`, or add a second extra entry with that name. The existing assertion that `recover` fails then pins it. |
| S77-16 | `OUT_OF_SCOPE_HARDENING` | Low | `lifecycle._lines_outside_keys` | Once a `key` entry applies, the file is judged through `json.loads` and then re-serialized. Python keeps the last value of a duplicated key, so `{"declinedPlugins": […], "x": "software-factory", "x": "ok"}` gives no finding. Without the entry, the raw line is a finding. Hosts write `.claude.json` through a serializer, so this does not violate the current closure. | Reviewer probe: `scan_residue` with the entry → `[]`; without the entry → `['line .claude.json:1']`. | Follow-up hardening: `json.loads(…, object_pairs_hook=…)` that raises on a duplicate key, so `_lines_outside_keys` returns `None` and the raw lines are judged. |

### Checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | `key` kind against revision04 item 2 | PASS in code; S77-14 test gap | The target is `.claude.json#declinedPlugins`, host `claude`, and the path is relative to the step directory (= `CLAUDE_CONFIG_DIR`). Only the top-level key is removed: the nested same-name key is still judged (reviewer KR2 red). Other keys and lines are judged (reviewer KR3 red). A file that is not a JSON object falls back to raw lines, which fails closed. A `key` target without `#` admits nothing. |
| 2 | Reinstall with the record present, and the `@builtin` filter | PASS; S77-15 test gap | Reviewer RI1 (reinstall dropped) is red. BR2 (filter to `@software-factory` only) is red. BR1 is zero red (S77-15). |
| 3 | Pins and workflow | PASS | The pins equal the printed versions, and a test compares README and workflow. The workflow diff since `504e5177` is that single `npm install` line. The trigger is still `workflow_dispatch` only, with `permissions: contents: read`, the same three SHA-pinned actions, `fetch-depth: 0`, `persist-credentials: false`, and no secret or token name. |
| 4 | Earlier mutations | PASS | RM1, RM2, RM4, RM8 and RM9 each turn one test red (baseline 65 passed). Each mutation ran on the full file, in a disposable `--no-hardlinks` clone, with porcelain 0 after each. |
| 5 | Boundary | PASS | `read_boundary(revision04)` → `DECLARED`. The diff `f53ecc6a..2290bf4f` is five `CREATE 100644` changes, each admitted, and `evaluate_changes` gives `(None, None)`. |
| 6 | Local run (L1, L2) and record | PASS | L1 exits 0 with ten `PASS` verdicts, using the host's own CLIs. L2: build `PASS`, codex-ref `NOT_SUPPORTED`, codex-files `PASS`. The record carries both versions and says the candidate differs from `8bb57b56` only by the record, which is true (`git diff --stat`). |
| 7 | Receipt truth | PASS | P1 rerun: 176 passed, 392 subtests, the same as the receipt. T1 rerun: `Success: no issues found in 2 source files`. M1: the seat's thirteen mutations are each red. C1: run 45746324457 has headSha `2290bf4f`, conclusion success, both jobs success. E1 rerun with `--candidate 2290bf4f`: `cells=9 defects=0`, exit 0. `RETURN.md` differs from `RETURN.as-returned.md` only by USAGE. The foreign pytests at F1 are named in the STATEMENT, as the F1 assert requires, and F1 shows only the registered failure. `items: 13` matches the 13 items. There is no `jas77-r3*` residue under `C:/Temp/claude`. |
| 8 | P0 types | PASS | `mypy --strict` is clean. There is no `Any` and no `type: ignore`. |
| 9 | Full suite | Not rerun | I took no host lock and did not touch the `integ-80` lock. The seat's F1 and both CI jobs cover the suite. |

Host commands: only through `lifecycle.py` (V3), so only `--version`, `plugin` and `plugin marketplace`. No prompt, session or login ran, and the user's configuration was not touched.

### Verdict

`CHANGES_REQUESTED`. S77-12 and S77-13 are closed, and the candidate's behaviour matches revision04 item 2 word for word. Two properties that revision04 states are not pinned by a test, and each of my counter-mutations on them left all 65 tests passing:
- S77-14: the `key` entry applies only to `.claude.json` at the step root;
- S77-15: the `@builtin` filter matches the suffix, not a substring.

Each needs a one-line test change, added as an additive commit on the same branch. S77-11 and S77-16 are hardening and do not block.

```review-verdict
candidate: 2290bf4fac5d688cd21b31d9d84869708d34784a
verdict: CHANGES_REQUESTED
round: initial
closure_revision: revision04
reviewer: ticket-review seat R77-3 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 2290bf4fac5d688cd21b31d9d84869708d34784a
round: 4
kind: INITIAL
verdict: CHANGES_REQUESTED
causes: IMPLEMENTATION_DETAIL
```

### Residue (R77-3)

Removed: `C:/Temp/claude/R77-3-V3`, `C:/Temp/claude/R77-3-mypycache`, and every `R77-3-*` entry in `.worktrees/77-acceptance-review-scratch` (the clone `R77-3-m`, the driver, boundary and probe files, and the captures, which were copied here first as `M-reviewer-rev04.txt` and `V3-reviewer-rev04.txt`). `PROCESSES_LEFT=0`.

## Revision04 correction review

- Candidate: `8cf1e387d38ad7a346582586f17e3f27034bb402`, one additive commit on `2290bf4f`.
  - It is authored `Johnny Liu <johnny.liu365@gmail.com>`, with the trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
  - It equals `origin/cp/wave3-77-acceptance`.
- Label: the correction review of closure revision04. CodeReview §5 rule B applies.
- Reviewer: `ticket-review` seat, run id `R77-4` (claude-opus-5-5).

### Closure of the revision04 initial-review findings

| id | status | evidence |
| --- | --- | --- |
| S77-14 | Closed | The key-scan test writes `.claude.json` at the step root and `sub/.claude.json`, each with `declinedPlugins` naming the plugin. It asserts there are findings and that every one is `line sub/.claude.json:…`, so the file at the root is admitted and the nested one is not. I reran KR1 (any file of that base name): `1 failed, 64 passed`. The failure is in `test_a_key_entry_admits_one_top_level_value_and_is_not_a_line_rule`, with `AssertionError: [] is not true`, which is the intended reason. |
| S77-15 | Closed | The fake `extra` entry is now `builtin-helper@elsewhere`. I reran BR1 (`"builtin" not in id`): `1 failed, 64 passed`. The failure is in `test_a_second_entry_that_is_not_builtin_fails_recover`, with `AssertionError: 0 != 1`, because `recover` passed with the extra entry hidden. That is the intended reason. Baseline: 65 passed. Output unfiltered, in `M-reviewer-rev04-correction.txt`. |
| S77-11, S77-16 | Carried | Hardening, not touched by this correction. Neither blocks. |

### Findings of this round

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S77-17 | `OUT_OF_SCOPE_HARDENING` | Low | `doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md` line 40 | The record says the receipt's candidate "differs by this record only" from `8bb57b56`. Since `8cf1e387`, the candidate also differs by one test commit. The substantive claims are still true: `lifecycle.py` is unchanged since `8bb57b56` (`git diff 2290bf4f 8cf1e387` touches only `tests/test_acceptance_lifecycle.py`), and L1 and L2 were repeated at the candidate with the same verdicts. Closure item 6 (the record starts with the local run) is not violated. | `git diff --stat 2290bf4f 8cf1e387`: one file, the test, 6 insertions and 1 deletion. | When the control plane next edits the record (the cloud-run section), say "it differs by this record and by test changes". |

### Checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Diff scope | PASS | `git diff 2290bf4f 8cf1e387` touches only `tests/test_acceptance_lifecycle.py`. It changes two test data lines and adds one assertion block. There is no production or record change. No new defect is in the diff. |
| 2 | P1, T1 | PASS | P1 rerun: 176 passed, 392 subtests, the same as the receipt. T1 rerun: `Success: no issues found in 2 source files`. |
| 3 | CI | PASS | Run 45752942946 has headSha `8cf1e387`, conclusion success, and both jobs success. Its log has no `UNREGISTERED_FAILURE`, `REGISTERED_NOT_FAILING` or `REGISTERED_NOW_PASSING`. |
| 4 | Receipt and STATEMENT | PASS | E1 rerun with `--candidate 8cf1e387`: `cells=9 defects=0`, exit 0. `RETURN.md` differs from `RETURN.as-returned.md` only by USAGE. L1 at `C:\Temp\claude\jas77-r4-L1` has ten `PASS` verdicts and exit 0. In L1, `--version` printed `2.1.332 (Claude Code)` and `codex-cli 0.166.0` four times each, from the host's own `~/.local/bin/claude.EXE`. M1 shows the baseline (65 passed) and 15 mutations, each red, with the exit list `0,1×15`. The STATEMENT describes the host lock truly: the seat waited for another seat's `r81a` lock and named the foreign pytest 51444. There is no `jas77-r4*` residue, and the seat's scratch is empty. `items: 13` matches the 13 items. |

I took no host lock and did not touch the `integ-81` lock. Host commands: none (no `lifecycle.py` run was needed for a test-only diff).

### Verdict

`APPROVED`. S77-14 and S77-15 are closed, and the reruns of KR1 and BR1 now fail their tests for the intended reasons. The diff is limited to the test file. P1, T1, CI and E1 hold. The remaining items S77-11, S77-16 and S77-17 are hardening and do not block. Under the review label rule this is the one correction review of revision04.

```review-verdict
candidate: 8cf1e387d38ad7a346582586f17e3f27034bb402
verdict: APPROVED
round: correction
closure_revision: revision04
reviewer: ticket-review seat R77-4 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 8cf1e387d38ad7a346582586f17e3f27034bb402
round: 5
kind: CORRECTION
verdict: APPROVED
causes:
```

### Residue (R77-4)

Removed: `C:/Temp/claude/R77-4-mypycache`, and every `R77-4-*` entry in `.worktrees/77-acceptance-review-scratch` (the clone `R77-4-m`, the driver, and the capture, which was copied here first as `M-reviewer-rev04-correction.txt`). `PROCESSES_LEFT=0`.

## Seat token use (readiness criterion 5)

Host-reported usage per seat, summed per unique message id, against the expectation the owner confirmed on 2026-11-18 ("1A"); appended to the receipt as `USAGE` cells at integration.

| Seat | Model | input | cache write | cache read | output | processed | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seat:implementation-standard/JAS77R1` | claude-sonnet-5-5 | 564 | 1872598 | 98640156 | 312093 | 100513318 | OVER_OUTPUT,OVER_PROCESSED |
| `seat:ticket-review/R77` | claude-opus-5-5 | 234 | 1731437 | 28150212 | 115196 | 29881883 | OVER_OUTPUT,OVER_PROCESSED |

## Seat use against the expectation (control plane, 2026-11-26)

Both seats are over the repository's expectation: implementation `OVER_OUTPUT,OVER_PROCESSED` (output 312093, processed 100513318), review `OVER_OUTPUT,OVER_PROCESSED` (output 115196, processed 29881883). The cause is the ticket's shape, not drift. Ticket 77 ran four closure revisions (revision01 to revision04) in one seat each, because two owner decisions came out of its own evidence:
- the Codex 0.4.14 zeros pin (CHANGE_DETECTED);
- the host CLI moving to 2.1.332.

Each revision reran the full local lifecycle on both hosts, plus a full suite. Wave 4's T13 (the full suite where it pays) and T15 (a rule-only review before every dispatch) address the cost. The carried items are:
- S77-11: case-insensitive residue match;
- S77-16: refusing duplicate JSON keys;
- S77-17: the record's "differs by this record only" wording.

## Initial review of closure revision06

- **Ticket.** Revision06 of ticket 77, read with `git show bc8da7bd:modules/tickets/workflow-governance/77-acceptance-0-5-0.md`. At `62ebc5fb` (and at `bfc02590`) the ticket differs only in its state row, which carries the dispatch digest `859c470c…6e72a4d2ec`. `JAS-77-4.yaml` from `62ebc5fb` hashes to that value. Sections read: the Revision05 paragraph, item 7 (7a to 7e and the indent rule), the Owner override record, TDD item 4, the revision05 mutations, L3, D1, the boundary block and 禁止修改; items 3 to 5 for context. Revision05 reopens the ticket after `INTEGRATED` by owner override, so this is a new closure revision and the §5 count restarts.
- **Candidate.** `ec0c06dcc0d92663617067d3cd79819575c67905`, equal to `origin/cp/wave3-77-acceptance`. It is one commit on `8cf1e387` (the revision04 approval, integrated at `e87bc5cb`), and `f53ecc6a` (the dispatch base) is its ancestor. The commit is authored `Johnny Liu <johnny.liu365@gmail.com>`. Its subject is the dispatch's commit line, and its trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` matches the dispatch model `claude-sonnet-5-5` and the USAGE cell `seat:implementation-standard/JAS77R6`.
- **Label.** Initial review of closure revision06. Process tier: strict.
- **Reviewer.** Independent `ticket-review` seat, run id `R77-6` (claude-opus-5-5). After a fetch, the worktree `.worktrees/77-acceptance-review` was detached from `8cf1e387` to the candidate. Porcelain was empty before and after.
- **Captures.** Everything is in `.worktrees/77-acceptance-review-out/r06/`, together with the scripts that produced it:
  - `exact-texts.txt` (`exact_texts_r06.py`);
  - `M1-review.txt` and `M1-driver.txt` (`counter_mutations_r06.py`, `counter_mutations_r06.sh`);
  - `P1-review.txt`, `T1-review.txt` and `lock-log.txt` (`p1_t1_r06.sh`);
  - `C1-review.txt` and `ci-scan.txt`;
  - `E1-review.txt`;
  - `L3-seat-read.txt` and `L3-review-read.txt` (`l3_read_r06.py`), `L3-review.txt` and `parity-after.txt` (`parity_r06.sh`);
  - `boundary-review.txt` (`boundary_r06.py`).

### Findings (revision06)

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S77-18 | `IMPLEMENTATION_DEFECT` | Low | `tests/test_acceptance_lifecycle.py` line 1196, in `test_the_step_installing_the_development_requirements_has_the_run_lines_of_ci_yml` | Item 7d says the step's `run` lines equal those of `ci.yml`'s step, "read from `ci.yml` and not written a second time in the test". The test does read them from `ci.yml`. Then it adds `self.assertEqual(mine[-1], "python -m pip install -r requirements-dev.txt")`, which writes one of those `run` lines in the test a second time. That is a second source for the line. If `ci.yml` changes its install line and `acceptance.yml` follows, the test goes red, though 7d makes `ci.yml` the only source. The candidate's behaviour is correct, and the extra line makes no test weaker. The deviation is from the frozen wording of 7d. | The line quoted. The equality alone already turns every mutation of the frozen list red. Seat mutation 4 and my CM10 (only `ci.yml` changed) are red through `assertEqual(mine, theirs)` (`M1-review.txt`). | Delete line 1196. If the control plane wants to keep a literal pin on `requirements-dev.txt`, that is a change to 7d (a ticket edit), not to the candidate. |
| S77-19 | `OUT_OF_SCOPE_HARDENING` | Low | `tests/test_acceptance_lifecycle.py` lines 1107–1118 (`step_run_lines`) and 1191–1214 | Item 7a says the step is exactly its four lines and "Nothing else in the workflow changes". The tests pin the step's name, its `run` lines and its place, but not that the step has no other key. Adding `if: ${{ false }}` after the `run` lines disables the install, and all 69 tests stay green (CM8). So does `continue-on-error: true` (CM9). At this candidate the step is byte-exact (check R1). The gap is only regression protection: if this regressed, a workflow that does not install `requirements-dev.txt`, the failure of run 45920193720, would pass. | CM8 and CM9 in `M1-review.txt`: each shows `69 passed`, `exit=0`. | In the same test, assert that the line after the last `run` line starts a new step (`      - ` or `      # `) or ends the file, so the step holds no key beyond `name` and `run`. This is one assertion and no new mechanism. It can ride with S77-18's correction. |
| S77-20 | `OUT_OF_SCOPE_HARDENING` | Low | `tests/test_acceptance_lifecycle.py` lines 1253–1277 | Two properties of the frozen README text are not pinned. First, 7b's place: the sentence must stay on the line that begins `one). `, in section "The local run (condition 3)", but `assertIn` on the whole text accepts the sentence anywhere. Moving it to the Isolation section stays green (CM7). The ticket chose `assertIn` itself ("the 7d test checks it with `assertIn` on the README text as read"), so the candidate meets 7d. Second, 7c's first install line: removing `py -3.11 -m venv <A>` from the parity block stays green (CM12). 7d does not list it. | CM7 and CM12 in `M1-review.txt`: each shows `69 passed`, `exit=0`. | Carry the item to the follow-up hardening ticket. There, match `^one\). ` followed by the escaped sentence and `$` as a whole line, and add `"\npy -3.11 -m venv <A>\n"` to the section's `assertIn`s. |

Notes. None of these is a finding.

- **N12. The merge base has moved, as for ticket 82 (N10 there).** The candidate's merge base with `origin/cp/wave3` (`bfc02590`) is now `8cf1e387`. Over `8cf1e387..ec0c06dc`, `evaluate_changes` gives `MODIFICATION_OUTSIDE_BOUNDARY` for `.github/workflows/acceptance.yml`, because the boundary lists the three files under `create` only. The Owner override record says the `create =` lines "still describe the diff from that base" (`f53ecc6a`). Over `f53ecc6a..ec0c06dc` the gate gives `(None, None)`: five `CREATE` entries. I judged that range. If the gate must judge this reopened ticket against `cp/wave3`, the fix is in the ticket: add the three files to `modify`.
- **N13. `tool_digest` also names `dispatch_lint.py`.** E1 names only `index_pins.py` and `receipt_fence_check.py`. All three digests equal the blobs at the candidate. The revision04 receipt carries the same three. E1 accepts it.
- **N14. The npm postinstall is not covered.** Under this host's npm 11.16.0, the `--prefix` line prints an `allow-scripts` warning, and `@anthropic-ai/claude-code@2.1.332`'s `postinstall: node install.cjs` does not run. That happened in both the seat's run and mine. `claude.CMD` still printed `2.1.332 (Claude Code)` and passed every step. The runner's `npm install --global` may run that script. 7c and 7e do not ask about it, and the parity run cannot show the difference. The control plane may want to name it next to the README's `py` launcher sentence.
- **N15. The seat's discarded first parity run.** The STATEMENT says the first run resolved the host's own `claude.EXE` and `codex.EXE` (codex 0.172.0) because of the `PATH` form. It says that run was removed and redone. L3 holds only the second run, and my reading of it agrees (check R6).
- **N16. The seat's mutation 5 appends rather than restores.** It adds " This or any Python 3.11 will do." after the 7b sentence, so only the `assertNotIn` fires. TDD item 4's other half, "the 7b sentence removed", is covered by my CM6 (the revision04 sentence restored): red on the `assertIn`.
- **N17. `requirements-dev.txt` pins `pydantic>=2.12.2,<3`, not one version.** My parity venv got `pydantic 2.14.4`. The runner gets whatever is newest in that range. That is `ci.yml`'s own state, and revision05 does not touch it.

### Per-check table (revision06)

| # | Check | Result | Evidence and notes |
| --- | --- | --- | --- |
| R1 | Diff and exact texts (D1, 7a, 7b, 7c) | PASS | `git diff 8cf1e387 ec0c06dc` changes exactly `.github/workflows/acceptance.yml` (+4), `ci/acceptance/README.md` (+24 −1) and `tests/test_acceptance_lifecycle.py` (+77). I took the 7a and 7c blocks from the ticket blob and removed the five-space list indent. The candidate workflow equals the revision04 file with the 7a block inserted after setup-python's `with:` block (lines 37–39). The block is lines 40–43 and the host-CLI step follows at line 44. The step's `- name:` line has six spaces. Those four lines equal `ci.yml` lines 45–48. The candidate README equals the revision04 README with two changes and nothing else: the old sentence is replaced in place by 7b, and the 7c block plus one blank line is inserted before `## Isolation`. 7b is line 30, the only line that begins `one). `, unwrapped, inside `## The local run (condition 3)`. `## The parity run` is line 53 at column 1, once, and `## Isolation` is line 76. "or any Python 3.11" is absent. Neither file has a CR. `exact-texts.txt` |
| R2 | The four new tests against 7d | PASS (S77-18) | The first test reads `run` lines from both workflows with `step_run_lines`, which requires the name line once, then `        run: |`, then the 10-space body. It compares them with `assertEqual`. The second test compares the line numbers of setup-python, the step, the host-CLI step, `Run the lifecycle` and the one `python ci/acceptance/lifecycle.py` line. Each comes from `line_number`, which requires exactly one whole-line `re.MULTILINE` match. The third test uses `assertIn` on the 7b sentence and `assertNotIn` on "or any Python 3.11". The fourth test checks heading before Isolation as whole lines, the `<A>` pip line as a whole line inside the section, exactly one `npm install --prefix <B>` line, and its two `package@version` items. Those items must equal, in order, the two of the workflow's one `npm install --global` line, which is read from the workflow. Line 1196 is the extra literal of S77-18. |
| R3a | The seat's M1 | PASS | Baseline 69 passed. Mutations 1 to 7 each show `exit=1`, the intended test names, an `AssertionError` for the intended reason and `porcelain-lines-after-restore=0` (read in full in `77-acceptance-out/M1.txt`). |
| R3b | My counter-mutations | PASS with S77-19, S77-20 | I ran them in a disposable `git clone --no-hardlinks` copy at `ec0c06dc`, using the whole test file, not `-x`. The output was unfiltered: I ran pytest directly with `-rfE` and no wrapper. The unmutated baseline is 69 passed. Porcelain was 0 after each restore. **Red:** CM1, the step's `run` body emptied (`Lists differ: [] != [...]`). CM2, the step duplicated after the lifecycle step (2 failed, "matches 2 lines" and "not in the workflow exactly once"). CM3, the 7b sentence wrapped. CM4, the heading indented ("matches 0 lines"). CM5, the codex package dropped from the `--prefix` line. CM6, the revision04 sentence restored. CM10, the copy door: only `ci.yml` changed, which proves the comparison reads `ci.yml`. CM11, the first-match door: a second `--prefix` line with codex 0.165.0 (`2 != 1`). CM13, the `<A>` pip line pointed at `requirements.txt`. CM14, a trailing space on the step's name line. CM15, the step moved before setup-python (`41 not less than 36`). **Green**, and each matters: CM7, the sentence moved out of its section (S77-20); CM8, `if: ${{ false }}` (S77-19); CM9, `continue-on-error: true` (S77-19); CM12, the venv line removed (S77-20). Environment door: a CRLF checkout (`core.autocrlf=true`, CR present in both files) gives 69 passed. `M1-review.txt` |
| R4 | P1 and T1 rerun, under the host lock | PASS | I held `C:/Temp/claude/jas-fullsuite.lock` as `R77-6`. I acquired it at 02:01:13Z and released it at 02:02:13Z by rename and remove, after `owner.txt` still named me. I took it again for the counter-mutations and released it at 02:18:03Z. At both acquisitions, the only other python processes were another project's (`test_week_templates_sql_020r.py`, PID 33784, and a `vita360 staging` guard, PID 40044). Neither runs in this repository's runtime root. The interpreter was `C:/Temp/claude/jas-venv/Scripts/python.exe` with `PYTHONUTF8=1`. P1 (four files, `-rfEs`): 180 passed, 392 subtests passed, exit 0, no skip, the same as the receipt. T1: mypy `--strict --python-version 3.11` on the two files gives "Success: no issues found in 2 source files", exit 0. `P1-review.txt`, `T1-review.txt`, `lock-log.txt` |
| R5 | CI read back | PASS | Run 45922292427 (workflow `ci`, branch `cp/wave3-77-acceptance`): `headSha` `ec0c06dc…`, conclusion `success`, and both `test (windows)` and `test (linux)` are `success`. The 14,993-line log has 0 `UNREGISTERED_FAILURE`, 0 `REGISTERED_NOT_FAILING`, 0 `REGISTERED_NOW_PASSING` and no `FAILED tests/test_acceptance_lifecycle`. The comparison step passed on both jobs. `C1-review.txt`, `ci-scan.txt` |
| R6 | L3 against 7e, the seat's cell and my own parity run | PASS | **Seat's cell:** the exits are `0,0,0,0` (the three install lines, then the lifecycle), and the 10 records are all `PASS`. The generator's `argv[0]` is `C:\Temp\claude\jas77r6-a1-venv\Scripts\python.exe` (under `<A>`). All 66 host commands are `claude.CMD` (35) or `codex.CMD` (31) under `C:\Temp\claude\jas77r6-a1-npm\node_modules\.bin`, each `--version` or `plugin …`. The `--version` records are `2.1.332 (Claude Code)` ×4 and `codex-cli 0.166.0` ×4. `L3-seat-read.txt`. **My parity run** followed README "The parity run" in the review worktree at the candidate. I used `<A>` `C:/Temp/claude/R77-6-A`, `<B>` `C:/Temp/claude/R77-6-B`, the run root `C:/Temp/claude/R77-6-run`, `--candidate ec0c06dc…` and `--expected-publication d355b4a2…`. `PATH` was exported inside the one script in the `/c/…` form. `command -v` and `shutil.which` from `<A>` both resolved the `.CMD` shims under `<B>` before the run. The three install lines exited 0, the lifecycle exited 0 with ten `PASS`, and `report.jsonl` has the same shape: the generator under `<A>`, 35 + 31 `.CMD` host commands under `<B>`, and the same versions. The publication commit regenerated as `d355b4a2…`. I then removed the three directories. `L3-review.txt`, `L3-review-read.txt`, `parity-after.txt` |
| R7 | E1, P9 and the receipt | PASS | I reran E1 as the dispatch gives it, with `--repo .worktrees/77-acceptance` (at `ec0c06dc`, porcelain empty) and `--candidate ec0c06dc…`, on the receipt as it stands with USAGE: `cells=9 defects=0`, exit 0 (`E1-review.txt`). All 9 evidence cells name the candidate. P9's capture reads `receipt defects: 0`, exit 0. `RETURN.md` differs from `RETURN.as-returned.md` only by the appended USAGE section. `items: 12` matches the 12 STATEMENT items. F1 was read, not rerun: 1 failed (`test_acr2_linux…`, registered), 3512 passed, 13 skipped. `77-acceptance-out-rev04/` holds the revision04 receipt (9 cells at `8cf1e387`), with every file timed at the 09:20:54 copy. No `jas77r6*` directory is left under `C:/Temp/claude/`, and the seat's scratch is empty. |
| R8 | The boundary and the revision05 limit | PASS (N12) | `git diff --name-status f53ecc6a ec0c06dc` shows five `A` entries, each a `create =` line of the boundary block. `read_boundary` at `bc8da7bd` and at `62ebc5fb` gives `DECLARED`, and the range gives `(None, None)`. The controls (`ci.yml`, `README.md`, `library/`, `skills/`, `CodeReview.md`) give `PATH_FORBIDDEN`. The blobs of `ci/acceptance/lifecycle.py`, `requirements-dev.txt`, `.github/workflows/ci.yml` and the acceptance record are unchanged since `8cf1e387`. `boundary-review.txt` |
| R9 | Merge into `origin/cp/wave3` | PASS | `git merge-tree --write-tree origin/cp/wave3 ec0c06dc` exits 0 with no conflict. Against `origin/cp/wave3` (`bfc02590`), the result changes only the three files, each equal to the candidate's. `cp/wave3` still holds `8cf1e387`'s copies of the six relevant files. Nothing was merged anywhere. `boundary-review.txt` |

Applicable references: `CodeReview.md`; `review-checks.md` (test truthfulness, with the reviewer counter-mutation, points 1 to 5). XSS: not applicable (no browser, WebView or DOM). Secret and external effect: the workflow holds no secret, and I did not run or dispatch it.

### Verdict (revision06)

`CHANGES_REQUESTED`. The fix itself holds under every independent rerun:
- the step is byte-exact and in its place;
- the README sentence and section are exact;
- the parity run passes with only what the workflow installs;
- P1, T1, CI and E1 hold;
- the diff stays inside D1 and the boundary.

The one item that asks for a correction is S77-18: the test writes a `ci.yml` run line a second time, which 7d forbids. The fix is to delete one line. S77-19 and S77-20 are hardening and do not block. S77-19's assertion is cheap enough to take in the same correction. Under the review label rule this is the initial review of closure revision06, and its correction review is the one that remains.

```review-verdict
candidate: ec0c06dcc0d92663617067d3cd79819575c67905
verdict: CHANGES_REQUESTED
round: initial
closure_revision: revision06
reviewer: ticket-review seat R77-6 (claude-opus-5-5)
reviewed_at: 2026-11-27
```

```rework-record
candidate: ec0c06dcc0d92663617067d3cd79819575c67905
round: 6
kind: INITIAL
verdict: CHANGES_REQUESTED
causes: IMPLEMENTATION_DETAIL
```

### Not done here, and why (revision06)

- **The full suite was not rerun.** It was not asked for; F1 was read from its capture.
- **The revision04 mutations were not rerun.** The ticket says three of them target `lifecycle.py`, which is unchanged, and that the push-trigger test is unchanged.
- **L1 and L2 were not rerun.** The ticket says they are not rerun in revision05. My parity run stands for the lifecycle at this candidate.
- **The control-plane list after integration is not done here.** It covers the control plane's own parity run at the integrated candidate, the fast-forward of `main`, the second cloud run and the owner-assisted session.

### Residue (R77-6)

- **Removed:**
  - `C:/Temp/claude/R77-6-A`, `R77-6-B` and `R77-6-run` (the parity run);
  - `C:/Temp/claude/R77-6-mypycache`;
  - the clones `R77-6-m` and `R77-6-crlf` and the CI log `R77-6-ci.log` under `.worktrees/77-acceptance-review-scratch/`, which is empty now;
  - the host lock, released twice by rename and remove, each time with `owner.txt` naming `R77-6`.
- **Left, with the reason:**
  - The npm cache (`%LOCALAPPDATA%\npm-cache`) and the pip cache (`%LOCALAPPDATA%\pip\Cache`), which the install lines and the 0.4.9 installer wrote. They do not carry my run id.
  - `%TEMP%` staging, which the installer removes itself.
  - The unreferenced tree objects that `git merge-tree --write-tree` wrote to the shared object store (result tree `7da816c3`). They are not referenced by any ref and are removed by `git gc`.
- **Not touched:** the candidate, the branch, the receipt, `77-acceptance-out-rev04`, the seat's worktree and the shared `publication-0.5.0` ref.
- PROCESSES_LEFT=0.
