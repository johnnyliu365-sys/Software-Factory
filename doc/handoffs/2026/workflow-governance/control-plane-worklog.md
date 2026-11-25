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
| agents | governance | open | git:867ddb53021b79f97afc1ccce3b10d6c6db03555 | sha256:2b53eab4ecf32d07652237d476f25accd51ba260a1d3f265731e326e737ca29d | AGENTS.md |
| workflow | governance | open | git:c2bccb7c0c8de9719cb48c40e49169bc9a2b777b | sha256:e090c065a26c4131aedf737a0161ce2cd62500bcc33a41b15d706acc8a8dba6e | Workflow.md |
| codereview | governance | open | git:9ae502de5dbbf7e36b39179bcfbbc0a1d380519e | sha256:7665a6e41aba778fb873435841197bd2db2b2fb3a4e062bb78af088d6114dff9 | CodeReview.md |
| req043 | requirement | open | git:fbff6742a1ad9e256feb5379f343d8d834dab528 | sha256:609913664d53c7e15c975ced75c82d27d5c639ff2eb252fcc7acf0077ed4bf70 | doc/requirements/active/2026/workflow-governance/REQ-20261103-043.md |
| req044 | requirement | open | git:885cf217a15f424eb388f63f10a175839f6dc13b | sha256:5f42ba408036fe9dcc57e3ee672a81d09e24e69155afcb2399918aa79d447c72 | doc/requirements/active/2026/workflow-governance/REQ-20261120-044.md |
| req045 | requirement | open | git:f537c71b15a9182f205a1028f1f04acb0573edec | sha256:267ea89eead7c39721c1f289417aa35d413cf4f8b1b4fe6f73f438b6e0fdb21c | doc/requirements/active/2026/workflow-governance/REQ-20261120-045.md |
| tickets | index | open | git:fbff6742a1ad9e256feb5379f343d8d834dab528 | sha256:06c8183e173fade784717af0b89ea1490aeda72c5ec02c823d86cf803148724f | modules/tickets/workflow-governance/README.md |
| t71 | ticket | open | git:fbff6742a1ad9e256feb5379f343d8d834dab528 | sha256:5eb7a73a20b8e2ab15e1893097180b79e3efa0bc587fe9dce2076681efb72eec | modules/tickets/workflow-governance/71-publication-0-5.md |
| t71review | review | open | git:fbff6742a1ad9e256feb5379f343d8d834dab528 | sha256:98cb331d5a0d0bb7fc28c49fb7ab67dcd33fc2b7b5274865e86d662d573dc331 | doc/reviews/workflow-governance/71-publication-0-5-ticket-review.md |
| t79 | ticket | open | git:08c5819ef9fc59ab43c3bd024e358bff492cade5 | sha256:9db9648be058adf238c19f30760334a426fdc5128740b106e99ee78b85441e76 | modules/tickets/workflow-governance/79-read-only-lookup-goes-to-the-leaf.md |
| integration | record | open | git:885cf217a15f424eb388f63f10a175839f6dc13b | sha256:eef317a881e20b0c53758907e244bae0708182cd41c3bc8a630349601373bd19 | doc/reviews/workflow-governance/wave3-integration-2026-11-18.md |
| expectation | state | open | git:9ed4ae715cbba28bc3a7d138b389ff99b1c510d3 | sha256:65f3ba13d08cddeae628f5b85bd57618f93f3ff7730af673df7c3421208318d5 | doc/handoffs/2026/workflow-governance/usage-expectation.json |

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
