# 77｜Acceptance of 0.5.0: the install lifecycle in isolated directories, locally and once on a GitHub-hosted Windows runner

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner decisions 2026-11-19 "A" with conditions "1.2.3.4", 2026-11-19 on Level 2 and the Codex install path, 2026-11-20 on the release order and the rename, 2026-11-26 "B" on the cloud trigger, 2026-11-27 "A" on the failed cloud run） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision06 / receipt under `.worktrees/77-acceptance-out/` / owner implementation seat / worktree `.worktrees/77-acceptance` / branch `cp/wave3-77-acceptance` / baseline the wave-3 branch after ticket 71 is integrated |
| 實作語言 | Python 3.11 for the lifecycle script and its test; YAML for the workflow（CONTEXT.md Implementation language） |
| Closure revision | 不適用 |
| Strict checker | `mypy --strict --python-version 3.11` (mypy 2.3.0) |
| Profile / resource | the dispatch's `profile:` line (`doc/runbooks/dispatch-model-profile.md`) |
| XSS classification | 不適用：no browser, WebView or DOM input |
| 狀態 | `INTEGRATED`; dispatch=sha256:859c470c259754ad8f5c97e53a94021f192c460652e8800973a71a6e72a4d2ec (`doc/handoffs/2026/workflow-governance/dispatch/JAS-77-4.yaml`)（candidate `c983c6ef`; correction review `APPROVED`） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/77-acceptance` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/77-acceptance-review` |
| 責任邊界 | one lifecycle script, its test, one `workflow_dispatch` workflow, and the acceptance record |
| 禁止修改 | the shipped manifests, `README.md`, `library/`, the gate scripts, the governance documents, `.github/workflows/ci.yml`; in revision05 also `ci/acceptance/lifecycle.py`, `requirements-dev.txt` and the acceptance record |
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

- **2026-11-27 "A" on the failed cloud run:** the one cloud run (45920193720, `main` `f1d04039`) failed at `build` with `ModuleNotFoundError: No module named 'pydantic'`, because the workflow installs no Python package. The owner chose "A（建議）：重開票 77，出一個新修訂": the workflow gains the install step, the README sentence is corrected and a test pins the order.

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

**Revision05.** Revision04 was approved at `8cf1e387` and integrated at `e87bc5cb`. The owner fast-forwarded the development `main` to `f1d04039` and confirmed the cloud run. Run 45920193720 ended `failure` in 40 seconds: `build` cloned and checked out the candidate, then the publication generator exited 1 with `ModuleNotFoundError: No module named 'pydantic'` (`library/local_orchestration/contracts.py` line 8), and the other nine steps did not run. `.github/workflows/acceptance.yml` installs the two host CLIs and no Python package; `ci.yml` installs `requirements-dev.txt`, which holds `pydantic`. `ci/acceptance/README.md` says "or any Python 3.11", which is wrong for `build`. Every local run had used an interpreter that already held `pydantic`, and the host's own `claude.exe` and `codex.exe`, not the `.cmd` shims that `npm install --global` makes on the runner. On 2026-11-27 the control plane installed the Python packages and the host CLI versions that the workflow installs (a new venv with `requirements-dev.txt`; `npm install --prefix` of the two pinned packages, first on `PATH`) and ran the six steps at `f1d04039`: all ten verdicts `PASS`, with every host command started through `claude.CMD` or `codex.CMD` (record, section "The cloud run", entry "Parity run"). The one defect found is the missing install step, and revision05 is item 7. The parity run (7c, 7e) is the control plane's evidence that the fix works with only what the workflow installs. It is not part of the owner's option text, and it sets no rule on how many cloud runs there are (decision 2 of 2026-11-27 is not answered). **Revision06** applies the exact fixes of the rule-only delta review of revision05 (S77R-24 to S77R-34, `doc/reviews/workflow-governance/77-acceptance-0-5-0-ticket-review.md`) and changes nothing else. `ci/acceptance/lifecycle.py`, `requirements-dev.txt` and the acceptance record do not change in revision05; items 1, 2, 5 and 6 stay as revision04 left them. The record of the run is `doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md`, section "The cloud run", on `cp/wave3`.

7. **Revision05: the workflow installs the Python packages, and the parity run is written down.**
   - **7a, the workflow.** `.github/workflows/acceptance.yml` gains one step, placed after the `actions/setup-python` step and before the step `Install the host CLIs at the versions of ci/acceptance/README.md`. Its `name` and its `run` lines are those of the step `Install development requirements` of `.github/workflows/ci.yml`:

     ```
           - name: Install development requirements
             run: |
               python -m pip install --upgrade pip
               python -m pip install -r requirements-dev.txt
     ```

     Nothing else in the workflow changes.
   - **7b, the README sentence.** In `ci/acceptance/README.md`, section "The local run (condition 3)", the sentence "Use the interpreter that has `mypy` and `pytest` (`requirements-dev.txt`) or any Python 3.11." is replaced by: "Use an interpreter that holds the packages of `requirements-dev.txt`: the `build` step runs the publication generator, which imports `pydantic`, and a Python 3.11 without it fails `build`." The new sentence stays on the line that begins `one). `, unwrapped, and the 7d test checks it with `assertIn` on the README text as read.
   - **7c, the parity run.** `ci/acceptance/README.md` gains this section, directly before `## Isolation`:

     ````
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
     ````

     Each line of the 7a and 7c blocks loses the five leading spaces of this list when it is written: the step's `- name:` line has six leading spaces, like the `- uses:` lines of `acceptance.yml`, and `## The parity run` starts at column 1.

   - **7d, the tests**, in `tests/test_acceptance_lifecycle.py`, each a new method:
     - the workflow holds a step named `Install development requirements`; its `run` lines equal the `run` lines of the step of that name in `ci.yml`, read from `ci.yml` and not written a second time in the test; that step's line number is greater than the `actions/setup-python` line's and less than the line `- name: Install the host CLIs at the versions of ci/acceptance/README.md`;
     - the step's lines and the heading are matched as whole lines with `re.MULTILINE`: `^      - name: Install development requirements$` and `^## The parity run$`;
     - the README holds the 7b sentence and does not hold "or any Python 3.11";
     - the README holds the heading `## The parity run` before `## Isolation`, the line `<A>/Scripts/python.exe -m pip install -r requirements-dev.txt`, and an `npm install --prefix <B>` line whose two `package@version` items equal the two in the workflow's `npm install --global` line, read from the workflow.
   - **7e, the parity run by the seat (cell L3).** The seat follows 7c as written, with `<A>`, `<B>` and the run root new directories under `C:/Temp/claude/` named with its run id, at `--candidate` its last commit and `--expected-publication d355b4a26336cebbe4e8e28650ce0120d4c39a13` (the publication commit of this branch's payload, as in revision04). It must exit 0 with all ten verdicts `PASS`, the generator's command naming the interpreter under `<A>`, and every host command naming a `.CMD` under `<B>`. Besides `lifecycle.py`, the seat runs only the three install lines of 7c. `lifecycle.py`'s host commands are those item 5 allows, and the seat runs no `claude` or `codex` command of its own. An install line that exits non-zero is a `BLOCKED` return naming the line and its output. A parity-run step that is not `PASS` is a `CHANGE_DETECTED` return naming the step, the command and its output (the revision04 L1 passed every step); the seat does not edit `lifecycle.py`. The STATEMENT names the versions that the `--version` records of `report.jsonl` show for the CLIs under `<B>`. After `report.jsonl` is copied into cell L3, the seat removes `<A>`, `<B>` and the run root, which carry its run id. The npm cache (`%LOCALAPPDATA%\npm-cache`) and the pip cache, which the install lines write, are not removed, and the STATEMENT names them.

**After review approval and integration, control-plane and owner work, not this seat's:**

1. With conditions (1), (2) and (4) checked and (3) in the receipt, the control plane asks the owner to confirm two things: the fast-forward push of the development `main` to `cp/wave3`, and then the one cloud run. It triggers that run with `gh workflow run acceptance.yml --ref main -f candidate=<the main commit after the fast-forward> -f expected_publication=<ticket 71's publication commit>`, and records the run id and the artifact. A failed run is recorded and reported to the owner; it is not re-run without a new owner decision. Run 1 (45920193720) failed at `build`. After revision05 is integrated, the control plane does the parity run of item 7c at the new candidate and records it, then asks the owner to confirm the fast-forward of `main` and the second run, each in words.
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
- **Owner override record**：the cloud run and the Codex session wait for the owner in chat. Revision05 reopens this ticket after `INTEGRATED` (`8cf1e387` at `e87bc5cb`). `specification-ticketing.md` "Records" lists no transition out of `INTEGRATED`, and `CodeReview.md` §4 would send a change after closure to a new `PLANNED` ticket; the owner chose "A（建議）：重開票 77，出一個新修訂" (REQ-043 row "Owner decision 2026-11-27 (the cloud run failed at `build`; ticket 77 is reopened, "A")"). Revision05 is a new closure revision: its first code review is an initial review (`CodeReview.md` rule-review-label), and the revision04 review and integration records stay as written. The seat continues the branch `cp/wave3-77-acceptance` at `8cf1e387` on its base `f53ecc6a`, so the `create =` lines of the boundary block still describe the diff from that base.
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
4. Revision05, each a named test that goes red: the step `Install development requirements` removed from the workflow; that step moved after the step that runs `lifecycle.py`; that step moved between the host-CLI step and the step that runs `lifecycle.py`; its `run` lines made to differ from `ci.yml`'s; the 7b sentence removed from the README or "or any Python 3.11" put back; the parity-run section removed; a package version in the README's `npm install --prefix` line made to differ from the workflow's.
5. 回歸保護：the workflow file is parsed. Its only trigger is `workflow_dispatch`; it holds none of `secrets.`, `GITHUB_TOKEN`, `github.token`, `id-token`; every `uses:` is a full SHA; its permissions are `contents: read`. The test passes on both runners of `ci.yml` without a new row in `ci/registered-failures.json`; fake CLIs are Python files started through `sys.executable`; a case that needs Windows is skipped elsewhere, with its reason.

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
- **Revision05 mutations (cell M1; the four above are not rerun: three target `lifecycle.py`, which does not change; the push-trigger test is unchanged, and the new step lies outside `on:`)**：
  - the step `Install development requirements` removed from `acceptance.yml`;
  - that step moved after the step that runs `lifecycle.py`;
  - that step moved between the host-CLI step and the step that runs `lifecycle.py`;
  - `requirements-dev.txt` in that step replaced by another file name;
  - "or any Python 3.11" put back into the README sentence;
  - the section `## The parity run` removed from the README;
  - one package version in the README's `npm install --prefix` line changed.
- **L3 (revision05)**: the parity run of item 7e, with `report.jsonl` as the raw block. L1 and L2 are not rerun in revision05.
- **Revision05 file limit (cell D1)**: `git diff --name-only 8cf1e387 <candidate>` lists only `.github/workflows/acceptance.yml`, `ci/acceptance/README.md` and `tests/test_acceptance_lifecycle.py`.
- **CI evidence**: one run of `ci.yml` on a commit of this branch, with both jobs `success`. The acceptance workflow is not run by the seat.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The one cloud run, the owner-assisted session and the release follow ticket 71's release order, each push with the owner's confirmation.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
