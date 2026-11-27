# Wave 3 integration record (from 2026-11-18)

Integrations of REQ-20261103-043 wave 3 onto `cp/wave3`, by hand, in the wave-2 pattern:

1. a fresh clone with `transfer.fsckObjects`, `--no-hardlinks` and `core.autocrlf=false`;
2. a check that the fetched branch tip equals the approved candidate;
3. `merge --no-ff`, with the tip as the first parent and the candidate as the second (owner decision 2026-11-07 "1.A");
4. the full suite under the host lock;
5. a fast-forward push and the CI readback.

## Tickets 65 and 69 (2026-11-18 to 2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 65 retire the flow engine, the private router, the profile and the router telemetry | `b185dea9` | revision02 correction review `APPROVED` | `361ba136` |
| 69 token use per seat | `7cc0e08f` | revision01 correction review `CONVERGENCE_REVIEW_REQUIRED`, disposition `APPROVED` under rule B (S69-07, S69-08 carried) | `9b746c97` |

Integration clone: `C:/Temp/claude/jas-integ65`.

- **First run:** ticket 65 was merged alone on `dc4cc524`, and the full suite ran under the host lock: 5 failed, 3535 passed, 32 skipped. Every failure is a base name, so zero new red.
- **The tip moved:** before the push, the control plane pushed two docs-only commits (`369d6844`, `d4e432b5`), so the tip moved. Both merges were redone in order on `d4e432b5`: 65 as `361ba136`, then 69 as `9b746c97`.
- **Second run:** the full suite ran again on `9b746c97` under the host lock: 5 failed, 3628 passed, 32 skipped. Every failure is a base name, so zero new red.

| Check | Result |
| --- | --- |
| Pushed | `cp/wave3` at `9b746c97`, a fast-forward from `d4e432b5` |
| CI readback | run 44342660977 on `9b746c97`: `test (linux)` and `test (windows)` both `success` |

## USAGE cells (readiness criterion 5)

After integration, the control plane appended one `USAGE` cell per seat to each returned receipt. The script is `append_usage.py`, and it keeps the receipt as returned in `RETURN.as-returned.md`. The values are the host-reported usage, summed per unique message id, and they are the same values as in each review record.

- **P9 is not rerun** on a receipt that holds `USAGE` cells. That is the rule of ticket 69, S69-07.
- **E1 is rerun with the integrated `evidence_gate.py`:**

  | Receipt | sha256 after append | E1 with USAGE |
  | --- | --- | --- |
  | `.worktrees/65-retire-engine-and-private-router-out/RETURN.md` | `087fb799578ae1c46c1fa2303c5078c7cf8be6249bf1cd55006cbd722775aa9a` | exit 0, `cells=6 defects=0` |
  | `.worktrees/69-token-use-per-seat-out/RETURN.md` | `67f5f45a33bf99fe909ea905c637139a71dccb4422c2a58739666d8d69bab7ab` | exit 0, `cells=7 defects=0` |

- **`usage_report.py`** was run over both receipts with `template/doc/handoffs/governance/usage-expectation.TEMPLATE.json`, the values the owner confirmed on 2026-11-18 ("1A"). It exits 1:

  ```text
  seat:implementation-standard/65-impl implementation-standard output=88467 processed=23263970 WITHIN
  seat:ticket-review/65-rev02 ticket-review output=91014 processed=24146363 OVER_PROCESSED
  seat:implementation-standard/69-impl implementation-standard output=149575 processed=41813298 OVER_OUTPUT,OVER_PROCESSED
  seat:ticket-review/69-rev01 ticket-review output=97780 processed=17044392 WITHIN
  ```

  Each seat over its expectation is explained in its review record. Being over does not block integration (owner decision 2026-11-18 "1A").

## Ticket 72 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 72 dispatch lint: one action per line | `8c770265` | revision01 correction review `CONVERGENCE_REVIEW_REQUIRED`, disposition `APPROVED` under rule B (S72-05, S72-06 carried) | `fa4019fa` |

The integration clone `C:/Temp/claude/jas-integ-72` was made from `1d4145ea`, using the integration script `integ_one.sh`.

| Check | Result |
| --- | --- |
| Full suite in the integration clone under the host lock | 5 failed, 3644 passed, 32 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `fa4019fa`, a fast-forward from `1d4145ea` |
| CI readback | run 44381596401 on `fa4019fa`: `test (linux)` and `test (windows)` both `success` |
| USAGE | two cells were appended to `.worktrees/72-lint-out/RETURN.md` (sha256 `d3919b8941fef7e8502b0574078ca373509019464b42a4c29739c12c5f8c893d`); E1 gives exit 0 (`cells=7 defects=0`); `usage_report.py` gives exit 0 with both seats `WITHIN` |

From this integration onward, the control plane writes dispatches to the new R5: one action per line, with literal payloads in backticks and each enumerated item as its own list item (S72-05).

## Tickets 68 and 66 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 68 archive the router-era SPECs, SPEC archive rule, ADRs superseded | `c3ecdd6b` | revision01 correction review `APPROVED` | `8c4e9a77` |
| 66 retire the cross-lifetime bridge | `2d11118c` | revision01 correction review `APPROVED` | `cded7a27` |

The integration clone `C:/Temp/claude/jas-integ-6866` was made from `8b82a2b1`. Both candidates were merged in order. `REQ-20261103-043.md` merged automatically, without a conflict.

| Check | Result |
| --- | --- |
| Full suite on `cded7a27` in the integration clone under the host lock | 5 failed, 3140 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `cded7a27`, a fast-forward from `8b82a2b1` |
| CI readback | run 44390034272 on `cded7a27`: `test (linux)` and `test (windows)` both `success` |
| USAGE, ticket 68 | `.worktrees/68-archive-specs-out/RETURN.md` (sha256 `61da8e6790ca0334f6b3d7c2b6b938c766f1b6223eb483f02fbd8d755371c2a5`); E1 with L1 required gives exit 0 (`cells=8 defects=0`); both seats `WITHIN` |
| USAGE, ticket 66 | `.worktrees/66-retire-bridge-out/RETURN.md` (sha256 `91b44069dd9251f760194cfbea21c0b50a20c7d4132c30bafe64a57d13625365`); E1 gives exit 0 (`cells=6 defects=0`); the implementation seat is `OVER_PROCESSED` and the review seat is `OVER_OUTPUT,OVER_PROCESSED`, both explained in the review record |

The suite now holds 3140 passed tests, down from 3644 at ticket 72. The tests that ticket 66 retires account for the difference.

## Ticket 70 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 70 wave-2 template follow-ups, tracked-path length cap | `548665e5` | revision02 correction review `CONVERGENCE_REVIEW_REQUIRED`, disposition `APPROVED` under rule B (S70-05 to S70-07 carried) | `277aa80b` |

The integration clone `C:/Temp/claude/jas-integ-70` was made from `68ace49c`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3171 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `277aa80b`, a fast-forward from `68ace49c` |
| CI readback | run 44396032169 on `277aa80b`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/70-templates-out/RETURN.md` (sha256 `de3fb29e913e884922770c02df7d651560acb1d0640ca6ca8fb774d74bf0484c`); E1 gives exit 0 (`cells=6 defects=0`); the implementation seat is `OVER_PROCESSED`, explained in the review record, and the review seat is `WITHIN` |


## Ticket 67 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 67 governance documents name no retired surface; exclusive-file-lock restored | `0f621d9c` | revision04 correction review `APPROVED` | `b97077e6` |

The integration clone `C:/Temp/claude/jas-integ-67` was made from `2b787737`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3224 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `b97077e6`, a fast-forward from `2b787737` |
| CI readback | run 44455722140 on `b97077e6`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/67-doc-sweep-out-c1/RETURN.md` (sha256 `630e88285879fccbe6fa37dda73f08bb7bc0337a7396c90d40f4a953b167b837`) with both seats' cells; E1 gives exit 0 (`cells=8 defects=0`); `usage_report.py` gives the implementation seat `OVER_OUTPUT,OVER_PROCESSED` and the review seat `WITHIN`, exit 1, explained in the review record. The first-pass receipt `.worktrees/67-doc-sweep-out/RETURN.md` (sha256 `3093251db52aa9274555c29ed5eb9a8b354b930cab31c7c8396c34308c3aad2d`) is kept beside it. |

After the integration, the control plane rebased its four unpushed ticket-76 commits onto `b97077e6` before pushing them. The content is unchanged; the old and new commit identifiers are mapped in the ticket-76 review record.

## Ticket 74 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 74 wave-3 rule texts at named anchors | `4943d76c` | revision04 initial review `APPROVED` (S74-01 to S74-05 recorded and carried) | `f257bffa` |

The integration clone `C:/Temp/claude/jas-integ-74` was made from `ef87d8ac`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3240 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `f257bffa`, a fast-forward from `ef87d8ac` |
| CI readback | run 44474507317 on `f257bffa`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/74-rule-texts-out/RETURN.md` (sha256 `b2c33f235f1420c0add13989e551a3b2bef0f273757abea9e509eb583ab4367c`) with both seats' cells; E1 gives exit 0 (`cells=7 defects=0`); `usage_report.py` gives both seats `WITHIN`, exit 0 |

## Ticket 75 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 75 the repository's own ticket template follows the harness; dispatch lint R7 checks the dispatch digest | `dd10fca6` | revision03 initial review `APPROVED` (S75-01 and S75-02 recorded) | `aa5d1d0d` |

The integration clone `C:/Temp/claude/jas-integ-75` was made from `f42444a4`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3274 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `aa5d1d0d`, a fast-forward from `f42444a4` |
| CI readback | run 44491650931 on `aa5d1d0d`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/75-own-tickets-out/RETURN.md` (sha256 `7b0c3410630ec48be10a1032235af7a7ec54bb2b01f6466e7964114a4b7300c5`) with both seats' cells; E1 gives exit 0 (`cells=7 defects=0`); `usage_report.py` gives both seats `WITHIN`, exit 0 |

From this integration on, the control plane lints every dispatch with `--ticket` before it goes out.

## Ticket 76 (2026-11-19)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 76 seat model and effort bound to the profile; USAGE effort line; mismatch verdicts; dispatch lint R8 | `78810fa6` | revision03 initial review `APPROVED` (S76-01 to S76-05 recorded) | `82a250a8` |

The integration clone `C:/Temp/claude/jas-integ-76` was made from `ecb66083`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3335 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `82a250a8`, a fast-forward from `ecb66083` |
| CI readback | run 44505684582 on `82a250a8`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/76-seat-binding-out/RETURN.md` (sha256 `15119b07b26f8b5dfdb3a448381f0ccd4cf520dc01a76c51310bba292df467c6`) with both seats' cells, each with an `effort:` line read from the host transcript. E1 with the integrated gate gives exit 0 (`cells=7 defects=0`). The integrated `usage_report.py`, run with the repository's own `doc/handoffs/2026/workflow-governance/usage-expectation.json`, gives `model=claude-sonnet-5-5 effort=high … WITHIN` and `model=claude-opus-5-5 effort=high … WITHIN`, exit 0. |

From this integration on, every USAGE cell the control plane appends carries the seat's effort, and every usage report runs with the repository's own expectation file.

## Ticket 73 (2026-11-20)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 73 rework-record block and `rework_report.py`; the wave-3 code-review records backfilled | `b5121ee0` | revision03 correction review `APPROVED` (S73-01 and S73-03 carried to wave 4) | `3cd4bf5d` |

The integration clone `C:/Temp/claude/jas-integ-73` was made from `7b25dabd`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3398 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `3cd4bf5d`, a fast-forward from `7b25dabd` |
| CI readback | run 44608980985 on `3cd4bf5d`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/73-rework-out-c1/RETURN.md` (sha256 `a98b9bb4711f9484bb6311cf618ed4bf87e4d8958fecac4973edc0137b5f624a`) with both seats' cells and `effort:` lines; E1 gives exit 0 (`cells=8 defects=0`); `usage_report.py` with the repository's expectation gives the implementation seat `OVER_PROCESSED` and the review seat `WITHIN`, explained in the review record |
| Rework report, first run on the integrated tree | over the wave-3 code-review records: `TOTAL tickets=11 rounds=21 CONTROL_PLANE_RULE=5 RETURN_UNTRUE=2 DESIGN_UNFORESEEN=2 IMPLEMENTATION_DETAIL=8`, exit 0 |

## Ticket 79 (2026-11-26)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 79 a read-only question goes straight to its leaf | `74b637d5` | revision03 correction review `APPROVED` (S79-02 and S79-03 carried as out-of-scope hardening) | `41477f90` |

The integration clone `C:/Temp/claude/jas-integ-79` was made from `35298bdf`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3419 passed, 22 skipped; every failure is a base name, so zero new red |
| Pushed | `cp/wave3` at `41477f90`, a fast-forward from `35298bdf` |
| CI readback | run 45662753511 on `41477f90`: `test (linux)` and `test (windows)` both `success` |
| USAGE | `.worktrees/79-lookup-out/RETURN.md` (sha256 `9b7c176825b5b0821e7787c2f9c830eb7420dcc6fd95cb05b16215842d226704`) with both seats' cells and `effort:` lines; E1 gives exit 0 (`cells=6 defects=0`); `usage_report.py` with the repository's expectation gives both seats `WITHIN`, exit 0 |
| Rework report over the wave-3 code-review records | `TOTAL tickets=12 rounds=23 CONTROL_PLANE_RULE=5 RETURN_UNTRUE=3 DESIGN_UNFORESEEN=2 IMPLEMENTATION_DETAIL=8`, exit 0 |

## Ticket 71 (2026-11-26)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 71 publication 0.5.0 as Software Factory | `824d00b9` | revision05 correction review `CONVERGENCE_REVIEW_REQUIRED`, disposition `APPROVED` under rule B (S71-02 to S71-04 carried) | `f53ecc6a` |

The integration clone `C:/Temp/claude/jas-integ-71` was made from `4ddea536`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3430 passed, 22 skipped. Every failure is a base name, so zero new red. The four publication tests and `test_the_pinned_sha_exists` fail here because the clone has no local `refs/heads/publication-0.5.0`; they stay registered until the anchor is pushed |
| Pushed | `cp/wave3` at `f53ecc6a`, a fast-forward from `4ddea536` |
| CI readback | run 45680692755 on `f53ecc6a`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | `d355b4a26336cebbe4e8e28650ce0120d4c39a13`, named by the local ref `refs/heads/publication-0.5.0` and pinned by the development `marketplace.json`; not pushed; the publication repository is untouched |
| Local test marketplace | `C:/Temp/claude/sf-050-local/`, its plugin tree equal to the extracted publication commit |
| USAGE | `.worktrees/71-publication-out/RETURN.md` (sha256 `2c7f81fbba33346a606a8dd8442d76829aa0531c4bdbe21d4636acdca8a5a5c7`) with both seats' cells and `effort:` lines; E1 gives exit 0 (`cells=11 defects=0`); `usage_report.py` with the repository's expectation gives both seats `WITHIN`, exit 0 |
| Rework report over the wave-3 code-review records | `TOTAL tickets=13 rounds=25 CONTROL_PLANE_RULE=5 RETURN_UNTRUE=3 DESIGN_UNFORESEEN=2 IMPLEMENTATION_DETAIL=9`, exit 0 |

## Ticket 80 (2026-11-26)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 80 a read-only lookup goes through the 流程索引 | `7ec1f539` | revision02 initial review `APPROVED` (S80-01 and S80-02 moved into ticket 81 by owner decision; S80-03 and S80-04 handled) | `72d035b6`, merged forward at `31f15b7c` |

The integration clone `C:/Temp/claude/jas-integ-80` was made from `4fe5a8ef`.

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3442 passed, 22 skipped. Every failure is a base name, so zero new red |
| Merged forward | Three record-only commits (`12dc603c`, `57cd380d`, `cf504055`: ticket 81 text and its review record, REQ-043 and the ticket index) landed on `cp/wave3` during the run. They were merged into the integration as `31f15b7c`; CI covers that merge |
| CI readback | run 45753850263 on `31f15b7c`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | `193777a7a8503d869c521425befc0d41ab323c28`, named by the local ref `refs/heads/publication-0.5.0` since 2026-11-26T02:42:39Z; not pushed |
| USAGE | `.worktrees/80-index-out/RETURN.md` (sha256 `bea46f0d25a437070c7884d3ea53f7822b2d662dfd21a068d03b6ff28fcc693b`) with both seats' cells and `effort:` lines; E1 gives exit 0 (`cells=10 defects=0`); `usage_report.py` gives both seats `WITHIN` |
| Rework report over the wave-3 code-review records | `TOTAL tickets=14 rounds=26 CONTROL_PLANE_RULE=5 RETURN_UNTRUE=3 DESIGN_UNFORESEEN=2 IMPLEMENTATION_DETAIL=9`, exit 0 |

## Tickets 81 and 77 (2026-11-26)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 81 old and new do not fight; the first 流程索引 row narrowed with a tie-break | `d07bf53b` | revision04 initial review `APPROVED` (S81-01 carried to wave 4) | `c6ae03e9`, merged forward at `02e1691f` |
| 77 acceptance of 0.5.0 | `8cf1e387` | revision04 correction review `APPROVED` (S77-11, S77-16 and S77-17 carried to wave 4) | `e87bc5cb` |

| Check | Result |
| --- | --- |
| Full suite under the host lock | 81: 5 failed, 3459 passed. 77: 5 failed, 3524 passed. Every failure is a base name, so zero new red |
| Merged forward | One record commit (`f6decb64`, ticket 77's approval record) landed during the 81 run. It was merged into the integration as `02e1691f`; CI covers it |
| CI readback | run 45761709630 on `02e1691f` and run 45763761666 on `e87bc5cb`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | `6d04fa6d0cf0c1e7134a312894adc219f44bf4a9`, named by the local ref `refs/heads/publication-0.5.0`; not pushed |
| Final local lifecycle | at `e87bc5cb` with `--expected-publication 6d04fa6d…`: exit 0, every verdict `PASS` (`77-acceptance-0-5-0-record.md`) |
| USAGE | 81: `.worktrees/81-coexist-out/RETURN.md` (sha256 `4e5976fa4032340abe6cfc82eea66786632fb95f1510ef5a2f71e66109de366c`), E1 `cells=11 defects=0`, both seats `WITHIN`. 77: `.worktrees/77-acceptance-out/RETURN.md` (sha256 `a47378c6e859f66a2371b52928a57ce25f94353a9c2458ab58890aa49b5ce18e`), E1 `cells=9 defects=0`, both seats `OVER_OUTPUT,OVER_PROCESSED`, explained in the 77 review record |
| Rework report over the wave-3 code-review records | `TOTAL tickets=16 rounds=32 CONTROL_PLANE_RULE=6 RETURN_UNTRUE=4 DESIGN_UNFORESEEN=4 IMPLEMENTATION_DETAIL=12`, exit 0 |

## Ticket 82 (2026-11-26)

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 82 the plugin's SessionStart hook points every session at its rules and the 流程索引, and stops a session that also lists the old plugin | `4be37a7a` | revision06 initial review `APPROVED`, no findings | `f0ba4995` |

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3565 passed, 22 skipped. Every failure is a base name, so zero new red |
| Merged forward | none; the base `6f91e7b5` was still the tip of `cp/wave3` at push |
| CI readback | run 45800560207 on `f0ba4995`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | `3ab86d439f236880db92648ab28724a626dc360b`, named by the local ref `refs/heads/publication-0.5.0` since 2026-11-26T09:10:07Z; not pushed |
| Final local lifecycle | at `f0ba4995` with `--expected-publication 3ab86d43…`: exit 0, every verdict `PASS` (`77-acceptance-0-5-0-record.md`) |
| USAGE | `.worktrees/82-hook-out/RETURN.md` (sha256 `1fdf8bdf3c869b5fc727caf7471a62409caaaa96886a8dc5f02c27c79e985560`), E1 `cells=11 defects=0`; both seats over one round's expectation because each ran three rounds by resumption, explained in the 82 review record |
| Rework report over the wave-3 code-review records | `TOTAL tickets=17 rounds=35 CONTROL_PLANE_RULE=6 RETURN_UNTRUE=4 DESIGN_UNFORESEEN=4 IMPLEMENTATION_DETAIL=12`, exit 0 |

## Ticket 82 revision08 (2026-11-26)

Revision06 was integrated at `f0ba4995`. The owner then found that the Codex desktop app does not ask to trust a changed hook and decided "A" (REQ-043); revision07 and revision08 reopen the ticket with the owner override recorded in it.

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 82 revision08: README section 4 sends a Codex user to the terminal once to trust the hook | `82cd82ab` | revision08 initial review `APPROVED` by a fresh review seat, no findings (N10 carried to wave 4) | `9f764a88`, merged forward at `3e54da2c` |

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3565 passed, 22 skipped. Every failure is a base name, so zero new red |
| Merged forward | One record commit (`d8d15293`, REQ-044) landed on `cp/wave3` during the run. It was merged into the integration as `3e54da2c`; CI covers that merge |
| CI readback | run 45843976423 on `3e54da2c`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | `e08e82d3373547a5448040638fb22b1810dc9cf3`, named by the local ref `refs/heads/publication-0.5.0` since 2026-11-26T13:54:19Z; not pushed |
| Final local lifecycle | at `3e54da2c` with `--expected-publication e08e82d3…`: exit 0, every verdict `PASS` (`77-acceptance-0-5-0-record.md`) |
| USAGE | `.worktrees/82-hook-out/RETURN.md` (sha256 `4160aef06bd827b4cb731576a314fec5821fb8b3a17f0fec67a40fefd3f87d0b`), E1 `cells=11 defects=0`; the implementation seat's row is a four-round total, and the fresh review seat is `WITHIN`, both explained in the 82 review record |
| Rework report over the wave-3 code-review records | `TOTAL tickets=17 rounds=36 CONTROL_PLANE_RULE=6 RETURN_UNTRUE=4 DESIGN_UNFORESEEN=4 IMPLEMENTATION_DETAIL=12`, exit 0 |

## Ticket 77 revision06 (2026-11-27)

Revision04 was integrated at `e87bc5cb`. The one cloud run (45920193720) failed at `build` because the acceptance workflow installed no Python package, and the owner decided "A" (REQ-043, 2026-11-27); revision05 and revision06 reopen the ticket with the owner override recorded in it.

| Ticket | Approved candidate | Approval | Integration commit |
| --- | --- | --- | --- |
| 77 revision06: the acceptance workflow installs `requirements-dev.txt`, the README sentence is corrected, the parity run is written down | `c983c6ef` | revision06 initial review `CHANGES_REQUESTED` on `ec0c06dc` (S77-18), correction review `APPROVED` (S77-20, S77-21 carried to wave 4) | `34583ba2` |

| Check | Result |
| --- | --- |
| Full suite under the host lock | 5 failed, 3569 passed, 22 skipped. Every failure is a base name, so zero new red |
| Merged forward | Nothing landed on `cp/wave3` during the run |
| CI readback | run 45935267364 on `34583ba2`: `test (linux)` and `test (windows)` both `success` |
| Publication commit | unchanged: `e08e82d3373547a5448040638fb22b1810dc9cf3`. The candidate changes `.github/`, `ci/` and `tests/` only, none of which is in the payload |
| USAGE | `.worktrees/77-acceptance-out/RETURN.md` (sha256 `bbdece1a2ffb57f714c519a1a5c690b3ca5af948d4799ada365a3ff51c39eab2`), E1 `cells=9 defects=0`; both seats `WITHIN`, by round in the 77 review record |
| Rework report over the wave-3 code-review records | `TOTAL tickets=17 rounds=38 CONTROL_PLANE_RULE=6 RETURN_UNTRUE=4 DESIGN_UNFORESEEN=4 IMPLEMENTATION_DETAIL=13`, exit 0 |
| Time | owner decision to integration: about 4 hours on 2026-11-27, of which the one-line correction round took about 1.5 hours (the seat's rerun of every cell, the correction review, this integration). REQ-044 T13 takes it as its baseline |

## Release of 0.5.0 (2026-11-27)

The steps are those of ticket 71's paragraph "The release, after review approval", with ticket 82's publication commit (`doc/runbooks/release.md`). Ticket 77's acceptance was met first: cloud run 45941477324, ten of ten `PASS` on `main` `fe0b1245` (`77-acceptance-0-5-0-record.md`, section "The cloud run"). Each push was shown to the owner with its rehearsal and the values to check, in a runnable block only once it could run (REQ-044 T4 rule (d)); the owner ran each one, and the control plane read the remote back.

| Step | What | Result, read back by the control plane |
| --- | --- | --- |
| 2 | The owner renamed the publication repository `Johnny_AI_Skill_publication` to `software-factory-plugin` | `gh repo view johnnyliu365-sys/software-factory-plugin`: public, `main` at `0b3afd36`, tags `plugin-v0.4.10` to `plugin-v0.4.14` |
| rule | `doc/runbooks/release.md`: no tag for the version, and the version greater than every tag | `git ls-remote --tags … "refs/tags/plugin-v*"` listed 0.4.10 to 0.4.14 and no `plugin-v0.5.0` |
| 3 | Tag `plugin-v0.5.0` pushed to the publication repository | `refs/tags/plugin-v0.5.0` is `e08e82d3373547a5448040638fb22b1810dc9cf3` (04:54:47Z) |
| 3 | The publication repository's `main`, by `--force-with-lease=refs/heads/main:0b3afd36…` | `refs/heads/main` is `e08e82d3…` (04:56:50Z); `plugin-v0.4.14` still names `0b3afd36` |
| 4 | Branch `marketplace` pushed to the publication repository | `refs/heads/marketplace` is `bc8a2d2d2155ebcf3f04770c37a4dd41662036d7` (04:57:36Z), a parentless commit whose tree holds only `.claude-plugin/marketplace.json`, the blob `385259b6615b42cec1e73d110af3c18521fa52ab` of the development `main`. The public raw URL of the README answered 200 with the same blob id |
| 5 | `refs/heads/publication-0.5.0` pushed to the development repository | `e08e82d3…` (05:01:03Z). The owner pressed the block twice; the second push printed `Everything up-to-date` |
| 6 | The development `main` fast-forwarded to `68afa9e22c555beedb6a8e49c630f1b9dce4f777` (CI run 45942826956 `success` on both jobs), and the annotated tag `v0.5.0` | `refs/heads/main` and `refs/tags/v0.5.0^{}` are `68afa9e2…`; the tag object is `2c48384ab7e9d1b540bbf7c6d66b59587513c0fa` (05:25:27Z) |
| 7 | Readback from a fresh clone made with `--no-hardlinks`: `v0.5.0` checked out, `git branch publication-0.5.0 origin/publication-0.5.0`, then `--verify-only --ref refs/heads/publication-0.5.0` | `verified e08e82d3373547a5448040638fb22b1810dc9cf3`, exit 0, porcelain empty |
| 8 | One smoke install through the public path, by the owner, following `doc/runbooks/install-guide-0.5.0.md` after removing the local-marketplace install and both cache folders | Passed on both hosts, below |
| 9 | The eight rows of the four publication tests removed from `ci/registered-failures.json` | commit `b602c87b`. CI run 45945688417 on `main` `68afa9e2`, started after the anchor push, reported `REGISTERED_NOW_PASSING` for 4 rows on Linux, as step 9 expects |

**The smoke install (step 8).** The control plane read the hosts' state afterwards; it read no credential file.

- **Claude Code.** `claude plugin list`: `software-factory@software-factory`, 0.5.0, scope user, enabled. The marketplace's source is the README's raw URL on the publication repository. The cache folder `…/cache/software-factory/software-factory/0.5.0` equals `git archive plugin-v0.5.0` in all 150 files once line endings are ignored (the host's Git wrote CRLF); it also holds the host's own `.in_use` markers. In a new session of the test project (Claude Code 2.1.325), the transcript holds the hook's text with the installed path in place of `${CLAUDE_PLUGIN_ROOT}`. To "P0 權限是什麼" the session read the plugin's `AGENTS.md` and answered from `P0：權限與所有權`, naming the file, the anchor `#p0-permissions` and the version 0.5.0; it looked for a target `AGENTS.md` by file name and did no keyword search.
- **Codex (0.172.0).** The marketplace's source is `https://github.com/johnnyliu365-sys/software-factory-plugin.git` with `ref = "marketplace"`. The installed copy is a clone at `e08e82d3373547a5448040638fb22b1810dc9cf3`, equal to the package once line endings are ignored. The plugin is enabled, and the hook has a trust record. `codex exec --skip-git-repo-check -s read-only "Answer exactly OK."` in the test project printed `hook: SessionStart Completed`. The owner did not show a Codex answer to the P0 question after this install; the earlier retest of the same package did (`77-acceptance-0-5-0-record.md`).
- **Seen on the way.** The session above ran Claude Code 2.1.325, the terminal has 2.1.332 and one terminal tab showed 2.1.316; the acceptance pins 2.1.332. `codex plugin list --json` did not return within two minutes when the control plane ran it without a terminal, so the Codex state was read from its configuration and cache instead.

**Not part of this release, carried.** The owner keeps the development repository public until three things are done (REQ-043, owner decision 2026-11-27 "A"): commits that change only documents do not run the suite; the two URLs of the development repository in `ci/acceptance/lifecycle.py` move or are retired; the install guide gets a home an outside installer can open. Installation by someone other than the owner (REQ-044 T18 measurement (3)) is the owner's next step.

**Outside install, first report (2026-11-27).** The owner passed on the output of an installer on another computer: the first command of the guide's section 3, `codex plugin marketplace add johnnyliu365-sys/software-factory-plugin --ref marketplace`, failed in PowerShell with `CommandNotFoundException` for `codex`. The guide's section 1 lists `codex --version` as a check, but section 3 did not repeat it and the troubleshooting table had no row for a missing `codex` command. The guide gains the check at the head of section 3 and row X0. For REQ-044 T18 measurement (3) this attempt counts as one that needed help, at the first Codex command; whether section 2 (Claude Code) went through on that computer is not yet known.
