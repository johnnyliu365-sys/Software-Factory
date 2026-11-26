# Ticket 80 — rule-only review before dispatch

Ticket: `modules/tickets/workflow-governance/80-lookup-through-the-index.md`. Process tier: strict. A rule-only review is outside the `CodeReview.md` §5 count. Under the strict tier, the next revision applies the reviewer's exact fixes, and there is no third round (L-19).

## Revision01 (commit `187f83cf`), independent `ticket-review` seat

**verdict: CHANGES_REQUESTED**

The seat modified nothing, moved no ref, and ran neither `claude` nor `codex`. It read the two hosts' plugin install records and cache folders, read-only.

It confirmed four things:
- **Boundary:** no test names `d355b4a2`. `check_registered_failures.py` matches by test id. The D7 patterns do not match the new texts. The payload closure scan drops anchor-only links.
- **Ordering with ticket 77:** the boundaries are disjoint. 77's `build` step regenerates in its own clone.
- **The Router 返回規則 row:** it is already reachable through `router-control.md`.
- **Tier:** strict is the right tier.

S80R-04 added two rows beyond the owner's option A. The control plane put it to the owner, who answered "一起補 (Recommended)". The answer is recorded in `REQ-20261103-043`.

| id | severity | finding | revision02 |
| --- | --- | --- | --- |
| S80R-01 | High | The generator moves the ref it is given with no old value, so the old-value guard never applied | The generator gets `refs/heads/publication-0.5.0-t80`. OLD is checked first. `update-ref` with OLD, then the temporary ref is deleted |
| S80R-02 | High | 「照下方「找不到」處理」 pointed to the HALT paragraph, not to the lookup's own not-found sentence | The exact sentence the reviewer gave, which refers to this paragraph's 「找不到該類索引」 sentence. Two new pinned constants |
| S80R-03 | Medium | A P0 row has three links, rows overlap, and column 2 links into `Workflow.md` | The same sentence: P0 rows win ties; column 2 is the leaf when it links into this file, column 3 otherwise; the rule applies when the user names no file |
| S80R-04 | Medium | 啟動順序 and Target project 正式來源 have no row | Owner decision "一起補": two more anchors and two more rows |
| S80R-05 | Medium | The link check could not be decided on the test's temporary copy | `copy_texts` copies the four reference files; anchors must match exactly one line |
| S80R-06 | Medium | The shared local ref turns host runs red in other checkouts until integration | The STATEMENT gives the time of the move; the restore command is given if the ticket is closed without integration |
| S80R-07 | Medium | Taken literally, the release order would push ticket 71's pin | The SOP names this ticket's commit for steps 3, 4 and 5 |
| S80R-08 | Medium | Both hosts cache by version, so a reinstall may reuse the stale copy | HALT if the old tree cannot be removed; the owner checks both cache copies for the new row |
| S80R-09 | Low | "At the integration commit" is ambiguous; 77's trigger text names ticket 71's commit | The first commit holding both tickets; item 3 of the control-plane list |
| S80R-10 | Low | The changelog row and the 0.5.0 sentence had no exact text | Exact row and bullet |
| S80R-11 | Low | What the reason-text change replaces was unstated | Each of the eight occurrences of the old id becomes the new id |
| S80R-12 | Low (note) | Defect class 1 lists one boundary case | No change |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 76 | 170078 | 4383448 | 45545 |
