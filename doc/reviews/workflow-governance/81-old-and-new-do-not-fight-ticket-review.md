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

## Revision03 item 7 (commit `12dc603c`), same seat, resumed

**verdict: CHANGES_REQUESTED**

The owner decided "併進票 81 修" after the ticket 80 review found S80-01 and S80-02. Revision03 added item 7. This review covers only that item.

The seat walked four questions by hand through the lookup rule. "P0 原始碼型別", "啟動順序" and "唯讀查詢查不到時怎麼回答" each reach one leaf. "target project 的 PRD 放哪？" still fits two rows, the target-sources row and the PRD/CHG row. No test outside the boundary pins the old first row.

| id | severity | finding | revision04 |
| --- | --- | --- | --- |
| S81R-14 | Medium | S80-01 stays open for the target-sources question, and item 7 left out the tie-break the owner's option included | The tie-break clause 「其餘同時符合多列時，取表中較上面的一列」 is added to the lookup sentence; the scope line and a TDD case go with it |
| S81R-15 | Medium | The one-row-per-anchor check, as worded, turns today's table red, and does not catch S80-02 | Only links whose target begins with `#` are counted. `INDEX_TABLE` pins the whole table in order. The CM5 duplicate and a row swap become cases |
| S81R-16 | Low | `modify = AGENTS.md` admits the whole file | Evidence A1: exactly two changed lines. 責任邊界 and 禁止修改 reworded |
| S81R-17 | Low | Four smaller gaps: the 狀態 revision, the file count, the changelog row, the TDD list | All four applied |
| S81R-18 | Low (note) | 「規則即本檔該節」 names a section larger than the rule | No change |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 80 | 158926 | 5597102 | 36456 |
| rule-only review, revision03 item 7 | claude-opus-5-5 | high | 20 | 192896 | 1744403 | 13037 |
