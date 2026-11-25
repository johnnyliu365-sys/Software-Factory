# Ticket 71 revision05 — initial review (closure revision05)

- Seat: `ticket-review`, run id `R71-1`, model claude-opus-5-5. Process tier: strict. Review label: **initial**, closure revision05 (labelled before dispatch).
- Candidate: `7c321dfa720178c505fe413a89df8eb2054c88c1` (branch `cp/wave3-71-publication`) = base `41477f905ffe972f32cce0caba034f47150d5796` + `6f3f4707` (change) + `7c321dfa` (repin). Review worktree `.worktrees/71-publication-review`, detached at the candidate, porcelain empty before and after.
- Ticket read from `cp/wave3` at `efa03a7e` (state row `IN_PROGRESS; dispatch=sha256:253ac929…`). Dispatch `JAS-71-1.yaml` at `efa03a7e`: sha256 `253ac929d21d9e37840c28f8eb336d22e1dcb92837d0de6042a4622c3b0946e5`, recomputed, equal.
- Governance applied: `CodeReview.md` §1–§5, `skills/johnny-project-takeover/references/review-checks.md` (Test truthfulness row and Reviewer counter-mutation, Authorization bypass, Missing values, Token comparison). XSS: not applicable (manifests, Markdown and tests; no browser, WebView, DOM or JavaScript surface). Agent control / task-worktree: the seat's only Git effects were its branch push and the local ref; checked below.
- Publication commit: `d355b4a26336cebbe4e8e28650ce0120d4c39a13`, local ref `refs/heads/publication-0.5.0` (read, not moved).

## Findings

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S71-01 | `IMPLEMENTATION_DEFECT` (item 9) | Low | `doc/HARNESS-CHANGELOG.md` line 9 (first new row) | The row says "the seven router-era SPECs and nine superseded ADRs were archived (ticket 68)". The ADRs were not archived: ticket 68 marks nine ADRs `SUPERSEDED` in place (its boundary modifies `doc/adr/ADR-*.md` in place; `REQ-20261103-043` decision 2026-11-18 "1A" (4): "Router-era ADRs are marked `SUPERSEDED` … and stay in place"). The candidate's own `## 0.5.0` section states it correctly ("nine ADRs are `SUPERSEDED`"), so the record contradicts itself. | `doc/archive/specs/2026/` holds only the seven SPECs (`ARCH-SPEC-20261118-001`…`007`); `doc/adr/` still holds the ADRs; `modules/tickets/workflow-governance/68-archive-router-specs-and-adrs.md` title and boundary lines 27–32. | One additive commit rewording that row, e.g. "… the cross-lifetime bridge (ticket 66); the seven router-era SPECs were archived and nine ADRs marked `SUPERSEDED` (ticket 68)". `doc/` is outside the payload, so the publication commit `d355b4a2`, the pin and the eight registered rows are unaffected; rerun CI on the new commit. |
| S71-02 | `OUT_OF_SCOPE_HARDENING` | Low | `tests/test_plugin_payload_boundary.py` `_assert_readme_is_software_factory`, `_assert_shipped_manifests` | Exact texts of items 1 and 3 that the TDD matrix does not name are pinned only by `test_l5_stale_candidate_pin_is_named_before_generation`, which turns red on *any* payload byte change and is registered-failing on CI until the anchor push (overlap-masking shape, review-checks point 3). Reviewer counter-mutations that only `test_l5` caught: section headings 7 and 8 swapped with numbers kept (the test pins the numbers 1–10, not the titles); `--ref marketplace` dropped from the Codex `marketplace add` step; the section (1) "從 1.0 起…企業" sentence dropped; a retired-bridge sentence put back in section (2); `keywords` changed to `router` in both manifests at once (only plugin/entry equality is pinned, not the exact `description` and `keywords`). The candidate's texts are correct (checked byte for byte below); every case the ticket's TDD design names is pinned and red. | Mutations C5, C7, C8, C9, C11 in the counter-mutation table. | Carry to a later hardening ticket: pin the ten heading titles as an exact tuple and the exact `description`/`keywords` strings. Once release step 9 removes the eight rows, `test_l5` binds the payload bytes to the pin and closes the window for the payload files. |
| S71-03 | `OUT_OF_SCOPE_HARDENING` (note) | Low | README section 5, last sentence (ticket item 3 (5) text) | The ticket-mandated sentence "專案裡從早期版本複製過去的 AGENTS.md 與 Workflow.md，要換成 0.5.0 的版本" tells users to keep copies of plugin governance files in their project, which sits uneasily with `Workflow.md` P0 governance-document-ownership ("不得複製…到 target project"). The seat wrote the ticket text exactly, and `REQ-20261120-044` T2 already treats project copies as a fact to version-check, so this is not a seat defect and does not block. | `Workflow.md` lines 41–52; `REQ-20261120-044` row T2; ticket item 3 (5). | Route to the control plane with `REQ-20261120-044` (wave 4): decide whether migration advice is "replace" or "remove the copied plugin files". No change in this ticket. |

No blocking finding other than S71-01. No `TICKET_DEFECT`, no `EVIDENCE_DEFECT`, no `RETURN_UNTRUE`.

## Seat's flagged points

| # | point | judgement |
| --- | --- | --- |
| 1 | Forbidden routes in `test_l3_rejects…` gained `_RAW_CANDIDATE_MARKETPLACE_URL` and `_RAW_MAIN_MARKETPLACE_URL` | Within item 5 and the boundary. `tests/test_plugin_publication.py` is a `modify` path; the change strengthens, does not weaken (the dispatch forbids only skipping/deleting/weakening), keeps both constants meaningful after the route tuple stopped using them, and is named in the STATEMENT. The kept `_RAW_PUBLICATION_MAIN_MARKETPLACE_URL` entry now equals the allowed line and stays red as a duplicate route (test passes, P1). Accepted. |
| 2 | New classes `ShippedManifestTests`, `PublicationTreeContentTests` | Within item 5 and required by the TDD design: TDD 2 puts the manifest (`Proprietary`, version, author, `@`), README (`johnny-install.cmd`, Codex `plugin add`) cases in `tests/test_plugin_payload_boundary.py`; TDD 4 requires `LICENSE`/`NOTICE`/`README.md` carried and no retired module; defect rows 2–4 (empty author, e-mail, exact `0.5.0`) are cases in `test_a_wrong_manifest_value_is_red…`. Imports of `declared_payload_paths` and `materialise_publication_tree` only read `library/`. Accepted. |
| 3 | K1 used the ticket at `efa03a7e` as `--ticket` | Correct. The base copy (41477f90) differs from `efa03a7e` only in the state row, and only `efa03a7e` carries `dispatch=sha256:253ac929…`. Reproduced from the extracted package: `--ticket <efa03a7e copy>` → `LINT PASS` exit 0; `--ticket <base copy>` → `R7 state row: expected dispatch=sha256:253ac929…, found no dispatch=sha256:` exit 1. Accepted. |
| 4 | F1 shows only acr2 locally | Confirmed on CI run 45664775629 (head `7c321dfa`, both jobs `success`): linux and windows each list the four publication tests as `FAILED` (`PinnedCommitError` / "the pinned sha names no commit in this repository"; origin has no `publication-0.5.0`), windows also acr2 (5 failed); `ci/check_registered_failures.py` printed nothing and passed on both jobs, and neither log contains `REGISTERED_NOT_FAILING`, `UNREGISTERED_FAILURE` or `REGISTERED_NOW_PASSING`. So they are registered-failing, not `REGISTERED_NOT_FAILING`. Accepted. |

## Per-check results

| # | check | result | evidence |
| --- | --- | --- | --- |
| 1a | `plugin.json` exact fields (item 1) | PASS | Parsed and compared: `name` `software-factory`, `version` `0.5.0`, `license` `Apache-2.0`, `author` `{name: Johnny Liu, url: https://github.com/johnnyliu365-sys}`, `homepage`/`repository` `https://github.com/johnnyliu365-sys/software-factory-plugin`, `description` and `keywords` equal to the ticket strings. `payload` and `skills` equal to base; changed keys are exactly the eight named. |
| 1b | `marketplace.json` (item 1) | PASS | `name`, entry `name` `software-factory`; `owner` `{name: Johnny Liu, url: …}`; description equal to the ticket string; one entry; entry `version`, `license`, `author`, `homepage`, `repository`, `description`, `keywords` equal to `plugin.json`; `source` = `{"source":"url","url":"https://github.com/johnnyliu365-sys/software-factory-plugin.git","sha":"d355b4a26336cebbe4e8e28650ce0120d4c39a13"}`. No `@` and no `mail` in either manifest file. |
| 1c | `NOTICE` (item 2) | PASS | Diff changes only line 1 (`Software Factory`) and the `Repository:` line (publication URL); other lines unchanged. |
| 1d | README (item 3) | PASS | Ten `##` sections in the ticket's order with the ticket's titles, numbered `1.`–`10.`; section 5 renders `johnny-ai-skill` as plain text (the README carries no inline code at all, consistent with the no-inline-code rule; title text otherwise identical). Section 3: exactly the five commands, in order, each at column 0, each in its own fenced block (no indented `claude plugin` line anywhere). Section 4: the five Codex steps with the ticket's versions, commands and expected `version`/`installed`/`enabled`. Section 5: remove commands for `johnny-ai-skill@johnny-ai-skill` on both hosts, then install; copies sentence (see S71-03). Section 6: `uninstall` in a fenced block (same launcher path as today's `status` block); removes/leaves text matches `library/local_orchestration/live_uninstall_composition.py` (`.johnny-owned` marker, five receipt directories, journal and empty root cleared, foreign directory halts with ledger kept); hand-deletion condition stated. No backtick outside fences; link targets: `LICENSE`, `NOTICE` (payload paths, in the author line and section 10) and two external `https://github.com/johnnyliu365-sys` profile links plus one autolink (not repository paths; the closure scan's concern per S71R-23). No Level 2 install step, no `johnny-install.cmd`; the two retired-bridge sentences are absent; section 1 has "從 1.0 起，它的目標對象是企業". Sections 7–10 carry the ticket content (roadmap order 0.5.0 → wave 4 → beta → 1.0 enterprise, Docker Compose → SaaS). |
| 1e | `SKILL.md` sentence (item 4) | PASS | One sentence replaces the launcher sentence: "A 0.4.x Level 2 runtime is removed by its own `uninstall`, as the README describes." No path token in backticks; the no-runner statement and the honest statement before it are unchanged. |
| 1f | Changelog (item 9) | FAIL (S71-01) | Ten new rows naming each required subject, with existing ticket files as "Where" (all twelve paths exist). `## 0.5.0` section states every required point. Row 1 misstates the ADRs as archived. |
| 2 | Tests (item 5) | PASS | Diff read in full: `_RELEASE_VERSION` 0.5.0; `_PUBLICATION_URL` and `_RAW_PUBLICATION_MAIN_MARKETPLACE_URL` exactly the ticket values; route tuple = the one `marketplace add` line; injection anchor = that line; `test_t6` `0.5.0`; install/update/uninstall/remove assertions use `software-factory`; `test_references_qualify_receipt_bridge_by_lifetime` lost only the README read and its two assertions. `_REFERENCES_OUTSIDE_PAYLOAD` lost `johnny-install.cmd`; neither closure dictionary gained an entry. Eight registered rows kept (four per OS, linux and windows), reason names `d355b4a2…`. STATEMENT line numbers checked (106, 108, 125–126, 744, 767–776, 780–788, 940, 992–1005; 650, 716, 762, 777, 861): correct. |
| 2b | P1 rerun at candidate | PASS | `pytest tests/test_plugin_publication.py tests/test_plugin_payload_boundary.py tests/test_governance_consistency.py tests/test_entry_read_only_lookup.py -q -rfEs -p no:cacheprovider` in the review worktree: `228 passed, 876 subtests passed in 59.00s`, exit 0 (same counts as the receipt). |
| 2c | T1 rerun | PASS | `mypy --strict --python-version 3.11` on the two test files: `Success: no issues found in 2 source files`, exit 0. |
| 3a | G1 regeneration (item 6) | PASS | Exact item-6 command, twice, in `git clone --no-hardlinks` of the candidate (`g1-R71-1`): `publication commit d355b4a2…` both runs, `repinned d355b4a2… -> d355b4a2…`, exit 0, porcelain empty. Repeated in a `file://` single-branch clone (`g1b-R71-1`) in which `d355b4a2` was verified **absent** before the run: same id twice. |
| 3b | V1 at candidate | PASS | `--verify-only --ref refs/heads/publication-0.5.0` in the review worktree: `verified d355b4a26336cebbe4e8e28650ce0120d4c39a13`, exit 0. Fail-closed: same command with an absent ref → `PublicationReachabilityError: the pinned sha is not reachable from its pushable anchor`, exit 1. |
| 3c | Package check (item 7) | PASS | `git archive d355b4a2 \| tar -x` into empty `pkg-R71-1`: 149 files; absent: `.codex-plugin`, `install.ps1`, `johnny-install.cmd`, `johnny-router.ps1`, `requirements-runtime.lock`, `library/local_orchestration/` (find: none at any depth). `plugin.json` byte-equal to the candidate's (`software-factory`, `0.5.0`). Package `marketplace.json` `sha` = forty zeros; development copy pins `d355b4a2…` (the only diff between the two). README byte-equal to the candidate's: Codex section present, no Level 2 install heading, no `johnny-install.cmd`. `LICENSE`, `NOTICE` byte-equal. All 13 files of `skills/johnny-project-takeover/scripts/` sha256-equal to the candidate. Gate scripts run from the package: `dispatch_lint.py` R7 pass/fail as in flag 3; R8 (`effort:` line removed) → `R8 profile: without effort:` exit 1; `evidence_gate.py` on the receipt (its USAGE cell has `effort: high`), E1 arguments, `--repo` the review worktree, `--candidate 7c321dfa…` → `cells=11 defects=0` exit 0, for both `RETURN.md` and `RETURN.as-returned.md`; `usage_report.py --expectation doc/handoffs/2026/workflow-governance/usage-expectation.json RETURN.md` → `model=claude-sonnet-5-5 effort=high output=82150 processed=18279229 WITHIN` exit 0, and with an expectation naming effort `xhigh` → `EFFORT_MISMATCH` exit 1. Note: the generated commit's author is `Johnny Liu <software-factory@invalid>` (generator identity, reserved TLD; generator is out of boundary; not a manifest). |
| 4 | Local marketplace (item 8) | PASS | `C:/Temp/claude/sf-050-local/` holds exactly `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `plugins/software-factory/`. Claude file: `software-factory`, entry source `./plugins/software-factory`. Codex file: same entry, source `{"source":"local","path":"./plugins/software-factory"}`. `diff -r plugins/software-factory pkg-R71-1`: identical (149 files). STATEMENT item 3 lists the owner's Claude and Codex commands. |
| 5 | Out of scope (item 10) | PASS | Candidate diff touches only the nine boundary files; untouched: skill id directory `skills/johnny-project-takeover`, `library/workflow_router/project_adoption_contracts.py`, `.agents/plugins/johnny-ai-skill/`, every Level 2 file, `skills/apply-reusable-modules` description, the ticket-79-pinned description. |
| 6 | Boundary gate | PASS | `document_mutation_gate.read_boundary` on the ticket at `efa03a7e` → `DECLARED`; `parse_raw_diff` of `git diff --raw -z --no-renames 41477f90 7c321dfa` → nine `MODIFY` changes, `evaluate_change` `None` for each, `evaluate_changes` → `(None, None)` (admitted). No forbidden path touched. |
| 7 | Mutation evidence | PASS for the ticket's four and the reviewer's TDD-door mutations; gaps → S71-02 | Table below. Driver in a `--no-hardlinks` clone with the local anchor ref, both full test files per mutation (no `-x`), unfiltered output saved and read (FAILED/SUBFAILED lines), restored with porcelain empty after each. |
| 8 | Receipt truth | PASS | STATEMENT items 1–4 checked: publication id (G1), only `cp/wave3-71-publication` pushed (`git ls-remote origin`: no `publication-0.5.0`, no `v0.5.0`; publication repository `main` and `plugin-v0.4.14` still `0b3afd36`, no `plugin-v0.5.0`, no `marketplace` branch), CI claims, line numbers, owner commands, residue (`71-publication-scratch` empty, no `r71a` path, no host lock). Commits: author Johnny Liu `<johnny.liu365@gmail.com>`, last line `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (dispatch model `claude-sonnet-5-5`). The appended USAGE cell is the only difference from the as-returned copy. P1 and V1 rerun equal. |

## Mutation table

`test_l5_stale_candidate_pin_is_named_before_generation` turns red on any payload byte change (control C0, a JSON reformat of the manifests, is red on it alone) and is registered-failing on CI, so it is discounted when judging whether a property is pinned.

| id | door | mutation | red beyond `test_l5` | verdict |
| --- | --- | --- | --- | --- |
| C0 | control | both manifests re-serialised, values unchanged | none | expected (shows the `test_l5` mask) |
| S1 | seat | `plugin.json` `license` `Proprietary` | `test_the_shipped_manifests_carry…`, `test_a_wrong_manifest_value…` | red |
| S2 | seat | Level 2 install section appended to README | `test_the_readme_is_the_software_factory_readme`, `test_a_level_two_install_step…` | red |
| S3 | seat | plugin `name` `johnny-ai-skill` | `test_the_shipped_manifests_carry…`, `test_a_wrong_manifest_value…` | red |
| S4 | seat | `NOTICE` dropped from `payload.files` | `PublicationTreeContentTests` ×3 (incl. SUBFAILED `NOTICE`), `PayloadClosureTests` ×3 | red |
| C1 | reviewer: e-mail in author | `"email": "someone@example.org"` in the marketplace entry `author` | `test_no_shipped_manifest_holds_an_email_address` (SUBFAILED marketplace.json), `test_the_shipped_manifests_carry…`, `test_a_wrong_manifest_value…`, `test_the_pin_and_the_tree_are_one_fact` | red |
| C2 | reviewer: address through another field | `owner.url` = `mailto:someone@example.org` | `test_no_shipped_manifest_holds_an_email_address` (SUBFAILED marketplace.json), `test_the_shipped_manifests_carry…` (`@` in owner), `test_a_wrong_manifest_value…`, `test_the_pin_and_the_tree_are_one_fact` | red |
| C3 | reviewer: sixth command | fenced `claude plugin list` added to section 3 | `test_the_readme_is_the_software_factory_readme` | red |
| C4 | reviewer: reorder | `update` and `uninstall` swapped in section 3 | `test_the_readme_is_the_software_factory_readme` | red |
| C5 | reviewer: heading reordered | titles of sections 7 and 8 swapped, numbers kept | none | **not pinned → S71-02** |
| C6 | reviewer: inline-code path | `live_uninstall_composition.py` as a backticked repository path | `PayloadClosureTests` ×3 | red |
| C7 | reviewer: copy/equality | `keywords` `router` in both manifests | none | **not pinned → S71-02** |
| C8 | reviewer | `--ref marketplace` dropped from Codex step 2 | none | **not pinned → S71-02** |
| C9 | reviewer | section 1 enterprise sentence dropped | none | **not pinned → S71-02** |
| C10 | reviewer | old launcher sentence restored in `SKILL.md` | none | not pinned (item 4 has no TDD case; noted under S71-02's carry) |
| C11 | reviewer | retired-bridge sentence restored in README section 2 | none | **not pinned → S71-02** |

## Commands and residue

- Python `C:/Temp/claude/jas-venv/Scripts/python.exe`, `PYTHONUTF8=1`; one pytest at a time, no other pytest running at start (process list empty). The full suite was not run (CI and the receipt's F1 cover it; no host lock taken).
- Scratch `.worktrees/71-publication-review-scratch/` held `g1-R71-1`, `g1b-R71-1`, `pkg-R71-1`, `fix-R71-1`, `mut-R71-1`, two `ci-*-R71-1.log`; all removed with the scratch directory before return, as were `P1-R71-1.txt` in this folder and the `.mypy_cache` the T1 rerun created in the review worktree. `refs/heads/publication-0.5.0` still names `d355b4a2…`; `C:/Temp/claude/sf-050-local/` only read. No `claude` or `codex` run; nothing pushed. PROCESSES_LEFT=0.

```review-verdict
candidate: 7c321dfa720178c505fe413a89df8eb2054c88c1
verdict: CHANGES_REQUESTED
round: initial
closure_revision: revision05
reviewer: ticket-review seat R71-1 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 7c321dfa720178c505fe413a89df8eb2054c88c1
round: 1
kind: INITIAL
verdict: CHANGES_REQUESTED
causes: IMPLEMENTATION_DETAIL
```

## Revision05 correction review

- Seat: `ticket-review`, run id `R71-2`, model claude-opus-5-5. Label: **correction**, closure revision05 (the one correction review §5 allows; rule B applies).
- Candidate: `824d00b9298253bebb2b4adea986e09185ffba0a`, one additive commit whose parent is `7c321dfa` (`docs(changelog): … (ticket 71, S71-01)`), author Johnny Liu, last line `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Review worktree detached at it, porcelain empty.

### Findings

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S71-01 | `IMPLEMENTATION_DEFECT` (item 9) | Low | `doc/HARNESS-CHANGELOG.md` line 9 | **Closed.** The row now reads "… the seven router-era SPECs were archived and nine ADRs marked `SUPERSEDED` (ticket 68)". This agrees with the `## 0.5.0` section, which is byte-unchanged ("nine ADRs are `SUPERSEDED`"), and with `REQ-20261103-043`'s decision of 2026-11-18 "1A" (4) (SPECs archived; ADRs marked `SUPERSEDED` and kept in place). | `git diff --stat 7c321dfa 824d00b9`: only `doc/HARNESS-CHANGELOG.md`, 1 insertion and 1 deletion, on that row. | — |
| S71-04 | `EVIDENCE_DEFECT` | Low | `RETURN.md` STATEMENT item 2, last paragraph | The STATEMENT says `doc/HARNESS-CHANGELOG.md` has "nine new rows and a section 0.5.0". The candidate adds **ten** rows: `git diff 41477f90 824d00b9 -- doc/HARNESS-CHANGELOG.md \| grep -c '^+\| 2026-11-26'` gives 10 (the ticket-67 row stands apart from the 65/66/68 row). The same wording was in the initial receipt; the initial review (R71-1) missed it, so it is first recorded here. The deliverable is correct (the review checked all ten rows) and only the receipt's count is wrong. It does not change any exit-code classification, scope, security or P0. | the grep above; per-check 1f of the initial review | No code change. Under §5 rule B, the control plane records the correct count ("ten new rows") in the convergence disposition and carries the item. |
| S71-02, S71-03 | `OUT_OF_SCOPE_HARDENING` | Low | as in the initial review | Unchanged, carried as before; the STATEMENT says they were not part of this correction. | — | as in the initial review |

No new defect in the diff.

### Checks

| # | check | result | evidence |
| --- | --- | --- | --- |
| 1 | Diff scope and row truth | PASS | One file, one row (above). The boundary is unchanged (`doc/HARNESS-CHANGELOG.md` is a `modify` path). `git diff --quiet 7c321dfa 824d00b9 -- .claude-plugin ci README.md NOTICE skills tests` gives exit 0: the pin, the eight registered rows and every payload file are unchanged. |
| 2 | Publication commit unchanged | PASS | Item-6 command run twice in a `file://` single-branch `--no-hardlinks` clone of `cp/wave3-71-publication` at `824d00b9` (`g1-R71-2`), in which `d355b4a2` was **absent** before the run. Both runs print `publication commit d355b4a26336cebbe4e8e28650ce0120d4c39a13`, repin `d355b4a2 -> d355b4a2`, exit 0, porcelain empty. `--verify-only --ref refs/heads/publication-0.5.0` in the review worktree: `verified d355b4a2…`, exit 0. The ref still names `d355b4a2`. |
| 3 | CI readback | PASS | Run 45672667429: head `824d00b9`, completed, `success`; jobs `test (linux)` 139411830503 and `test (windows)` 139411831026 both `success`. Linux: 298 failed, 3210 passed, the same profile as run 45664775629. Windows: 5 failed, which are acr2 plus the four publication tests (`PinnedCommitError`; origin has no `publication-0.5.0`). `check_registered_failures.py` printed nothing in either job. Neither log contains `REGISTERED_NOT_FAILING`, `UNREGISTERED_FAILURE` or `REGISTERED_NOW_PASSING`. |
| 4 | Receipt and STATEMENT | PASS except S71-04 | All 11 cells carry `candidate: 824d00b9…`. The captures show: P1 228 passed, 876 subtests; T1 clean; G1 `d355b4a2` twice; V1 verified; C1 head `824d00b9` success; F1 only acr2 failed (1 failed, 3443 passed). Rerun here: E1 arguments with `--candidate 824d00b9…` give `cells=11 defects=0`, exit 0, on both `RETURN.md` and `RETURN.as-returned.md`; `usage_report.py` with the repository expectation gives `output=92029 processed=23430033 WITHIN`. The appended USAGE cell is the only difference from the as-returned copy. STATEMENT item 1 checked: only `cp/wave3-71-publication` is on origin; the publication repository `main` is still `0b3afd36`, with no 0.5 tag and no `marketplace` branch. Item 4 checked: the seat's `-scratch` is empty and no host lock is left. Item 2 is true apart from the row count (S71-04). |

### Residue

`.worktrees/71-publication-review-scratch/` (`g1-R71-2`, `ci-R71-2.json`, two `ci-*-R71-2.log`) was removed before return. Nothing else was written outside this file. No pytest was run in this round. `claude` and `codex` were not run, nothing was pushed, and `refs/heads/publication-0.5.0` was not moved. PROCESSES_LEFT=0.

```review-verdict
candidate: 824d00b9298253bebb2b4adea986e09185ffba0a
verdict: CONVERGENCE_REVIEW_REQUIRED
round: correction
closure_revision: revision05
reviewer: ticket-review seat R71-2 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 824d00b9298253bebb2b4adea986e09185ffba0a
round: 2
kind: CORRECTION
verdict: CONVERGENCE_REVIEW_REQUIRED
causes:
```

## Convergence disposition (control plane, 2026-11-26)

The correction review returned `CONVERGENCE_REVIEW_REQUIRED`: every blocking finding is closed and the open findings are non-blocking under CodeReview §5 rule B. Each carried finding keeps the smallest fix the reviewer named (lesson L-19).

```convergence-disposition
candidate: 824d00b9298253bebb2b4adea986e09185ffba0a
reviewer_verdict: CONVERGENCE_REVIEW_REQUIRED
disposition: APPROVED
rule: CodeReview §5 rule B (owner-approved 2026-11-05)
carried:
  - S71-02
  - S71-03
  - S71-04 (the STATEMENT's "nine new rows" is ten)
```

The reviewer's rework-record for round 2 named `RETURN_UNTRUE`, for S71-04. Under the rework-record rule of ticket 73, a `CONVERGENCE_REVIEW_REQUIRED` round whose disposition approves carries empty causes, so the control plane emptied them. S71-04 stays carried above.

## Seat token use (readiness criterion 5)

Host-reported usage per seat, summed per unique message id, against the expectation the owner confirmed on 2026-11-18 ("1A"); appended to the receipt as `USAGE` cells at integration.

| Seat | Model | input | cache write | cache read | output | processed | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seat:implementation-standard/JAS71R1` | claude-sonnet-5-5 | 258 | 513459 | 22916316 | 92029 | 23430033 | WITHIN |
| `seat:ticket-review/R71` | claude-opus-5-5 | 164 | 463023 | 12776588 | 71680 | 13239775 | WITHIN |
