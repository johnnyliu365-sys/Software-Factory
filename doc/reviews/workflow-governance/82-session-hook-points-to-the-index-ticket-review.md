# Ticket 82 — rule-only review before dispatch

Ticket: `modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md`. Process tier: strict. A rule-only review is outside the `CodeReview.md` §5 count. Under the strict tier, the next revision applies the reviewer's exact fixes, and there is no third round (L-19).

## Revision01 (commit `26b272e2`), independent `ticket-review` seat

**verdict: CHANGES_REQUESTED**

The seat changed nothing. It fetched the Claude Code hooks and plugins reference pages, and confirmed the ticket's doc facts. One correction: under PowerShell, the substituted path keeps native backslashes.

It ran the hook command locally, in Git Bash and in Windows PowerShell 5.1. It used a temp path, a path with a space, a backslash path, and a path with an apostrophe. Both shells printed the same text and exited 0. They differ only in the line end: LF in Git Bash, CRLF in PowerShell. A bare `bash` started from Python resolves to the WSL launcher, which fails rather than skips.

| id | severity | finding | revision02 |
| --- | --- | --- | --- |
| S82R-01 | blocking | The hook sent every read-only question to the 流程索引, while `AGENTS.md` sends only plugin-rule lookups there, and the text restated part of the rule | The reviewer's exact command text and README sentence; the test checks both anchors |
| S82R-02 | blocking | The ticket narrowed option A (a 2 to 3 KB injection, Codex first) without a record | The owner answered "接受 (Recommended)"; the "Scope against the decision" paragraph and a REQ-043 row record it |
| S82R-03 | major | Which bash runs, the line ends and stderr were undefined | Exact interpreter selection, skips, CRLF normalisation and the stderr rule |
| S82R-04 | major | "The extracted publication tree" did not say which tree | `materialise_publication_tree` into a temporary directory; K1 checks the pinned commit |
| S82R-05 | minor | The payload entry's form and place were undecidable | One line in `payload.files`, after `Workflow.md`; `trees` unchanged |
| S82R-06 | minor | Test changes did not name their constants | `ANCHORED_HEADINGS` and `test_the_session_hook_is_carried` named exactly |
| S82R-07 | minor | No test read the README sentence | A README check is added to the new test file |
| S82R-08 | minor | Forward slashes hold only under Git Bash | The fact is corrected; quoting is stated |
| S82R-09 | minor | It was not said whether the release waits when Codex does not run the hook | The release waits for a README ticket unless the owner decides otherwise |
| S82R-10 | minor | No correction-round clause for OLD | Added, as in tickets 80 and 81 |
| S82R-11 | low | The work log's `agents` pin will drift | Control-plane item 4: repin and check |

## Revision03 delta (commit `6eae7d41`), same seat, resumed

**verdict: CHANGES_REQUESTED**

The delta adds the old-plugin guard to the hook text (owner decision "放進 hook") and names the terminal for /hooks.

The seat checked three things:
- **The guard's conditions.** They match `SKILL.md` step 1.
- **Conflicts and false firing.** There is no conflict and no false firing: a marketplace that is registered with no plugin installed lists no skills.
- **The new command in both shells.** It ran with four path forms, and both `${CLAUDE_PLUGIN_ROOT}` places were substituted.

| id | severity | finding | revision04 |
| --- | --- | --- | --- |
| S82R-12 | major | The cache check could not tell a stale `838bb354` cache from the refreshed one | The check looks for the guard sentence's text in `hooks\hooks.json` |
| S82R-13 | minor | "Directly below the ticket 81 row" could add a second row | Replaced in place; the paragraph names what is replaced |
| S82R-14 | minor | The seat's worktree holds revision02 of the ticket | The seat reads revision04 by `git show` from the named commit |
| S82R-15 | minor | The owner-test list still expected /hooks in the desktop app, and did not require a plain question | Both reworded |
| S82R-16 | minor | Two copies of the guard with no test tying them | A cross-check test on the two match conditions |
| S82R-17 | low | The size figure is out of date | 777 printed characters stated |
| S82R-18 | low | The changelog row cited only "A" | It cites "A" and "放進 hook" |

## Revision05 delta (commit `22ddb00c`), same seat, resumed

**verdict: CHANGES_REQUESTED**

Revision05 adds two README paragraphs:
- 4b, the Codex trust sentence (owner finding "有");
- 4c, the install-scope sentence (owner decision "併進票 82").

The seat confirmed that both insertion points are exact and unique, and that every old README route check still passes. It also confirmed 4c's scopes with `claude plugin uninstall --help` on 2.1.332.

| id | severity | finding | revision06 |
| --- | --- | --- | --- |
| S82R-19 | major | The cache-check marker is already in the `9cda3f9e` build | The check looks for the new scope paragraph in the cached `README.md` |
| S82R-20 | minor | "M1" is not defined in the ticket | The cases join TDD 2 |
| S82R-21 | minor | "Exactly once at that place" was undefined | Exact neighbouring lines and a character check |
| S82R-22 | minor | 4b claimed more than the evidence shows | The reviewer's wording: after install or update, "if it asks"; the guard is also lost without trust |
| S82R-23 | low | 4c did not say which commands to run in the folder | The reviewer's wording |
| S82R-24 | minor | The owner-test bullet still treated Codex hook support as open | Reworded on the recorded evidence |
| S82R-25 | low | The changelog citation was incomplete, and the "gains" wording could duplicate the row | Cites "併進票 82"; "not added again" |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 70 | 161657 | 3653406 | 34696 |
