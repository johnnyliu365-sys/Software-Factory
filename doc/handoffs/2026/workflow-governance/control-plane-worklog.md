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
| agents | governance | open | git:46264b9a55ab50f26f5adb4a869fcfed43266ac3 | sha256:3681fc50dcd086c4a9cac517e8f239ba5f8205d534d1cbc1df98b29a395c647a | AGENTS.md |
| workflow | governance | open | git:c2bccb7c0c8de9719cb48c40e49169bc9a2b777b | sha256:e090c065a26c4131aedf737a0161ce2cd62500bcc33a41b15d706acc8a8dba6e | Workflow.md |
| codereview | governance | open | git:9ae502de5dbbf7e36b39179bcfbbc0a1d380519e | sha256:7665a6e41aba778fb873435841197bd2db2b2fb3a4e062bb78af088d6114dff9 | CodeReview.md |
| req043 | requirement | open | git:e05ca257ffe6813be8d9f8243fe0d840acd03f4d | sha256:978bdb0023887e9cd8c44c493498e04f20e6ab107d65962015d6a593b004b426 | doc/requirements/active/2026/workflow-governance/REQ-20261103-043.md |
| req044 | requirement | open | git:bfc0259045bfc0116aab4e3268d553e531dee531 | sha256:c003ae435fc8bf051c55c04bc6885bed91328b6206ed1651d03c71c1f0bc7209 | doc/requirements/active/2026/workflow-governance/REQ-20261120-044.md |
| req045 | requirement | open | git:96792d116d414ca618f471d38bf036438cd37622 | sha256:e46179a193a89de0e4e198b275afbcdaedc0acbebdb4a0713ca6cded383505f3 | doc/requirements/active/2026/workflow-governance/REQ-20261120-045.md |
| tickets | index | open | git:c08ccc84df233d19fda9ef276d83c429894e02bf | sha256:d4363117e901e417bcff518a30a0f089c3f384f2e313e6a15393fca99a1e6738 | modules/tickets/workflow-governance/README.md |
| t71 | ticket | open | git:0cfb563b20667af140e21f9d61a8e272aa382466 | sha256:5113d014656bfe1ea805f7edde7a2740699094145abb3213a584bf5a5e77ca41 | modules/tickets/workflow-governance/71-publication-0-5.md |
| t71review | review | open | git:68795ea281ffdb8a6f7b4340bf9bfc9ef949d108 | sha256:9a86b7e900064523ba14dc700d4458bf2ef9337b32df71c594d8b1f7b3761fe5 | doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md |
| t79 | ticket | open | git:efa03a7edd6a1a8a9077959228307fc70ac68fa0 | sha256:06b34754e6f2bd2254d6da8729c94321970b484464754bf2a82344753e47f7e5 | modules/tickets/workflow-governance/79-read-only-lookup-goes-to-the-leaf.md |
| integration | record | open | git:c08ccc84df233d19fda9ef276d83c429894e02bf | sha256:9909f73d5f8af21b4d98918367656762832c2d9a54841174890f6e107b8feab3 | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| expectation | state | open | git:9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | sha256:65f3ba13d08cddeae628f5b85bd57618f93f3ff7730af673df7c3421208318d5 | doc/handoffs/2026/workflow-governance/usage-expectation.json |
| t77 | ticket | open | git:62ebc5fbc40ce644d368fc35bcd898a38f1023b2 | sha256:ee21c2436e93727b887469845968955e3af21766d357a3ca4f6736f6fb74c17c | modules/tickets/workflow-governance/77-acceptance-0-5-0.md |
| t77record | record | open | git:bc8da7bdc79adef480112300e9738d3714ba4817 | sha256:3770894f7658ec576c14251994580c27200f106a30c9a8ee7d853a07a5d8fa6a | doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md |
| t80 | ticket | open | git:2a34bce4d267c8655f23e440f0486297ffbb1beb | sha256:fa2668353870a941eb69862250a5acdbaf934a4a2c945510d9fa8dbbc1c86e3b | modules/tickets/workflow-governance/80-lookup-through-the-index.md |
| t81 | ticket | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:a372e81107b6e95cca035c50cb0861d3f835652ae1b4aa925dc60bd620d2f01a | modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md |
| t82 | ticket | open | git:c08ccc84df233d19fda9ef276d83c429894e02bf | sha256:7478f1f4c5558c206c58e6c8faa8d9121f59297af9b99878102db82944c5f77c | modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md |
| t82ticketreview | review | open | git:b4c4b6b3974aa16f3e2b50d9c0483d7d9cfd9be1 | sha256:1d433de913abc0ebf90089421a9cf0ef0fa776ebed7ce81f0aaf74af5a643e29 | doc/reviews/workflow-governance/82-session-hook-points-to-the-index-ticket-review.md |
| t82review | review | open | git:8f49e10cd6d7895e84191afa9f047a14d5c94474 | sha256:090dc5eb92914c77d431eaca81aaaf7281a7985ba109191b78ee3c95e8cf52e2 | doc/reviews/workflow-governance/82-session-hook-points-to-the-index-code-review.md |
| integration3 | record | open | git:c08ccc84df233d19fda9ef276d83c429894e02bf | sha256:9909f73d5f8af21b4d98918367656762832c2d9a54841174890f6e107b8feab3 | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| release | runbook | open | git:d7623817149f5625b5998d5f3df00a1fc20f5b2e | sha256:fa666771742b6c84c3c7ca63013f190971d4a128b52a04451ec7e8041f163a6f | doc/runbooks/release.md |
| installguide | runbook | open | git:0a5d01f2c374f6a3f34b1ea1b1e1760dcd507493 | sha256:5b0daeeeee86e80552602a26d95c264a196cb9395aafa7d2636e4ce476ee1f1a | doc/runbooks/install-guide-0.5.0.md |

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

## 2026-11-26 stage summary, late evening (pointers only)

This section replaces the "end of day" summary below, which is kept for history. Every decision is quoted verbatim in REQ-043 (rows dated 2026-11-26) and REQ-044 (Owner decisions; themes T1 to T21). Read them, not this summary.

**Done since the end-of-day summary:**
- Ticket 82 revision06 was integrated at `f0ba4995`, then reopened by owner decision "A" as revision07 and revision08 (the Codex desktop app does not ask to trust a changed hook). Revision08 was integrated at `9f764a88`, merged forward at `3e54da2c`, CI green on both jobs (row `integration3`).
- The publication commit is `e08e82d3373547a5448040638fb22b1810dc9cf3`, named by the local ref `refs/heads/publication-0.5.0`; not pushed. The lifecycle passed all ten verdicts at `3e54da2c` with it, and the owner retested both hosts (row `t77record`).
- `doc/runbooks/install-guide-0.5.0.md` is drafted for an installer other than the owner (row `installguide`); its publication commit line is filled in after the release.
- REQ-044 grew to T21: T18 (five measurements that decide how far the harness is kept), T19 (context per call; resume or fresh by a water mark), T20 (a ticket is an executable spec bundle; first ticket of wave 4), T21 (translation fidelity; a read-back before dispatch). T4, T8 and T17 gained the protection rules. Issue #16 follows it.
- The owner's user-level settings gained two hooks for the memory index cap (memory `user-sessionstart-hook`).

**Resume order** (every push waits for the owner's confirmation):
1. Done: the owner fast-forwarded the development `main` to `f1d04039` on 2026-11-26T15:32:55Z; CI run 45850194264 is green on both jobs. `cp/wave3` is ahead of `main` again by record commits.
2. Cloud run 1 (45920193720, 2026-11-27) is FAIL at `build`: `acceptance.yml` installs no Python package and the generator needs `pydantic`. Reproduced locally with a clean venv (row `t77record`, section "The cloud run"). Waiting for the owner's decision on the fix and on a second run. After the fix: fast-forward `main` again, then `gh workflow run acceptance.yml --ref main -f candidate=<main> -f expected_publication=e08e82d3373547a5448040638fb22b1810dc9cf3`, each on the owner's confirmation in words.
3. The owner renames the publication repository to `software-factory-plugin`. Check its current name first.
4. Release per `doc/runbooks/release.md`. Show each push command with `--dry-run` before running it.
5. Smoke install from the public path by `doc/runbooks/install-guide-0.5.0.md`, fill in its publication commit, then remove the eight registered rows.
6. Give the owner the guide's link for the outside install (T18 measurement (3)).
7. Ticket 78, then wave 4: T20 first, in REQ-044's order.

**Practice kept:**
- Resume or fresh by the water mark of REQ-044 T19 lever (1): after one full round a seat's next round starts fresh unless it is a small fix.
- Model by difficulty until T18 measurement (4) decides.
- A correction dispatch tells the seat to copy the previous receipt first, and the control plane renames the old `RETURN.as-returned.md` before appending USAGE.


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
