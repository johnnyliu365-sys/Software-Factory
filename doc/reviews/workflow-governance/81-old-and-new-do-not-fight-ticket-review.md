# Ticket 81 — rule-only review before dispatch

Ticket: `modules/tickets/workflow-governance/81-old-and-new-do-not-fight.md`. Process tier: strict. A rule-only review is outside the `CodeReview.md` §5 count. Under the strict tier, the next revision applies the reviewer's exact fixes, and there is no third round (L-19).

## Revision01 (commit `66367c29`), independent `ticket-review` seat

**verdict: CHANGES_REQUESTED**

The seat modified nothing, moved no ref, and ran neither `claude` nor `codex`. It ran `git show` and `git grep`, listed the two hosts' plugin cache folders, and ran mypy with its cache in the scratchpad.

It confirmed four things:
- **Guard position and text.** The guard stands before the read-only step without conflict. Its text passes the provider, retired-surface, D7 and closure checks.
- **The README paragraphs.** They pass the route and closure checks.
- **Boundary.** The boundary holds: `doc/runbooks/` is outside the payload, and no outside test pins section 5 or the start steps.
- **Tier.** Strict is the right tier.

| id | severity | finding | revision02 |
| --- | --- | --- | --- |
| S81R-01 | High | The guard could not be decided in Codex, where skills are listed by name and file. It let work go on in a session whose skills had not been reloaded. It said nothing for a host that lists no skills | The reviewer's exact step: the name prefix or the folder name; a new session after removal; nothing else in this session; go on when no skills are listed |
| S81R-02 | Medium | README paragraph 1 promised more than the guard can do, because the old skill may be the one loaded | The reviewer's exact paragraph and changelog bullet |
| S81R-03 | Medium | README paragraph 2 generalized one observation on 2.1.332, and its subject was unclear | Names 2.1.332 and Software Factory; "wrote" in the risk list |
| S81R-04 | Medium | Two ticket 79 test cases break when the steps are renumbered | Both edits and the defect message named exactly |
| S81R-05 | Medium | OLD, the correction round and the rollback were not pinned down; "name the new id" was unclear | OLD from the baseline pin; rollback to ticket 80's commit; the eight occurrences of OLD replaced |
| S81R-06 | Medium | The release rule named no check, and it competed with ADR-018 | The `git ls-remote --tags` check, semantic-version order, HALT, and a citation of ADR-018 |
| S81R-07 | Low | The order's citation was ambiguous | Names ticket 71's release paragraph, copies no step, and substitutes the released ticket's commit |
| S81R-08 | Low | The cached-`SKILL.md` check gave neither the files nor the line | Both cache paths and the exact line prefix |
| S81R-09 | Low | The two-versions test could pass or fail by chance | The owner uses the plugin-qualified name; the record says which skill loaded |
| S81R-10 | Low | Ticket 77's cloud trigger was not repointed | Added to control-plane item 1 |
| S81R-11 | Low (note) | Copied 0.4.x rules belong to wave 4 T2 | Stated in the risk list |
| S81R-12 | Low (note) | The new runbook is swept by the D7 phrases | No change; the implementer keeps it free of them |
| S81R-13 | Low (note) | The README insertion points could be tighter | Applied: after the named line and the named fenced block, with one blank line on each side |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 80 | 158926 | 5597102 | 36456 |
