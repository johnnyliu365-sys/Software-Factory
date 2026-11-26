# Control-plane work log — Software Factory (formerly Johnny_AI_Skill)

Repository: `johnnyliu365-sys/Software-Factory` (private), branch `cp/wave3`. Local checkout: `C:/Users/User/Desktop/Johnny_AI_Skill`.

This file lives in the repository, so it is versioned and the pins are checked by the repository's own `index_pins.py`. Rule for whoever resumes: this log holds pointers and pins. The content of every decision lives in the pinned files. After compaction, run the pin check below first. If any row drifted, read that file before acting, and do not trust a summary's wording.

```text
py -3.11 skills/johnny-project-takeover/scripts/index_pins.py --check --root . doc/handoffs/2026/workflow-governance/control-plane-worklog.md
```

Run it from the repository root.

## Pinned index

| id | kind | state | revision | digest | leaf |
| -- | ---- | ----- | -------- | ------ | ---- |
| agents | governance | open | git:d7623817149f5625b5998d5f3df00a1fc20f5b2e | sha256:e89b2a2e294998ed0f9b1684fdcb2ed9d830ca949d9d5074bd2315a30f7b9718 | AGENTS.md |
| workflow | governance | open | git:c2bccb7c0c8de9719cb48c40e49169bc9a2b777b | sha256:e090c065a26c4131aedf737a0161ce2cd62500bcc33a41b15d706acc8a8dba6e | Workflow.md |
| codereview | governance | open | git:9ae502de5dbbf7e36b39179bcfbbc0a1d380519e | sha256:7665a6e41aba778fb873435841197bd2db2b2fb3a4e062bb78af088d6114dff9 | CodeReview.md |
| req043 | requirement | open | git:22ddb00c2385e3212edc4068ddd30f92fc86f941 | sha256:dedf2f8f79773daad713dec2054fd5fe17c60c88c6fc8960c937a13a330127e6 | doc/requirements/active/2026/workflow-governance/REQ-20261103-043.md |
| req044 | requirement | open | git:96792d116d414ca618f471d38bf036438cd37622 | sha256:74c2a38c5f1fae54bf74fbb44f22c1564754e15be9f042b6d5fd3b6ede1ca2bd | doc/requirements/active/2026/workflow-governance/REQ-20261120-044.md |
| req045 | requirement | open | git:96792d116d414ca618f471d38bf036438cd37622 | sha256:e46179a193a89de0e4e198b275afbcdaedc0acbebdb4a0713ca6cded383505f3 | doc/requirements/active/2026/workflow-governance/REQ-20261120-045.md |
| tickets | index | open | git:6eae7d41aba3bc6c739a1975a3ddc5c5330108da | sha256:2cc75a895bef3136988036a5990756d2903e57c6474d593176928070e95f087f | modules/tickets/workflow-governance/README.md |
| t71 | ticket | open | git:0cfb563b20667af140e21f9d61a8e272aa382466 | sha256:5113d014656bfe1ea805f7edde7a2740699094145abb3213a584bf5a5e77ca41 | modules/tickets/workflow-governance/71-publication-0-5.md |
| t71review | review | open | git:68795ea281ffdb8a6f7b4340bf9bfc9ef949d108 | sha256:9a86b7e900064523ba14dc700d4458bf2ef9337b32df71c594d8b1f7b3761fe5 | doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md |
| t79 | ticket | open | git:efa03a7edd6a1a8a9077959228307fc70ac68fa0 | sha256:06b34754e6f2bd2254d6da8729c94321970b484464754bf2a82344753e47f7e5 | modules/tickets/workflow-governance/79-read-only-lookup-goes-to-the-leaf.md |
| integration | record | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:1b83b83d9ae46498852a9407ed7e4b90610289fcda28cc540f1abb9573fbc77a | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| expectation | state | open | git:9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | sha256:65f3ba13d08cddeae628f5b85bd57618f93f3ff7730af673df7c3421208318d5 | doc/handoffs/2026/workflow-governance/usage-expectation.json |
| t77 | ticket | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:359b639edb552ee489f37f10e54df570d0a649239d100cf6f99329da05c4df72 | modules/tickets/workflow-governance/77-acceptance-0-5-0.md |
| t77record | record | open | git:ef8f4d659c9db7143ca1ecbd685b0566c397e0b2 | sha256:97afb50c69ba6b70d62d4b798b28ab3211bf1b0f4a558573810af910598dd8be | doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md |
| t80 | ticket | open | git:2a34bce4d267c8655f23e440f0486297ffbb1beb | sha256:fa2668353870a941eb69862250a5acdbaf934a4a2c945510d9fa8dbbc1c86e3b | modules/tickets/workflow-governance/80-lookup-through-the-index.md |
| t81 | ticket | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:a372e81107b6e95cca035c50cb0861d3f835652ae1b4aa925dc60bd620d2f01a | modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md |
| t82 | ticket | open | git:5769c0d87952af2a86dfd60927da1f52e1dc97af | sha256:208505eb5d5190bff2ae0fae5b9b77c1de15eab402dffa78cf05c542ec4a3d6c | modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md |
| t82ticketreview | review | open | git:44018a0b2ec66534be52c39e002774fe3ebb98f4 | sha256:5178b285db93a78736c1f353405d100dc6349a1fe8434825fd84f01baec29f4f | doc/reviews/workflow-governance/82-session-hook-points-to-the-index-ticket-review.md |
| t82review | review | open | git:edee7ce9bb8b447c1019d1baba9c4258ee8c3e92 | sha256:40d6211deb39950072e7ceca579ef53d6f367e50f8126ae0c7036ebf52334c67 | doc/reviews/workflow-governance/82-session-hook-points-to-the-index-code-review.md |
| integration3 | record | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:1b83b83d9ae46498852a9407ed7e4b90610289fcda28cc540f1abb9573fbc77a | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| release | runbook | open | git:d7623817149f5625b5998d5f3df00a1fc20f5b2e | sha256:fa666771742b6c84c3c7ca63013f190971d4a128b52a04451ec7e8041f163a6f | doc/runbooks/release.md |

## Gate script pins

`index_pins.py` pins only `.md` and `.json` leaves, so the gate scripts are pinned here by the same rule: the commit that last changed the file, and the sha256 of its bytes at that commit. To check one, run `git log -1 --format=%H -- <path>` and `git show <commit>:<path> | sha256sum`.

| script | revision | sha256 |
| --- | --- | --- |
| skills/johnny-project-takeover/scripts/dispatch_lint.py | 78810fa6ca29fe6463efadc530547c52d93b4916 | f600bb7e0c51b91e0d52423d39d2976ed94b96fb1456b8e71d962426e135ec1a |
| skills/johnny-project-takeover/scripts/evidence_gate.py | 9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | 50318e437ad5d1050ffff60ba92a1e0c8e39a2ce39f2baa4a08c33961fd7503a |
| skills/johnny-project-takeover/scripts/usage_report.py | 9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | 85d7fe4e633699c6bb742d7d5b93cb48fd528aa183798b69b7fbbb661a287bd0 |
| skills/johnny-project-takeover/scripts/rework_report.py | 06667834c7098ba3702cc7da8740ff5336a9ea1d | ef79b719f94958e94a04b76e1d0b145c704b2c88ea37865061695513ea477179 |
| skills/johnny-project-takeover/scripts/integrate.py | 64010e6e88bc6af176f113e86fea615b36ed0b05 | 125573d541c812597c0249d823b8b841f48b67fd283b610f655402a8c288f199 |

## 2026-11-25 stage summary (pointers only)

**Branch tip:** `cp/wave3` at `fbff6742`, pushed. Nothing is left unpushed. The work is paused at the owner's request ("等等。先暫停。做個階段總結"). No seat is running. The rule-only review of ticket 71 revision03 was stopped mid-way and is to be rerun.

**Wave 3 (需求 1, REQ-043, issue #3):**
- INTEGRATED: 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76.
- Ready to dispatch: 79, at revision03, rule-only review done (row `t79`).
- In revision: 71, revision03 (row `t71`; its revision02 review is row `t71review`).
- Not yet written: 77 (acceptance) and 78 (Level 2 code and `.codex-plugin` retirement).
- First rework report over 11 tickets: 21 rounds; CONTROL_PLANE_RULE 5, RETURN_UNTRUE 2, DESIGN_UNFORESEEN 2, IMPLEMENTATION_DETAIL 8.

**Other requirements:**
- Wave 4: 需求 2, REQ-044, issue #16; seven themes T1 to T7, owner-approved.
- 1.0 enterprise: 需求 3, REQ-045, issue #17; owner-approved. The plugin is paired with a service that the enterprise deploys itself; the beta runs on the tester's own computer; the 1.0 adapter is Docker Compose; a SaaS comes later.

**Decisions since 2026-11-19.** All are quoted verbatim in REQ-043. Read its rows dated 2026-11-19 and 2026-11-20 rather than any summary.

**Resume order:**
1. Rerun the rule-only review of ticket 71 revision03.
2. Dispatch 79, review it and integrate it.
3. Dispatch 71, build the local candidate, and let the owner test with the local marketplace.
4. Write and run 77.
5. Release in REQ-043's order, with the owner's confirmation at each push. The owner renames the publication repository to `software-factory-plugin` first.

**Practice:**
- Name the model and effort on every seat.
- Lint each dispatch with `--ticket`.
- Run every exit-0 cell at the base first.
- Name the registered base failures by test id.
- Merge local commits, do not rebase them.
- Batch the record pushes.
- Quote owner decisions verbatim, with the question.

The scratchpad tools are listed in `control-plane-resume-2026-11-20.md`, in the shared side-session notes folder outside the repository.

## 2026-11-26 stage summary, end of day (pointers only)

This section replaces the earlier 2026-11-26 summary below, which is kept for history. Every decision is quoted verbatim in REQ-043 (rows dated 2026-11-26), REQ-044 (Owner decisions, T8 to T17) and REQ-045 (owner decision 2026-11-26). Read them, not this summary.

**Done today:**
- Tickets 79, 71, 80, 81 and 77 were integrated, each with CI green on both jobs (row `integration3`).
- The final local lifecycle passed all ten verdicts at `e87bc5cb` with `6d04fa6d` (row `t77record`).
- The owner's local tests are in row `t77record`. The written read-only rule was not followed in use. With ticket 82's SessionStart hook, both lookups went through the 流程索引 with no search. The hook runs in the Claude desktop app and in Codex; Codex asks to trust it. The old-plugin guard fires from the hook on a plain question.
- REQ-044 grew from T1–T7 to T1–T17. The order is A (T13–T15) first, then B and C (T12, T16), then the rest. The non-engineer themes are due by 1.0. Generic lessons are in its carried list.
- Issues #3, #16 and #17 were rewritten or updated.

**In flight at this summary:**
- Ticket 82 revision06 correction. Its seat runs dispatch `JAS-82-3` (sha256 `d0eea2ec…`) on `cp/wave3-82-hook`, from `b629db41`. It adds README section 4's trust paragraph and section 5's scope paragraph, rebuilds the publication commit from OLD `9cda3f9e`, and rebuilds the local marketplace. Revision04 was APPROVED at `b629db41` (row `t82review`).
- The shared local ref `refs/heads/publication-0.5.0` names the newest rebuild. Check it with `git rev-parse`.

**Resume order** (every push waits for the owner's confirmation):
1. When the 82 seat returns:
   - append USAGE and rerun E1;
   - send the correction review of revision06 to the same reviewer (it reviewed revision02 and revision04);
   - record the review, integrate with `integ_one.sh`, read CI back, and write the integration record.
2. Rerun ticket 77's lifecycle at the integration commit, with the new publication id, and record it.
3. The owner refreshes both hosts. The cache check is the README line `上面的 uninstall 指令針對裝在 user 範圍的舊版`. The owner retests once: the P0 lookup, the PRD lookup and the two-versions plain question.
4. Repin the `agents` row and run `index_pins --check`.
5. Fast-forward the development `main` (decision "B"). Trigger the one cloud run: `gh workflow run acceptance.yml --ref main -f candidate=<main> -f expected_publication=<newest id>`.
6. The owner renames the publication repository to `software-factory-plugin`. A reviewer reported "Repository not found" for the old name, so check its current name first.
7. Release per `doc/runbooks/release.md`. Show each push command with `--dry-run` before running it.
8. Smoke install from the public path, then remove the eight registered rows.
9. Ticket 78, then wave 4 in REQ-044's order.

**Practice kept today:**
- Every ticket gets a rule-only review before dispatch, and a delta review for each new revision.
- Correction dispatches tell the seat to copy the previous receipt first (S82-01).
- Each report states what runs, how long it usually takes, and whether the owner must act.

## 2026-11-26 stage summary (pointers only)

**Branch tip:** `cp/wave3`, pushed. All 0.5.0 code tickets are INTEGRATED: 65 to 76, 79, 71, 80, 81, 77. Ticket 78 waits until after the release.

**Publication commit:** `6d04fa6d0cf0c1e7134a312894adc219f44bf4a9`. It is named by the local ref `refs/heads/publication-0.5.0` and was never pushed. The final local lifecycle at `e87bc5cb` passed all ten verdicts (row `t77record`).

**Owner decisions of 2026-11-26.** All are in REQ-043 (rows dated 2026-11-26) and REQ-044 (T8 to T15). Read them, not a summary.

**Resume order** (each push waits for the owner's confirmation):
1. The owner retests the final candidate on the desktop: the P0 lookup, the PRD lookup, and two versions installed together. Record the result in `t77record`.
2. Fast-forward the development `main` to `cp/wave3` (decision "B").
3. Trigger the one cloud run: `gh workflow run acceptance.yml --ref main -f candidate=<main> -f expected_publication=6d04fa6d…`.
4. The owner renames the publication repository to `software-factory-plugin`.
5. Release per `doc/runbooks/release.md` and ticket 71's release order, with `6d04fa6d`.
6. Smoke install.
7. Remove the eight registered rows.
8. Tickets 78 and wave 4: T13 to T15 come first.
