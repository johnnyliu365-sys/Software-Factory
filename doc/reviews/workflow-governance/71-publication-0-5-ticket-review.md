# Ticket 71 — rule-only review before dispatch

Ticket: `modules/tickets/workflow-governance/71-publication-0-5.md`. Process tier: strict. A rule-only review is outside the `CodeReview.md` §5 count. If it returns `CHANGES_REQUESTED`, the ticket gets a new revision before dispatch.

## Revision02 (commit `b22a4db8`), independent `ticket-review` seat

**verdict: CHANGES_REQUESTED**

The seat treated tickets 73 and 76 as landed and modified nothing. It ran read-only git commands and one `git ls-remote origin`.

It confirmed:
- the boundary;
- the shipped text against `RETIRED_SURFACE` and the provider-literal ban;
- the base facts (pin `0b3afd36`, the four registered publication tests, the licences, the archived SPECs and superseded ADRs);
- the strict tier.

Revision03 also carries the owner decisions of 2026-11-20: the rename to Software Factory, the plugin id `software-factory`, the marketplace in the public publication repository on a branch `marketplace`, the publication repository renamed by the owner to `software-factory-plugin`, the full README rewrite, and testing from a local marketplace.

| id | severity | finding | revision03 |
| --- | --- | --- | --- |
| S71R-01 | High | The package check required the marketplace pin to name the publication commit, but the generator writes forty zeros into the package's copy | Split: the development `marketplace.json` pins the commit; the package's copy holds zeros |
| S71R-02 | Medium | "No Level 2 file" was undefined | The set is enumerated (four root files and `library/local_orchestration/`); the `payload` declaration is unchanged |
| S71R-03 | Medium | The README lines to keep and drop were unstated, and the exact route tuple and injection anchor of the publication tests were not addressed | The README is rewritten section by section with the exact commands; the route tuple and the anchor become the one new `marketplace add` line |
| S71R-04 | Medium | Removing the README's install step leaves the `johnny-install.cmd` closure entry unmatched; new inline path tokens would break the closure tests | The entry is dropped; paths appear only in fenced blocks or plain text |
| S71R-05 | Medium | The target of the `v0.5.0` tag was not unique, integration was missing from the order, and the push was only implied | The release order names the integration, the fast-forward of `main`, and `v0.5.0` on it, each push with the owner's confirmation |
| S71R-06 | Medium | `--verify-only` in a fresh clone needs a local `refs/heads/` anchor | The readback steps are stated: check out `v0.5.0`, create the branch from `origin/publication-0.5.0`, then verify |
| S71R-07 | Medium | CI evidence needs the seat's branch pushed | The seat pushes only its own development branch |
| S71R-08 | Low | Moving the publication `main` is not a fast-forward | It is the owner's, by force-with-lease from `0b3afd36`; installs use tags and the `marketplace` branch |
| S71R-09 | Low | There are eight registered rows, not four, and CI goes red with `REGISTERED_NOW_PASSING` after the anchor push | Eight rows are named, the expected red is stated, and the reason text names the new pin |
| S71R-10 | Low | The uninstall text cited no source | `johnny-router.ps1` and `live_uninstall_composition.py` are cited |
| S71R-11 | Low | `test_t6` hard-codes `0.4.14` | It is named among the changed constants |
| S71R-12 | Low | The tier line was not the section's first line | It is now the first line |
| S71R-13 | Low (note) | Template rows are absent | No change, as with ticket 73 |
| S71R-14 | Low (note) | The Codex evidence holds only indirectly | Accepted; ticket 77 verifies it on a fresh `CODEX_HOME` |
| S71R-15 | Low (note) | A backticked `johnny-router.ps1` in `SKILL.md` would break the payload test | The new sentence has no path token in backticks |
| S71R-16 | Low (note) | Changelog form | Rows in the table, plus a `## 0.5.0` section |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision02 | claude-opus-5-5 | high | 108 | 186923 | 6831654 | 44106 |
