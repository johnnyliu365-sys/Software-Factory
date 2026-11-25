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

## Revision03 (commit `fbff6742`), same seat, resumed

**verdict: CHANGES_REQUESTED**

The seat treated ticket 79 revision03 as landed and modified nothing. Since `b22a4db8` nothing it pins has drifted. It closed S71R-01 to S71R-12, S71R-15 and S71R-16; S71R-13 and S71R-14 stay accepted notes. Three closures left a residual, each filed again as a new finding: S71R-03 (S71R-22), S71R-04 (S71R-23), S71R-07 and S71R-09 (S71R-26).

On the questions put to it:
- No test or file outside the boundary pins `johnny-ai-skill` for the shipped Claude manifest. Item 10's list is right but incomplete (S71R-25).
- Claude Code reading a raw marketplace URL on a non-default branch has a precedent: the 0.4.14 candidate route.
- Codex `--ref` with a same-repository `url`+`sha` source can only be shown by running the CLI, so it is a ticket-77 item.
- The new `marketplace add` line passes the route check if it starts at column 0.
- No force push is needed except the owner's own move of publication `main`.

Revision04 applies the reviewer's exact fixes. Under the strict tier there is no third rule-only round (L-19).

| id | severity | finding | revision04 |
| --- | --- | --- | --- |
| S71R-17 | Medium | `test_l1` pins `_PUBLICATION_URL` to the old repository, and `_RAW_PUBLICATION_MAIN_MARKETPLACE_URL` names it too | Item 5 names both constants and their new values |
| S71R-18 | Medium | `test_references_qualify_receipt_bridge_by_lifetime` pins two README sentences about the retired bridge | The README drops them; item 5 removes the test's two README assertions and keeps its router and authority assertions |
| S71R-19 | Medium | The public install path cannot be checked before release, and step 8 has no failure branch | Item 8 makes Codex `--ref` with a same-repository `url`+`sha` source a ticket-77 item; step 8, on failure, holds any announcement, stops before step 9 and reports; deleting the `marketplace` branch is the owner's |
| S71R-20 | Medium | No source supports the `.agents/plugins/marketplace.json` copy on the public branch, and its schema differs | Dropped from step 4. Which local file Codex reads, and its schema, is a ticket-77 item |
| S71R-21 | Low (note) | `--plugin-dir` never reads the local marketplace file; the target directory is not required to be empty | The directory must be absent or empty; the Claude marketplace flow is a ticket-77 item |
| S71R-22 | Low | "Exactly these three commands" conflicts with keeping `update` and `uninstall` | Five commands, listed, each at column 0 |
| S71R-23 | Low | The closure scan also reads markdown link targets | Link targets are payload paths only; section (10) keeps the links to `LICENSE` and `NOTICE` |
| S71R-24 | Low | Keywords and the two `marketplace.json` descriptions were unspecified | Exact `description` and `keywords` for `plugin.json`; exact marketplace description; the plugin entry copies `plugin.json` |
| S71R-25 | Low (note) | Shipped prose still names Johnny | Item 10: it stays until wave 4 |
| S71R-26 | Low | Three revision02 leftovers: 責任邊界, defect class 3, "four publication rows" | All three aligned |
| S71R-27 | Low | "Its target is teams" had no source; the roadmap cited only REQ-043 | "From 1.0 its target is enterprises", citing REQ-045, which is added to the decisions line |
| S71R-28 | Low (note) | Step 4 did not say what the `marketplace` commit is | One parentless commit whose tree is only `.claude-plugin/marketplace.json` |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision02 | claude-opus-5-5 | high | 108 | 186923 | 6831654 | 44106 |
| rule-only review, revision03 (stopped run and resumed run) | claude-opus-5-5 | high | 38 | 443345 | 3419101 | 23596 |
