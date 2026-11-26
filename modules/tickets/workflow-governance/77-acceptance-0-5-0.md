# 77｜Acceptance of 0.5.0: the install lifecycle in isolated directories, locally and once on a GitHub-hosted Windows runner

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner decisions 2026-11-19 "A" with conditions "1.2.3.4", 2026-11-19 on Level 2 and the Codex install path, 2026-11-20 on the release order and the rename, 2026-11-26 "B" on the cloud trigger） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision04 / receipt under `.worktrees/77-acceptance-out/` / owner implementation seat / worktree `.worktrees/77-acceptance` / branch `cp/wave3-77-acceptance` / baseline the wave-3 branch after ticket 71 is integrated |
| 實作語言 | Python 3.11 for the lifecycle script and its test; YAML for the workflow（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `REVIEW_APPROVED`; dispatch=sha256:2d5bb809e9c9f2db6a95a0330bd3d39aa40a3740c619a595b190435e32aeddec (`doc/handoffs/2026/workflow-governance/dispatch/JAS-77-3.yaml`)（candidate `8cf1e387`; correction review `APPROVED`） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/77-acceptance` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/77-acceptance-review` |
| 責任邊界 | one lifecycle script, its test, one `workflow_dispatch` workflow, and the acceptance record |
| 禁止修改 | the shipped manifests, `README.md`, `library/`, the gate scripts, the governance documents, `.github/workflows/ci.yml` |
| 環境 | `LOCAL` in isolated directories; one GitHub-hosted Windows run, triggered by hand after the four conditions hold |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
create = ci/acceptance/lifecycle.py
create = ci/acceptance/README.md
create = tests/test_acceptance_lifecycle.py
create = .github/workflows/acceptance.yml
create = doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md
modify = doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md
forbid = .github/workflows/ci.yml
forbid = .claude-plugin/
forbid = README.md
forbid = library/
forbid = skills/
forbid = AGENTS.md
forbid = Workflow.md
forbid = CodeReview.md
```

## 使用者拍板與可觀察結果

Process tier: strict.

Owner decisions this ticket carries out. Each is quoted in `REQ-20261103-043`, which is authoritative:

- **2026-11-19 "A", conditions "1.2.3.4":**
  - Fresh install, upgrade from 0.4.x, uninstall without residue, and recovery from a failed install run on a GitHub-hosted Windows runner.
  - The runner job runs once, and only when all four conditions hold: (1) ticket 71 is approved and integrated with its package check; (2) the job triggers by `workflow_dispatch` only, never on push; (3) each lifecycle step has passed locally in isolated directories; (4) the job itself has been reviewed.
  - A Codex session that loads 0.5.0, one test ticket through the new flow, and a resume from files after an interruption run on this host, with `CODEX_HOME` and `JOHNNY_ROOT` pointed at new empty directories. The Codex session uses the owner's login and starts only after the owner is told.
- **2026-11-19:** Level 2 does not ship; ticket 77 also tests the removal of an old Level 2 runtime.
- **2026-11-20, release order:** the cloud runner regenerates the same package from the candidate commit. For the upgrade step it first installs 0.4.14 from the public marketplace. Credentials are never copied into a new `CODEX_HOME`.
- **2026-11-26 "B":** a `workflow_dispatch` workflow runs only from the default branch, so the development `main` is fast-forwarded to `cp/wave3` before the cloud run. From then on, `main`'s marketplace is 0.5.0's, so the upgrade step reads 0.4.14 at a fixed commit. Until the release, a 0.4.14 user whose marketplace updates from `main` reads the 0.5.0 marketplace, whose source repository is not yet pushed, so that update fails; the owner accepted this (option B).
- **2026-11-26 "A" on S77R-01:** the 0.4.9 installer asks a person to type `INSTALL` (`v0.4.9` `install.ps1` line 100), and states that an agent's answer is not consent. The owner authorized `lifecycle.py` to answer that prompt on standard input, only for an install into an empty `JOHNNY_ROOT` made for this acceptance, on this host and on the runner. The authorization covers this test use only.
- **2026-11-26 "A" on the Codex upgrade:** the public 0.4.14 marketplace pins forty zeros, and Codex honours that `sha`, so 0.4.14 cannot be installed through Codex from there. Codex installs 0.4.14 instead from a local marketplace that holds the development repository's marketplace of that time (pin `0b3afd36`, source the public publication repository). This reproduces a user who already has 0.4.14.
- **2026-11-26 "放寬" on host CLI drift:** the host's Claude Code moved from 2.1.316 to 2.1.332 between two dispatches. Under 2.1.332, an uninstall leaves the host's own decline record (`declinedPlugins`) in its configuration, and `plugin list --json` shows the host's `@builtin` entries. Real users run the newest host, so the rules accept both. The plugin never edits the user's host configuration. A reinstall must still succeed while the record is present.

Ticket 71's rule-only review handed this ticket three checks that only running the CLIs can settle (`doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md`, S71R-19, S71R-20, S71R-21).

After this ticket:

1. **`ci/acceptance/lifecycle.py`.**
   - It uses only the standard library and passes `mypy --strict`.
   - It takes `--candidate <commit>`, `--expected-publication <commit>`, `--host claude|codex|both`, `--steps <comma list>` and `--run-root <empty directory>`. `build` and `level2` run once with `host` `none`; `codex-ref` and `codex-files` run for `codex` only; any other pairing is refused.
   - Every step gets its own new directory under the run root. For Claude Code that directory is `CLAUDE_CONFIG_DIR`; for Codex it is `CODEX_HOME`; for Level 2 it is `JOHNNY_ROOT`. The script refuses a run root that is not empty, and it never reads or writes the user's own configuration directories. The script also refuses a run root inside a Git work tree, and runs every command with its step directory as the working directory. Each host CLI runs with an environment built from an allow-list (`PATH`, `SYSTEMROOT`, `WINDIR`, `COMSPEC`, `PATHEXT`, `TEMP`, `TMP`, `LOCALAPPDATA`, `APPDATA`, `PROGRAMDATA`) plus the step's own variables, `HOME` and `USERPROFILE` set to `<step>/home`, `GIT_CONFIG_GLOBAL` set to an empty file there, `GIT_TERMINAL_PROMPT=0` and `DISABLE_AUTOUPDATER=1`; no other inherited variable reaches it. The receipt names the host state outside the step directory that a step may still write: the pip cache, `%TEMP%` staging, and the Codex update check.
   - Each step writes one JSON line to `<run-root>/report.jsonl` with `step`, `host`, `verdict` (`PASS`, `FAIL` or `NOT_SUPPORTED`), the commands run, their exit codes, and the evidence. It holds no credential and no e-mail address.
   - The script exits 0 only when every requested step is `PASS`. `NOT_SUPPORTED` means a host CLI lacks a command or refuses the `file://` URL form of `codex-ref`; it is never a `PASS`.
2. **The steps.**
   - **build:**
     - clone the repository with `--no-hardlinks` into `<run-root>/build/repo`, check out `--candidate` detached, and run there `python -m library.local_orchestration.plugin_publication --repo . --manifest .claude-plugin/plugin.json --marketplace .claude-plugin/marketplace.json --ref refs/heads/publication-0.5.0`;
     - require the printed commit to equal `--expected-publication`;
     - extract it and build the local marketplace in `<run-root>/build/marketplace/` with the layout of ticket 71 item 8;
     - no other step runs without `build` in the same run.
   - **fresh:**
     - add the local marketplace, then install `software-factory@software-factory`;
     - read the host's plugin list back. It shows `0.5.0`, installed and enabled. The read-back commands are `claude plugin list --json` and `codex plugin list --marketplace software-factory --json`; a pinned CLI without the first is `NOT_SUPPORTED` and a `CHANGE_DETECTED` return;
     - then run the README's `claude plugin update software-factory@software-factory --scope user`, which must exit 0 and leave the list at `0.5.0`, installed and enabled.
   - **upgrade:**
     - install `johnny-ai-skill@johnny-ai-skill` 0.4.14 from the public marketplace. For Claude Code, the URL is `https://raw.githubusercontent.com/johnnyliu365-sys/Software-Factory/01b810f096b1201005d26922e2c8a474bdd5a0a0/.claude-plugin/marketplace.json`, the last change to the 0.4.14 `main`'s marketplace. For Codex, it is a local marketplace in `<step>/marketplace-0414/` whose only file is `.claude-plugin/marketplace.json`, written byte for byte from `01b810f096b1201005d26922e2c8a474bdd5a0a0:.claude-plugin/marketplace.json` (source `url` the public publication repository, `sha` `0b3afd3645946f97662c336f0e6ac0dcae502e69`). The step records the commit Codex installed. `PASS` needs `0.4.14` installed from `0b3afd3645946f97662c336f0e6ac0dcae502e69`; a refusal is `FAIL` and a `CHANGE_DETECTED` return;
     - remove `johnny-ai-skill@johnny-ai-skill` and the marketplace `johnny-ai-skill` with the host's commands of README section (5), then install from the local marketplace as in `fresh`;
     - the plugin list then shows `software-factory` `0.5.0` and no `johnny-ai-skill` plugin, and the marketplace list shows no `johnny-ai-skill`.
   - **uninstall:**
     - starting from the state of `fresh`, uninstall the plugin and remove the marketplace, with the README's commands;
     - afterwards no path segment and no line of a `.json` or `.toml` file under the step's directory names `software-factory` as a whole name, except the entries of a fixed allow-list in `ci/acceptance/README.md`, each with its reason; that list is reviewed under condition (4), and anything else is `FAIL`;
     - the allow-list admits one host record by key, not by line: the value of the top-level key `declinedPlugins` in `.claude.json` under the step's `CLAUDE_CONFIG_DIR`, with the reason "the host's own decline record (owner decision 2026-11-26, 放寬)"; any other key or line of that file that names `software-factory` is `FAIL`;
     - then, with the record still present, add the good marketplace and install again; it must exit 0, and the list must show `software-factory@software-factory` `0.5.0`, installed and enabled.
   - **recover:**
     - add a local marketplace named `software-factory` whose plugin source names a missing directory, then install; the first of the two that exits non-zero is the expected failure, and if both exit 0 the step is `FAIL`;
     - then run the README's uninstall and marketplace-remove commands, recording their exits without judging them;
     - then add the good marketplace and install, which must exit 0, and the list must show exactly one entry outside the host's `@builtin` plugins, `software-factory@software-factory` `0.5.0`, installed and enabled.
   - **level2:**
     - download `https://github.com/johnnyliu365-sys/Software-Factory/releases/download/v0.4.9/johnny-ai-skill-0.4.9.zip` and `…/v0.4.9/johnny-install.cmd` into `<step>/download` with `urllib`, without a token, and require sha256 `2365b6f70a06f00ae0aed008371f7cc0b5afd0cb148a77e7476416bf25854aef` and `906b067238f05841ba87b5c59d88d0a8a5499821d8ebc660df9cee17296f532b`; a mismatch is `FAIL`;
     - run its documented install (`johnny-install.cmd`, its `INSTALL` prompt answered on standard input under the owner decision of 2026-11-26 on S77R-01) with `JOHNNY_ROOT` set to `<step>/root`, a new directory checked empty before the install, then its own `uninstall`. The installer's environment is the allow-list of item 1, `HOME=<step>/home`, no `USERPROFILE` (the `py` launcher exits 109 under a foreign one), and `JOHNNY_ROOT`. The install runs with the step directory as its working directory, and the wrapper is passed by absolute path;
     - after `uninstall`, `JOHNNY_ROOT` holds no file except those on a list in `ci/acceptance/README.md` that quotes README section (6) for each entry; any other file is `FAIL`.
   - **codex-ref:** emulate a `marketplace` branch with a plugin source of `url` + `sha` pointing into the same repository, using a local bare repository and a `file://` URL. Run `codex plugin marketplace add <that URL> --ref marketplace`, then `plugin add`. The bare repository's default branch tip differs from the pinned commit, and the `marketplace` branch holds only `.claude-plugin/marketplace.json`, as release step 4 pushes it. `PASS` needs the installed tree to equal the pinned commit's tree. `marketplace add` exiting non-zero on the `file://` URL is `NOT_SUPPORTED`, with its output recorded, and the check moves to release step 8; any later failure, or another tree, is `FAIL`.
   - **codex-files:** three local marketplaces: both files with different plugin versions; only `.claude-plugin/marketplace.json` (source `./plugins/software-factory`); only `.agents/plugins/marketplace.json` (source `{"source": "local", "path": …}`). It records, for each, whether `plugin add` exits 0 and which version is listed. `PASS` when every command completes and each outcome is recorded; a crash or a timeout is `FAIL`.
3. **`.github/workflows/acceptance.yml`.**
   - Its only trigger is `workflow_dispatch`, with inputs `candidate` and `expected_publication`.
   - It runs on `windows-latest`, `timeout-minutes: 60`, and has `permissions: contents: read`.
   - Its checkout is the action and SHA of `ci.yml` with `fetch-depth: 0` and `persist-credentials: false`; every action is pinned to a full SHA with its version in a comment.
   - It installs the two host CLIs at the exact versions written in `ci/acceptance/README.md`. Those versions are the ones on this host at the local run: the run of item 5 uses the host's own CLIs, with no copied binary, and the README pins what `--version` printed there.
   - It runs `lifecycle.py` with `--host both` and the steps `build,fresh,upgrade,uninstall,recover,level2`. It runs with `--run-root "$RUNNER_TEMP/acceptance"`. It uploads `report.jsonl` as an artifact.
   - It uses no secret and does not log in to either host.
4. **`ci/acceptance/README.md`.** It holds the host CLI versions, the commands for the local run, and the four conditions with where each one's evidence lives.
5. **The local run (condition 3).**
   - Before returning, the seat runs `--host both --steps build,fresh,upgrade,uninstall,recover,level2`, which must exit 0 (condition 3), then `--host codex --steps build,codex-ref,codex-files` in a second run root, whose report is recorded; a `NOT_SUPPORTED` there does not block `COMPLETED`. Each run root is a new directory under `C:/Temp/claude/`, named with the seat's run id, outside every Git work tree. The seat runs only `claude --version`, `codex --version` and the `plugin` and `plugin marketplace` subcommands; never a prompt, `-p`, `exec` or a session, and never a login.
   - `report.jsonl` goes into the receipt as a cell.
   - A test that does not replace them asserts that each fixed value in `lifecycle.py` equals the ticket's literal: `0b3afd3645946f97662c336f0e6ac0dcae502e69`, `01b810f096b1201005d26922e2c8a474bdd5a0a0`, the Claude Code URL of the `upgrade` step, and the two `v0.4.9` sha256 values.
   - Host CLI versions are read with `claude --version` and `codex --version`, and named in the STATEMENT, and, when they differ from `ci/acceptance/README.md`, the STATEMENT says so and the record carries both.
6. **The acceptance record.** `doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md` starts with the local run. The control plane later adds the cloud run and the owner-assisted Codex session.

**After review approval and integration, control-plane and owner work, not this seat's:**

1. With conditions (1), (2) and (4) checked and (3) in the receipt, the control plane asks the owner to confirm two things: the fast-forward push of the development `main` to `cp/wave3`, and then the one cloud run. It triggers that run with `gh workflow run acceptance.yml --ref main -f candidate=<the main commit after the fast-forward> -f expected_publication=<ticket 71's publication commit>`, and records the run id and the artifact. A failed run is recorded and reported to the owner; it is not re-run without a new owner decision.
2. **The owner-assisted session on this host:**
   - The control plane tells the owner first.
   - The owner starts Codex with `CODEX_HOME` and `JOHNNY_ROOT` set to new empty directories, logs in anew, and installs 0.5.0 from the local marketplace.
   - One test ticket goes through the new flow on a fixture project.
   - The session is ended mid-ticket, and a new session resumes it from the ticket, receipt and queue files alone.
   - With `johnny-ai-skill` 0.4.14 and `software-factory` 0.5.0 both installed, a session stops at the first start step of ticket 81 and gives the removal commands.
   - The control plane records each step.
3. Installation by someone other than the owner stays with the owner.

## 實作範圍、依賴與 ticket elements

### 角色指派（必填）

- 流程／Grill／ticket owner：control plane.
- implementation owner：`implementation-standard` seat in `.worktrees/77-acceptance`.
- reviewer：`ticket-review` seat in `.worktrees/77-acceptance-review`.
- **Owner override record**：the cloud run and the Codex session wait for the owner in chat.
- `ImplementationHandoff`：this ticket; ticket 71 and its local marketplace; `library/local_orchestration/plugin_publication.py`.
- `ImplementationReturn`：`COMPLETED → ACTION_COMPLETED`／`BLOCKED → HALT`／`CHANGE_DETECTED → REQUIREMENT_CHANGED → Grill`。A host command that behaves other than the README says is a `CHANGE_DETECTED` return naming the step, the command and its output.

### 前端組合與依賴注入

**N/A reason**：a test harness and a workflow; no UI boundary.

- element 路徑：不適用
- 實際原始碼路徑：the paths in the boundary block
- 公開契約／資料模型：the arguments and the `report.jsonl` line above.

## TDD 設計

1. 正常行為：with a fake host CLI on `PATH` that records its arguments, every step issues the README's exact commands with the step's own directory set in the environment.
2. 規則違反／輸入錯誤：
   - a run root that is not empty is refused;
   - an unknown step or host is refused;
   - a regenerated commit other than `--expected-publication` fails `build`.
3. 外部失敗／fail-closed：
   - a fake CLI that exits non-zero fails the step;
   - a missing subcommand gives `NOT_SUPPORTED`, and the script exits non-zero;
   - the `recover` step fails when the broken install exits 0.
4. 回歸保護：the workflow file is parsed. Its only trigger is `workflow_dispatch`; it holds none of `secrets.`, `GITHUB_TOKEN`, `github.token`, `id-token`; every `uses:` is a full SHA; its permissions are `contents: read`. The test passes on both runners of `ci.yml` without a new row in `ci/registered-failures.json`; fake CLIs are Python files started through `sys.executable`; a case that needs Windows is skipped elsewhere, with its reason.

### 適用的缺陷類別

| # | 類別 | 是否適用 | 本工單的必要案例 |
| --- | --- | --- | --- |
| 1 | 路徑前綴誤匹配 | 是 | the residue scan matches `software-factory` as a whole path segment or file name, not as a prefix of another name |
| 2 | null／空字串／陣列 | 是 | empty `--steps`, an empty run root path |
| 3 | 權限繞過 | 是 | no step touches the user's own configuration; the workflow has no secret and no write permission |
| 4 | Token 格式與比較 | 是 | commit ids compared as 40 lower-case hex, exactly |
| 5 | 錯誤碼是否一致 | 是 | `PASS`, `FAIL` and `NOT_SUPPORTED` stay distinct |
| 6 | 例外是否會拋出 | 是 | a CLI that cannot be started is a `FAIL` with the reason, not a traceback |

## 完成定義與證據

- `python -m pytest tests/test_acceptance_lifecycle.py -q` exits 0; `mypy --strict --python-version 3.11` on the script and the test exits 0.
- **L1**: the local run of every step, with `report.jsonl` as the raw block.
- **反向突變證據**：
  - drop the empty-run-root check;
  - let `NOT_SUPPORTED` count as a pass;
  - add a `push` trigger to the workflow;
  - drop the expected-publication comparison.
- **CI evidence**: one run of `ci.yml` on a commit of this branch, with both jobs `success`. The acceptance workflow is not run by the seat.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The one cloud run, the owner-assisted session and the release follow ticket 71's release order, each push with the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
