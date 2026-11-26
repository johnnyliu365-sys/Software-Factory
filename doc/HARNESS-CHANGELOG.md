# Harness change log

One row per change that altered what the plugin does. Working history lives in Git; the revision-135 checklist stays on branch `codex/skill-improvement-checklist` at `doc/AI-SKILL-IMPROVEMENT-CHECKLIST.md` and is not carried onto this line. This table is not a progress tracker.

| Date | Change | Authority | Where |
| --- | --- | --- | --- |
| 2026-11-03 | Gates-first control plane: state in files, transitions by scripts; integration by script; stages by intake mode; four test layers; CI invariants only | `PRD-20261103-043` | `modules/spec/workflow-governance.md` Revision 04, `Workflow.md` section 0, `CodeReview.md` |
| 2026-11-03 | Commit identity of the wave-1 branch rewritten to the repository identity (owner decision); trees unchanged; old-to-new map committed | project owner, 2026-11-03 | `doc/reviews/workflow-governance/evidence/47/commit-identity-rewrite-2026-11-03.txt` |
| 2026-11-26 | The router library was retired: the flow engine, the private router and the profile (ticket 65), the cross-lifetime bridge (ticket 66), and the seven router-era SPECs were archived and nine ADRs marked `SUPERSEDED` (ticket 68) | `REQ-20261103-043`, owner decision 2026-11-18 "1A" | `modules/tickets/workflow-governance/65-retire-engine-and-private-router.md`, `66-retire-bridge.md`, `68-archive-router-specs-and-adrs.md` |
| 2026-11-26 | The documents were cleared of retired surfaces (ticket 67) | `REQ-20261103-043` | `modules/tickets/workflow-governance/67-governance-document-sweep.md` |
| 2026-11-26 | The gate scripts are the default path: each step is decided by a script reading the state files | `REQ-20261103-043` | `skills/johnny-project-takeover/scripts/` |
| 2026-11-26 | The USAGE cell reports token use per seat (ticket 69); the model and the effort are bound to each profile (ticket 76) | `REQ-20261103-043` | `modules/tickets/workflow-governance/69-token-use-per-seat.md`, `76-seat-model-and-effort-bound.md` |
| 2026-11-26 | The template follow-ups (ticket 70); the repository's own tickets follow the template, with dispatch lint R7 (ticket 75) | `REQ-20261103-043` | `modules/tickets/workflow-governance/70-wave2-template-and-hygiene.md`, `75-own-tickets-follow-the-harness.md` |
| 2026-11-26 | The wave-3 rule texts (ticket 74) | `REQ-20261103-043` | `modules/tickets/workflow-governance/74-wave3-rule-texts.md` |
| 2026-11-26 | Review rounds and the cause of each rework are recorded (ticket 73) | `REQ-20261103-043` | `modules/tickets/workflow-governance/73-review-rounds-and-rework-cause.md` |
| 2026-11-26 | A read-only lookup goes to the leaf document and does not load the workflow (ticket 79) | `REQ-20261103-043` | `modules/tickets/workflow-governance/79-read-only-lookup-goes-to-the-leaf.md` |
| 2026-11-26 | A read-only lookup goes through the 流程索引, and the index gains rows for the two P0 sections, the start order and the target project's sources (ticket 80) | `REQ-20261103-043`, owner decision 2026-11-26 "A" | `modules/tickets/workflow-governance/80-lookup-through-the-index.md` |
| 2026-11-26 | The skill stops when the old plugin johnny-ai-skill is still installed; the README explains the host's decline record; a version is never published twice; the first 流程索引 row is narrowed to the lookup's own rules, with a table-order tie-break (ticket 81) | `REQ-20261103-043`, owner decisions 2026-11-26 | `modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md` |
| 2026-11-26 | The plugin ships a SessionStart hook that names its rules file and sends a read-only lookup to the 流程索引 first (ticket 82) | `REQ-20261103-043`, owner decision 2026-11-26 "A" | `modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md` |
| 2026-11-26 | The licence is Apache License 2.0, and the author is Johnny Liu | owner decision 2026-11-18 "2A" | `LICENSE`, `NOTICE` |
| 2026-11-26 | The plugin is renamed from `johnny-ai-skill` to `software-factory` (Software Factory), version 0.5.0; the marketplace moves into the public publication repository; the README is rewritten | owner decision 2026-11-20 | `modules/tickets/workflow-governance/71-publication-0-5.md` |

## 0.5.0

Version 0.5.0 is the first release as Software Factory. This section is for readers outside the project.

### What was retired

- The flow engine was retired in 0.5.0.
- The private router was retired in 0.5.0, and so was the profile that selected a router.
- Router telemetry was retired in 0.5.0.
- The cross-lifetime bridge was retired in 0.5.0: the runner, wake, dispatch and review CLI families, and the live descriptor.
- The Level 2 runtime is no longer shipped. A 0.4.x Level 2 runtime is removed by its own `uninstall`, as the README describes.

### What to read instead

- The seven router-era SPECs are in `doc/archive/specs/2026/` as `ARCH-SPEC-20261118-001` to `007`, and nine ADRs are `SUPERSEDED`.
- To learn how the workflow runs now, read `AGENTS.md`, `Workflow.md`, `CodeReview.md` and `modules/spec/workflow-governance.md`.
- A question about a rule is answered through the 流程索引 of `AGENTS.md`: its row links the one section to read, and a keyword search is not a way to find a rule.
- Each session receives, from the plugin's SessionStart hook, the path of its rules file and the instruction to start a lookup at the 流程索引.

### The move from `johnny-ai-skill` to `software-factory`

- The plugin id is now `software-factory`, and the marketplace is `software-factory`. The old id was `johnny-ai-skill`.
- To switch, remove the old plugin with each host's remove command for `johnny-ai-skill@johnny-ai-skill`, then install as the README's sections 3 and 4 describe.
- Codex installs through `codex plugin marketplace add` and `codex plugin add`.
- The licence is Apache License 2.0, and the author is Johnny Liu.
- The skill id `johnny-project-takeover` keeps its name, because renaming it would break every project that names it.
- With both plugins installed, the new skill stops at its first step and asks the user to remove the old one and open a new session.

## Checklist items carried from revision 135

| Item | Status at freeze | Disposition under Revision 04 |
| --- | --- | --- |
| 01 主線與單票 | 30B review blocked | superseded by the contract gate (wave 2) |
| 02 已核准工作接續 | local integrated, effect open | state-in-files continuation (R4-1); grant-issuer and admit_dispatch residuals carried to wave 2 queue admission (R4-7) |
| 03 派工完整最小 | local integrated | dispatch lint script (wave 1); host-admission residuals carried to wave 2 |
| 04 TEST → A → B | complete local | kept; four layers (R4-6) |
| 05 候選來源與 Expected | contract local | contract gate provenance check (wave 2) |
| 06 共用樹覆蓋 | worker claim local | one writer per file; integration script (wave 2) |
| 07 完成與證據 | projection integrated | evidence gate (wave 2) |
| 08 測試依賴／退役 | local command source | coverage map script (wave 2) |
| 09 窄修窄審 | cases verified | kept as review policy |
| 10 成本／外部呼叫／回報 | local integrated | token column in receipts (wave 2) |
| 11 去重與衝突 | local integrated | requirement snapshot ids (wave 2) |
| 12 回放與獨審 | end to end not verified | implementation-readiness criterion 1 (fixture target project, session ended mid-ticket and resumed from files) is wave 2 acceptance; criteria 2–5 in REQ-20261103-043 |
| 13 歷史 SPEC 舊規則殘留 | precedence notes (wave 1) | sentence-level sweep over every SPEC and dated runbook with the ticket 47 D7 instrument, a contract-gate pin for both halves of R4-1 (dispatch = ticket state row; queue = integration candidates only), the D7/D8/D9 instrument gaps listed in ticket 47 correction 1 of revision09, the ticket 48 carried findings F-06, NF-04, NF-08, NF-16 (receipt checker clauses) and NF-17 (annotated-tag pins), and ticket 47 N9-03 (precedence waiver wording) (wave 2); archive through requirement lineage when the router library retires (wave 3) |
