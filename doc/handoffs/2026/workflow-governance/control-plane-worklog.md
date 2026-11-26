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
| req043 | requirement | open | git:12dc603c05d78d47acd1f975489153880be0d780 | sha256:a8782b1c64641ca294b760021e3b8803603960c21df1be4e19fe8852d4264f98 | doc/requirements/active/2026/workflow-governance/REQ-20261103-043.md |
| req044 | requirement | open | git:f6decb647c578094ff241fac722050719c1bcfea | sha256:a19fbfc88a6b0cbd01d4d32e70686bd1bcdd9cdb232814b452cbe27c5959b454 | doc/requirements/active/2026/workflow-governance/REQ-20261120-044.md |
| req045 | requirement | open | git:f537c71b15a9182f205a1028f1f04acb0573edec | sha256:267ea89eead7c39721c1f289417aa35d413cf4f8b1b4fe6f73f438b6e0fdb21c | doc/requirements/active/2026/workflow-governance/REQ-20261120-045.md |
| tickets | index | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:d4ce456af9f9e1107c0542b0d33527f9d839eda8cd4c174dea4230ce98f4cb95 | modules/tickets/workflow-governance/README.md |
| t71 | ticket | open | git:0cfb563b20667af140e21f9d61a8e272aa382466 | sha256:5113d014656bfe1ea805f7edde7a2740699094145abb3213a584bf5a5e77ca41 | modules/tickets/workflow-governance/71-publication-0-5.md |
| t71review | review | open | git:68795ea281ffdb8a6f7b4340bf9bfc9ef949d108 | sha256:9a86b7e900064523ba14dc700d4458bf2ef9337b32df71c594d8b1f7b3761fe5 | doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md |
| t79 | ticket | open | git:efa03a7edd6a1a8a9077959228307fc70ac68fa0 | sha256:06b34754e6f2bd2254d6da8729c94321970b484464754bf2a82344753e47f7e5 | modules/tickets/workflow-governance/79-read-only-lookup-goes-to-the-leaf.md |
| integration | record | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:1b83b83d9ae46498852a9407ed7e4b90610289fcda28cc540f1abb9573fbc77a | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| expectation | state | open | git:9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | sha256:65f3ba13d08cddeae628f5b85bd57618f93f3ff7730af673df7c3421208318d5 | doc/handoffs/2026/workflow-governance/usage-expectation.json |
| t77 | ticket | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:359b639edb552ee489f37f10e54df570d0a649239d100cf6f99329da05c4df72 | modules/tickets/workflow-governance/77-acceptance-0-5-0.md |
| t77record | record | open | git:4b6c187f4147e6130cb8eea182a9d8a829ce5b19 | sha256:bccb55324ef85e5877ed4ecd9d75feaf36d7cb619d950fa071894135b9c9f6df | doc/reviews/workflow-governance/77-acceptance-0-5-0-record.md |
| t80 | ticket | open | git:2a34bce4d267c8655f23e440f0486297ffbb1beb | sha256:fa2668353870a941eb69862250a5acdbaf934a4a2c945510d9fa8dbbc1c86e3b | modules/tickets/workflow-governance/80-lookup-through-the-index.md |
| t81 | ticket | open | git:7bbc28f63541e461eacccb7057f1aac12bba0f1e | sha256:a372e81107b6e95cca035c50cb0861d3f835652ae1b4aa925dc60bd620d2f01a | modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md |
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
