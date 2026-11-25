# 77｜Acceptance of 0.5.0: the install lifecycle in isolated directories, locally and once on a GitHub-hosted Windows runner

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043, owner decisions 2026-11-19 "A" with conditions "1.2.3.4", 2026-11-19 on Level 2 and the Codex install path, 2026-11-20 on the release order and the rename, 2026-11-26 "B" on the cloud trigger） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision01 / receipt under `.worktrees/77-acceptance-out/` / owner implementation seat / worktree `.worktrees/77-acceptance` / branch `cp/wave3-77-acceptance` / baseline the wave-3 branch after ticket 71 is integrated |
| 實作語言 | Python 3.11 for the lifecycle script and its test; YAML for the workflow（CONTEXT.md Implementation language） |
| 狀態 | `PLANNED`（revision01; strict tier; rule-only review before dispatch; after ticket 71） |
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
- **2026-11-26 "B":** a `workflow_dispatch` workflow runs only from the default branch, so the development `main` is fast-forwarded to `cp/wave3` before the cloud run. From then on, `main`'s marketplace is 0.5.0's, so the upgrade step reads 0.4.14 at a fixed commit.

Ticket 71's rule-only review handed this ticket three checks that only running the CLIs can settle (`doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md`, S71R-19, S71R-20, S71R-21).

After this ticket:

1. **`ci/acceptance/lifecycle.py`.**
   - It uses only the standard library and passes `mypy --strict`.
   - It takes `--candidate <commit>`, `--expected-publication <commit>`, `--host claude|codex|both`, `--steps <comma list>` and `--run-root <empty directory>`.
   - Every step gets its own new directory under the run root. For Claude Code that directory is `CLAUDE_CONFIG_DIR`; for Codex it is `CODEX_HOME`; for Level 2 it is `JOHNNY_ROOT`. The script refuses a run root that is not empty, and it never reads or writes the user's own configuration directories.
   - Each step writes one JSON line to `<run-root>/report.jsonl` with `step`, `host`, `verdict` (`PASS`, `FAIL` or `NOT_SUPPORTED`), the commands run, their exit codes, and the evidence. It holds no credential and no e-mail address.
   - The script exits 0 only when every requested step is `PASS`. `NOT_SUPPORTED` means a host CLI lacks a command; it is never a `PASS`.
2. **The steps.**
   - **build:**
     - regenerate the publication commit from `--candidate` with the committed generator;
     - require its id to equal `--expected-publication`;
     - extract it, and build the local marketplace the way ticket 71 item 8 does.
   - **fresh:**
     - add the local marketplace, then install `software-factory@software-factory`;
     - read the host's plugin list back. It shows `0.5.0`, installed and enabled.
   - **upgrade:**
     - install `johnny-ai-skill@johnny-ai-skill` 0.4.14 from the public marketplace. For Claude Code, the URL is `https://raw.githubusercontent.com/johnnyliu365-sys/Software-Factory/01b810f096b1201005d26922e2c8a474bdd5a0a0/.claude-plugin/marketplace.json`, the last change to the 0.4.14 `main`'s marketplace. For Codex, it is `johnnyliu365-sys/Johnny_AI_Skill_publication`;
     - follow README section (5) to move to `software-factory`;
     - the list then shows `software-factory` 0.5.0 and no `johnny-ai-skill`.
   - **uninstall:**
     - starting from the state of `fresh`, uninstall the plugin and remove the marketplace, with the README's commands;
     - afterwards no file under the step's directory names `software-factory`, apart from a residue list the script prints with a reason for each entry, which the reviewer judges.
   - **recover:**
     - install from a local marketplace whose plugin source names a missing directory, which must fail with a non-zero exit;
     - then follow the README's removal commands and install from the good marketplace, which must succeed with no half-installed entry left.
   - **level2:**
     - download the `v0.4.9` release assets into the step's directory (`gh release download v0.4.9`);
     - run its documented install with `JOHNNY_ROOT` set to the step's directory, then its own `uninstall`;
     - compare what remains with README section (6).
   - **codex-ref:** emulate a `marketplace` branch with a plugin source of `url` + `sha` pointing into the same repository, using a local bare repository and a `file://` URL. Run `codex plugin marketplace add <that URL> --ref marketplace`, then `plugin add`. If Codex does not take a `file://` URL, the verdict is `NOT_SUPPORTED`, and the check moves to release step 8.
   - **codex-files:** in a local marketplace that holds both `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`, with different plugin versions, record which one Codex reads.
3. **`.github/workflows/acceptance.yml`.**
   - Its only trigger is `workflow_dispatch`, with inputs `candidate` and `expected_publication`.
   - It runs on `windows-latest`, `timeout-minutes: 60`, and has `permissions: contents: read`.
   - It installs the two host CLIs at the exact versions written in `ci/acceptance/README.md`.
   - It runs `lifecycle.py` with `--host both` and the steps `build,fresh,upgrade,uninstall,recover,level2`. It uploads `report.jsonl` as an artifact.
   - It uses no secret and does not log in to either host.
4. **`ci/acceptance/README.md`.** It holds the host CLI versions, the commands for the local run, and the four conditions with where each one's evidence lives.
5. **The local run (condition 3).**
   - Before returning, the seat runs every step on this host with `--host both`, in a run root under its scratch directory.
   - `report.jsonl` goes into the receipt as a cell.
   - Host CLI versions are read with `claude --version` and `codex --version`, and named in the STATEMENT.
6. **The acceptance record.** `doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md` starts with the local run. The control plane later adds the cloud run and the owner-assisted Codex session.

**After review approval and integration, control-plane and owner work, not this seat's:**

1. With conditions (1), (2) and (4) checked and (3) in the receipt, the control plane asks the owner to confirm two things: the fast-forward push of the development `main` to `cp/wave3`, and then the one cloud run. It triggers that run with `gh workflow run acceptance.yml --ref main`, and records the run id and the artifact.
2. **The owner-assisted session on this host:**
   - The control plane tells the owner first.
   - The owner starts Codex with `CODEX_HOME` and `JOHNNY_ROOT` set to new empty directories, logs in anew, and installs 0.5.0 from the local marketplace.
   - One test ticket goes through the new flow on a fixture project.
   - The session is ended mid-ticket, and a new session resumes it from the ticket, receipt and queue files alone.
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
4. 回歸保護：the workflow file is parsed. Its only trigger is `workflow_dispatch`; it has no `secrets.` reference; its permissions are `contents: read`.

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
