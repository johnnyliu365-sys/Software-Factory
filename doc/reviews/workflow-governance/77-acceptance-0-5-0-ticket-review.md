# Ticket 77 — rule-only review before dispatch

Ticket: `modules/tickets/workflow-governance/77-acceptance-0-5-0.md`. Process tier: strict. A rule-only review is outside the `CodeReview.md` §5 count. Under the strict tier, the next revision applies the reviewer's exact fixes, and there is no third round (L-19).

## Revision01 (commit `690c08e8`), independent `ticket-review` seat

**verdict: CHANGES_REQUESTED**

The seat modified nothing and ran no `claude`, `codex` or workflow command. Its remote reads were `gh release view v0.4.9`, `gh api` for repositories, branches and contents, and `git ls-remote`.

It confirmed:
- **Boundary.** No test pins `ci/acceptance/` or `.github/workflows/acceptance.yml`. Neither `ci` nor `.github` is in the payload. The new paths are within the 120-character cap.
- **The 0.4.14 raw URL** at `01b810f0` pins `0b3afd36…`.
- **`--ref main`** matches decision "B".
- **The zeros pin** of the public publication repository's marketplace.
- **The `v0.4.9` assets** and their sha256 values.
- **The development repository is public.**
- **Strict** is the right tier.

S77R-01 needed an owner decision. The question as asked: "票 77 要測「移除舊版 Level 2」。但 0.4.9 的安裝程式會停下來等人手打 INSTALL 才繼續，而且它自己寫明：agent 代答不算同意。驗收時這個提示要怎麼處理？" The options:
- A, recommended: `lifecycle.py` answers on standard input, only for an install into an empty acceptance `JOHNNY_ROOT`, on this host and on the runner;
- B: the owner installs by hand, and `level2` leaves the runner.

The owner answered "A 你預先授權腳本代答 (Recommended)". It is recorded in `REQ-20261103-043`.

| id | severity | finding | revision02 |
| --- | --- | --- | --- |
| S77R-01 | High | The 0.4.9 installer waits for a person to type `INSTALL`, and says an agent's answer is not consent | Owner decision 2026-11-26 "A" recorded; the `level2` step answers on standard input under it |
| S77R-02 | Medium | `gh release download` needs a token on the runner | Download by URL with `urllib`, no token, sha256 of both assets required |
| S77R-03 | Medium | The installer refuses to run inside a Git work tree; the workflow names no run root | The run root is refused inside a work tree; commands run in the step directory; the workflow uses `$RUNNER_TEMP/acceptance` |
| S77R-04 | Medium | Comparing with README prose decides nothing | A file allow-list in `ci/acceptance/README.md` quoting README section (6) |
| S77R-05 | Medium | Residue judged by the reviewer is undecidable, and the check covered paths only | Path segments and `.json`/`.toml` lines, against a fixed, reviewed allow-list |
| S77R-06 | Medium | `recover` left the failing command and "half-installed" undefined | The exact sequence and the exact final list |
| S77R-07 | Medium | README (5) "install as above" points to the unpushed public branch | Install from the local marketplace; plugin list and marketplace list both checked |
| S77R-08 | Medium | The Codex 0.4.14 source pins forty zeros | Record the commit installed; `PASS` needs `0b3afd36…`; whether `sha` is honoured is recorded |
| S77R-09 | Medium | `codex-ref` had no `PASS` rule | Installed tree equals the pinned commit's tree; `NOT_SUPPORTED` defined for the `file://` refusal |
| S77R-10 | Medium | `codex-files` gave no schema result and no verdict | Three marketplaces, outcome recorded for each, verdict defined |
| S77R-11 | Medium | No step ran `claude plugin update` | Added to `fresh` |
| S77R-12 | Medium | The host-by-step matrix and condition (3) were undecidable | Pairings fixed; two local runs, the first must exit 0 |
| S77R-13 | Medium | The generator run in the seat's worktree would touch shared refs and the forbidden `.claude-plugin/` | A `--no-hardlinks` clone under the run root, the exact generator command, the marketplace under the run root |
| S77R-14 | Medium | Three variables do not isolate credentials, git config, the updater or caches | An allow-listed environment, a step home, an empty git config; the remaining host state is named in the receipt |
| S77R-15 | Medium | The seat could start an agent through a host CLI | Only `--version` and the `plugin` subcommands; no prompt, `exec`, session or login |
| S77R-16 | Medium | Actions not pinned; checkout would persist the token | SHA-pinned actions, `fetch-depth: 0`, `persist-credentials: false`; the test forbids the token names |
| S77R-17 | Low | The trigger command lacked its inputs | Both `-f` inputs named |
| S77R-18 | Medium | The new test also runs on Linux in `ci.yml` | Python fake CLIs through `sys.executable`; Windows-only cases skipped with a reason; no new registered row |
| S77R-19 | Low | The owner-accepted effect on 0.4.14 users was not stated | Stated under the decisions |
| S77R-20 | Low | The Claude read-back command was not named | `claude plugin list --json` and the Codex list command named |
| S77R-21 | Low (note) | No path for a failed cloud run | Recorded, reported, not re-run without a new owner decision |
| S77R-22 | Low (note) | Local and runner CLI versions may differ | The STATEMENT and the record carry both |
| S77R-23 | Low (note) | Template rows missing | Closure revision, Strict checker, Profile / resource and XSS classification added |

## Seat token use

| seat | model | effort | input | cache write | cache read | output |
| --- | --- | --- | --- | --- | --- | --- |
| rule-only review, revision01 | claude-opus-5-5 | high | 100 | 177613 | 6123376 | 52575 |
