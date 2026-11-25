# 71｜Publication 0.5.0 as Software Factory: plugin id `software-factory`, Apache-2.0 and author in the manifests, the README rewritten, Level 1 for Claude Code and Codex, the marketplace in the public publication repository

| 欄位 | 內容 |
| --- | --- |
| 對應規格 ID | `SPEC-AI-WORKFLOW-WORKFLOW-GOVERNANCE-20260805-01KZ6T8V2R4Y6B8D0F2H4J6M8P`（REQ-20261103-043 wave 3 "publication 0.5"; owner decisions 2026-11-07 "2.B", 2026-11-18 "2A", and 2026-11-19 on Level 2, the Codex install path and the Codex manifest） |
| 規格撰寫 AI | control plane |
| 第一步排查起點 | `doc/context/workflow-governance/main.md` |
| PRD 索引 | `PRD-20261103-043` |
| 需求變更 | `CHG-20261103-043` |
| Sealed Context binding | 不適用 |
| Agent Context binding | ticket revision03 / receipt under `.worktrees/71-publication-out/` / owner implementation seat / worktree `.worktrees/71-publication` / branch `cp/wave3-71-publication` / baseline the wave-3 branch after ticket 79 is integrated |
| 實作語言 | JSON manifests; Python 3.11 for the tests（CONTEXT.md Implementation language） |
| 狀態 | `PLANNED`（revision03; strict tier; rule-only review of revision02 CHANGES_REQUESTED, revision03 under rule-only review; the last wave-3 code ticket, after ticket 79） |
| 共同基準 | the `cp/wave3` commit named in the dispatch |
| 實作者 | `implementation-standard` seat, worktree `.worktrees/71-publication` |
| 審閱者 | `ticket-review` seat, worktree `.worktrees/71-publication-review` |
| 責任邊界 | the two shipped manifests, the README's install sections, one SKILL.md sentence, the publication test constants, the changelog entry, and the publication commit built locally with the committed generator |
| 禁止修改 | `library/` code, the gate scripts, the governance documents; any push to the publication repository (the control plane pushes after the owner confirms) |
| 環境 | `LOCAL` and GitHub Actions on the development repository; the publication repository, the anchor ref and the tags only after the owner confirms |

## 邊界宣告（機器可讀，整合前由閘門讀取）

```johnny-boundary
modify = .claude-plugin/plugin.json
modify = .claude-plugin/marketplace.json
modify = README.md
modify = NOTICE
modify = skills/johnny-project-takeover/SKILL.md
modify = tests/test_plugin_publication.py
modify = tests/test_plugin_payload_boundary.py
modify = ci/registered-failures.json
modify = doc/HARNESS-CHANGELOG.md
forbid = library/
forbid = skills/johnny-project-takeover/scripts/
forbid = Workflow.md
forbid = AGENTS.md
forbid = CodeReview.md
```

## 使用者拍板與可觀察結果

Process tier: strict.

Owner decisions this ticket carries out. Each is quoted in `REQ-20261103-043`, which is authoritative:

- **2026-11-07 "2.B":** the marketplace re-pin waits for the wave-3 publication.
- **2026-11-18 "2A":** the licence is Apache License 2.0, as `LICENSE` states; the author is Johnny Liu.
- **2026-11-19:** the Level 2 runtime does not ship; Codex installs through `codex plugin marketplace add` and `codex plugin add`; `.codex-plugin/plugin.json` is retired, which ticket 78 does.
- **2026-11-20, release order:** the candidate is tested from a local marketplace; nothing is pushed for testing; no release-candidate tag is made.
- **2026-11-20, rename ("1A 2.A 3A 4可以", "發布前我來改就好", publication name "A"):**
  - the plugin id becomes `software-factory`;
  - `marketplace.json` moves into the public publication repository;
  - the owner renames that repository to `software-factory-plugin` before the release;
  - the README is rewritten in full.

**Revision03** also answers the rule-only review of revision02 (`doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md`).

After this ticket:

1. **The shipped manifests.**
   - `.claude-plugin/plugin.json` gets:
     - `name` is `software-factory`;
     - `version` is `0.5.0`;
     - `license` is `Apache-2.0`;
     - `author.name` is `Johnny Liu`, with URL `https://github.com/johnnyliu365-sys`;
     - `homepage` and `repository` are `https://github.com/johnnyliu365-sys/software-factory-plugin`;
     - a description of the governed project workflow with its gate scripts and of reusable-module selection, naming neither router nor telemetry.
   - `.claude-plugin/marketplace.json` gets:
     - the marketplace `name` and the plugin entry `name` are both `software-factory`;
     - `owner.name` is `Johnny Liu`;
     - the plugin entry has `version` `0.5.0`, `license` `Apache-2.0` and the same author, homepage and repository;
     - its `source` is `{"source": "url", "url": "https://github.com/johnnyliu365-sys/software-factory-plugin.git", "sha": <the publication commit>}`.
   - No manifest holds an e-mail address.
   - The `payload` declaration of `plugin.json` is unchanged.
2. **`NOTICE`** names the product "Software Factory". Its repository line is the publication repository URL. Its other lines stay.
3. **The README is rewritten in full.** The section headings, in this order, are listed below.

   (1) **Software Factory 是什麼、給誰用.** A governed control plane for building software with AI agents. Its target is teams and, from 1.0, enterprises.

   (2) **它會做什麼、不會做什麼.** It carries the content of today's section "它會對你的 repository 做什麼、不做什麼", brought up to date.

   (3) **安裝：Claude Code.** Exactly these three commands:

   ```bash
   claude plugin marketplace add https://raw.githubusercontent.com/johnnyliu365-sys/software-factory-plugin/marketplace/.claude-plugin/marketplace.json
   claude plugin install software-factory@software-factory --scope user
   claude plugin marketplace remove software-factory
   ```

   The third command removes the marketplace. The README also keeps the `update` and `uninstall` commands with the new id.

   (4) **安裝：Codex.** The steps, in order:
   1. Run `codex --version`. The `plugin add` command is needed: `0.167.0-alpha.3.2` has it, and `0.130.0-alpha.5` lists only `plugin marketplace`.
   2. Run `codex plugin marketplace add johnnyliu365-sys/software-factory-plugin --ref marketplace`.
   3. Run `codex plugin add software-factory@software-factory --json`.
   4. Check the version with `codex plugin list --marketplace software-factory --json`: the entry `software-factory@software-factory` shows `version` `0.5.0`, `installed` true and `enabled` true.
   5. To remove it, run `codex plugin remove software-factory@software-factory --json`, then `codex plugin marketplace remove software-factory --json`.

   (5) **從舊版 `johnny-ai-skill` 換過來.** Remove the old plugin with each host's remove command for `johnny-ai-skill@johnny-ai-skill`, then install as above. A project's own copies of `AGENTS.md` and `Workflow.md`, copied from an earlier version, are replaced with the 0.5.0 copies.

   (6) **舊版 Level 2 runtime 的移除.**
   - The old runtime removes itself with its own `uninstall`. The command sits in a fenced block, as today.
   - What `uninstall` removes and what it leaves (`johnny-router.ps1`, `live_uninstall_composition.py`).
   - When the folder `%LOCALAPPDATA%\JohnnyRouter` may be deleted by hand: when `uninstall` cannot run, for example after a failed install whose `install-journal.jsonl` blocks a reinstall.

   Paths appear in fenced blocks or as plain text, never as inline code.

   (7) **第一次使用.** One project from requirement to acceptance, in plain steps.

   (8) **它怎麼運作.** State lives in files: tickets, receipts, the integration queue. Gate scripts decide each step. Reviews are independent.

   (9) **路線.** 0.5.0, then wave 4, then the beta (every 1.0 capability except deployment, run on the tester's own computer), then 1.0 for enterprises (self-hosted, Docker Compose), then a SaaS later.

   (10) **作者與授權.**

   The README names no Level 2 install step and no `johnny-install.cmd`.
4. **`SKILL.md`.** The sentence that ticket 67 restored after "The honest statement is: …" begins "The kept launcher commands". It becomes one sentence: a 0.4.x Level 2 runtime is removed by its own `uninstall`, as the README describes. It holds no path token in backticks. The no-runner statement before it stays.
5. **Tests.** Each change is named in the STATEMENT:
   - `tests/test_plugin_publication.py`:
     - `_RELEASE_VERSION` and the hard-coded `"0.4.14"` in `test_t6` become `0.5.0`;
     - the exact route tuple of `_assert_exact_l3_marketplace_routes` becomes the one `claude plugin marketplace add` line above;
     - the injection anchor of `test_l3_rejects…` becomes that line;
     - the install, update, uninstall and remove assertions use `software-factory`.
   - `tests/test_plugin_payload_boundary.py`:
     - the closure dictionaries lose the `johnny-install.cmd` entry, whose only payload reference leaves the README;
     - they gain no entry, because the new README adds no path-shaped inline token;
     - a manifest test reads the new id, version, licence and author.
   - `ci/registered-failures.json`: the eight rows of the four publication tests stay registered, on Linux and Windows, until the anchor is pushed. Their reason text names the new pin.
6. **The publication commit.**
   - The seat builds it locally with the committed generator: `python -m library.local_orchestration.plugin_publication --repo . --manifest .claude-plugin/plugin.json --marketplace .claude-plugin/marketplace.json --ref refs/heads/publication-0.5.0`.
   - The generator repins the development `marketplace.json`. The package's own copy keeps the pin of forty zeros that the generator writes.
   - The run is repeated, and the second run gives the same commit id.
   - The seat creates the local ref `refs/heads/publication-0.5.0`. It pushes only its own development branch, to run CI; it pushes nothing else.
7. **The package check.** The seat extracts the publication commit into an empty directory and checks there:
   - it runs the gate scripts from that directory: `dispatch_lint.py` with `--ticket` (R7) and R8, `evidence_gate.py` on a receipt with an `effort:` line, and `usage_report.py` with an expectation that names a model and an effort;
   - the sha256 of every gate script equals that on the development branch;
   - `plugin.json` says `software-factory` and `0.5.0`;
   - the package holds no `.codex-plugin`, and none of these Level 2 files:
     - `install.ps1`, `johnny-install.cmd`, `johnny-router.ps1`, `requirements-runtime.lock`;
     - anything under `library/local_orchestration/`;
   - the package's README holds the Codex section and no Level 2 install section;
   - the development `marketplace.json` pins this commit, while the package's copy holds forty zeros.
8. **The local marketplace for testing**, built by the seat in `C:/Temp/claude/sf-050-local/` from the extracted package:
   - the plugin tree goes in `plugins/software-factory/`;
   - `.claude-plugin/marketplace.json` names `software-factory`, with source `./plugins/software-factory`;
   - `.agents/plugins/marketplace.json` gives the same entry with source `{"source": "local", "path": "./plugins/software-factory"}`.

   The STATEMENT lists the exact commands the owner runs to test it:
   - Claude Code: `claude --plugin-dir C:/Temp/claude/sf-050-local/plugins/software-factory`.
   - Codex: a fresh `CODEX_HOME`, then `codex plugin marketplace add C:/Temp/claude/sf-050-local`, then `codex plugin add software-factory@software-factory --json`.

   The seat does not run Codex or Claude itself.
9. **The changelog.** `doc/HARNESS-CHANGELOG.md` keeps its one-row-per-change table, with new rows, and adds a section `## 0.5.0`.
   - The rows name:
     - the router library retirement (tickets 65, 66, 68), and the documents cleared of retired surfaces (67);
     - the gate scripts as the default path;
     - the USAGE cell (69), and model and effort bound to each profile (76);
     - the template follow-ups (70), and the repository's own template with dispatch lint R7 (75);
     - the wave-3 rule texts (74);
     - review rounds and rework causes (73);
     - read-only lookups that go to the leaf (79);
     - the licence;
     - the rename to Software Factory.
   - The section is for outside readers. It states:
     - the retired surfaces: the flow engine, the private router, the profile, router telemetry, and the cross-lifetime bridge (the runner, wake, dispatch and review CLI families, and the live descriptor);
     - that the seven router-era SPECs are in `doc/archive/specs/2026/` as `ARCH-SPEC-20261118-001` to `007`, and nine ADRs are `SUPERSEDED`;
     - what to read instead: `AGENTS.md`, `Workflow.md`, `CodeReview.md` and `modules/spec/workflow-governance.md`;
     - the move from `johnny-ai-skill` to `software-factory`.
10. **Out of scope.** These keep the old name, with the reasons:
    - the skill id `johnny-project-takeover`, which renaming would break in every project that names it;
    - the activation markers `johnny-ai-skill:project-adoption` in `project_adoption_contracts.py`, which existing projects carry;
    - `.agents/plugins/johnny-ai-skill/`, the Antigravity registration;
    - everything Level 2, which ticket 78 retires.

**The release, after review approval, ticket 77's acceptance and the owner's confirmation at each push.** This is control-plane work, not this seat's:

1. Integrate this ticket into `cp/wave3`, and read CI back.
2. The owner renames `Johnny_AI_Skill_publication` to `software-factory-plugin`.
3. Push the publication commit to the publication repository with tag `plugin-v0.5.0`. The publication repository's `main` is the owner's to move, by force-with-lease from `0b3afd36`.
4. Push a branch `marketplace` to the publication repository. It holds one commit containing the development `marketplace.json` at this ticket's integration, both as `.claude-plugin/marketplace.json` and as `.agents/plugins/marketplace.json`. Later releases add commits to it, so it never needs a force push.
5. Push `refs/heads/publication-0.5.0` to the development repository.
6. Fast-forward the development `main` to `cp/wave3`, and tag `v0.5.0` there.
7. Read back from a fresh clone made with `--no-hardlinks`: check out `v0.5.0`, run `git branch publication-0.5.0 origin/publication-0.5.0`, then run `--verify-only --ref refs/heads/publication-0.5.0`.
8. Run one smoke install through the public path of the README's sections (3) and (4).
9. Remove the eight rows from `ci/registered-failures.json` in an additive commit. The CI run after the anchor push is expected to be red with `REGISTERED_NOW_PASSING` until that commit lands.

## 實作範圍、依賴與 ticket elements

### 角色指派（必填）

- 流程／Grill／ticket owner：control plane.
- implementation owner：`implementation-standard` seat in `.worktrees/71-publication`.
- reviewer：`ticket-review` seat in `.worktrees/71-publication-review`.
- **Owner override record**：the outward pushes wait for the owner's explicit confirmation in chat.
- `ImplementationHandoff`：this ticket; `library/local_orchestration/plugin_publication.py`; tickets 65 to 70.
- `ImplementationReturn`：`COMPLETED → ACTION_COMPLETED`／`BLOCKED → HALT`／`CHANGE_DETECTED → REQUIREMENT_CHANGED → Grill`。

### 前端組合與依賴注入

**N/A reason**：manifests and tests; no UI boundary.

- element 路徑：不適用
- 實際原始碼路徑：the paths in the boundary block
- 公開契約／資料模型：the manifest fields above.

## TDD 設計

1. 正常行為:
   - `--verify-only` with the new pin and the local anchor ref prints `verified <sha>` and exits 0.
   - The four publication tests pass on the host.
2. 規則違反／輸入錯誤:
   - a shipped manifest with `Proprietary`, with a version other than `0.5.0`, or with an author other than `Johnny Liu` fails a test of `tests/test_plugin_payload_boundary.py`;
   - a README that names `johnny-install.cmd` as an install step, or lacks the Codex `plugin add` step, fails a test there;
   - a manifest containing an `@` in any author or owner field fails.
3. 外部失敗／fail-closed: `--verify-only` without the anchor ref refuses, as today.
4. 回歸保護: the payload closure test passes. The publication tree carries `LICENSE`, `NOTICE` and `README.md`, and no retired module.

### 適用的缺陷類別

| # | 類別 | 是否適用 | 本工單的必要案例 |
| --- | --- | --- | --- |
| 1 | 路徑前綴誤匹配 | 否 | payload rules unchanged |
| 2 | null／空字串／陣列 | 是 | an empty author name fails |
| 3 | 權限繞過 | 是 | no e-mail address in a manifest; no push by the seat |
| 4 | Token 格式與比較 | 是 | the version string compared exactly, `0.5.0` |
| 5 | 錯誤碼是否一致 | 否 | no exit codes change |
| 6 | 例外是否會拋出 | 否 | no new code |

## 完成定義與證據

- The tests:
  - `python -m pytest tests/test_plugin_publication.py tests/test_plugin_payload_boundary.py -q` exits 0 on the host with the local anchor ref.
  - `mypy --strict --python-version 3.11` on the two test files exits 0.
- **G1**: the generator run twice, giving the same commit id both times.
- **V1**: `--verify-only` exits 0.
- **反向突變證據**, each restored after it turns a named test red:
  - put `Proprietary` back in one manifest;
  - put a Level 2 install section back in the README;
  - set the plugin `name` back to `johnny-ai-skill`;
  - drop `NOTICE` from the payload.
- **CI evidence**: one run on a commit of this branch, with both jobs `success`. The four publication rows stay registered until the anchor ref is pushed.
- **Receipt**: R4-7 cells, passing P9 and E1 (E1 runs last).

## 正式環境移植 SOP

- The publication push, the anchor push and the readback are the control plane's, after the owner confirms. The record holds:
  - the pushed commit id;
  - `git ls-remote` of both repositories;
  - one `--verify-only` run on a fresh clone made with `--no-hardlinks`.

## 完成回寫

- 實際檔案：`<paths>`
- commit：`<SHA>`
- WorkProgress：不適用
