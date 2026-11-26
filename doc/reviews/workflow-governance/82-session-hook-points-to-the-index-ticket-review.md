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

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 70 | 161657 | 3653406 | 34696 |
