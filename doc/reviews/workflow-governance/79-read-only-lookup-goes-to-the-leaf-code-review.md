# Ticket 79, closure revision03: initial code review

- **Candidate:** `12304e8557dfc92a7377c1657cdfc3986ba9cd94`, on branch `cp/wave3-79-lookup`. It is two commits on base `69b4cdfbca9feb663ab1fdb694cb20236174d027`: `73d86d19` (the texts and the test) and `12304e85` (the test reads LF-normalised text).
- **Label:** initial review of closure revision03, labelled before dispatch.
- **Seat:** `ticket-review`, run id R79-1, claude-opus-5-5. Worktree `.worktrees/79-lookup-review`, detached at the candidate, porcelain empty before and after.
- **Read:** the ticket at the candidate (items 1 to 5, the copies note, the TDD design, the defect table, 完成定義, the boundary block), and the rule-only review record. The dispatch `JAS-79-1.yaml` at `2f2f96e8`: its sha256 `1a7465bc…e7a318` matches the brief. Also `RETURN.md`, `RETURN.as-returned.md` and every capture, `CodeReview.md` §1 to §5, and `review-checks.md`.
- **Out of scope:** XSS, Provider, Secret and UI do not apply. The change is governance Markdown plus one stdlib-only test, with no Browser, DOM or external effect. Profile fan-out does not apply either: one implementer, one reviewer.

**Verdict: `CHANGES_REQUESTED`.** The candidate is correct, and every shipped text is byte-exact. One evidence gap goes back now in one additive commit, S79-01. The gap is that ticket item 1 says "The five steps stay as they are", and no test pins those steps. My counter-mutations CM4 and CM4b reword and delete a start-order step, and they turn nothing red. The receipt's STATEMENT says the new test pins "the unchanged five steps of the start order", which the evidence contradicts. So this is `RETURN_UNTRUE`. Nothing else blocks.

## Findings

| id | §4 class | severity | location | finding | evidence |
| --- | --- | --- | --- | --- | --- |
| S79-01 | `EVIDENCE_DEFECT` (item 1 "The five steps stay as they are"; STATEMENT item 4). The STATEMENT claim is contradicted, so the cause is `RETURN_UNTRUE` | Low. Under §5 rule B it would not block, but this is the initial review, so it goes back now | `tests/test_entry_read_only_lookup.py:194-207`; `79-lookup-out/RETURN.md` STATEMENT item 4 | STATEMENT item 4 says: "The test also pins … the unchanged five steps of the start order". The test only walks the numbered block and checks that its last numbered line is `5. ` (`:206` "must keep its five steps"). It pins neither the step texts nor the count. No other P1 test pins them either. A second, smaller inaccuracy: STATEMENT item 1 says the start steps are at "SKILL.md lines 13 to 18", but step 5 runs to line 20. **Smallest fix (one additive commit, inside the boundary):** in `check_agents`, compare `lines[heading + 4 : cursor]` with a constant that holds the five unchanged step lines exactly as at base. Add one injection case, "a start-order step reworded is red". The STATEMENT claim is then true. Rebuild the receipt and correct "13 to 18" to "13 to 20". If you prefer not to pin the steps, correct the STATEMENT sentence instead. That closes the untrue claim but leaves CM4 at zero red. | CM4 (`取得唯一 action` → `取得 action` in step 3): `find_defects` → `[]`. The new test exits 0. The other four P1 files show only the four registered failures. CM4b (step 2 deleted): `find_defects` → `[]`. Files: `79-rev03-initial-counter-mutations.txt` and `79-rev03-initial-defects-and-yaml-differential.txt` |
| S79-02 | `OUT_OF_SCOPE_HARDENING` | Low | `tests/test_entry_read_only_lookup.py:102-125` (`plain_scalar_defect`, `FRONTMATTER_LINE`) | Seat flag 1. As a general YAML check, the reader accepts two values that PyYAML 6.0.3 rejects: `a:\tb` and `a\t#b`, both `ScannerError`. It also accepts implicit non-string scalars: `yes`, `null`, `~`, `1.0`. None of this is reachable for the shipped file, because `check_skill` also requires `description == DESCRIPTION` byte-exact (`:240`) and the `name` is pinned (`test_the_skill_frontmatter_parses_and_names_the_skill`). My CM7 and CM8 inject exactly these tab forms into the description, and both go red: "not the ticket's text". **Follow-up, not this ticket:** widen `" #"` and `": "` to a space-or-tab class, and say in the docstring that the reader proves "string scalar" only together with the exact pin | Differential table in `79-rev03-initial-defects-and-yaml-differential.txt` |
| S79-03 | `OUT_OF_SCOPE_HARDENING` (ticket and dispatch authoring, control plane) | Low | ticket 完成定義 "the five cases of TDD 2"; `JAS-79-1.yaml` M1 | Seat flag 4. TDD 2 lists eight bullets, nine mutations in all, but 完成定義 says "the five cases". The dispatch's M1 list leaves out the TDD 2 bullet "the description's last sentence removed". The seat's ninth mutation, M1.9, is that bullet, so the receipt covers TDD 2 in full. Nothing is open on the candidate | `79-lookup-out/M1.txt:3504-3932` (M1.9 RED, restored) |
| S79-04 | `OUT_OF_SCOPE_HARDENING` (dispatch residue rule, control plane) | Low | `C:/Temp/claude/jas79_edit.py` (4577 bytes, 2026-11-25 23:48) | The seat left a one-shot edit script that carries no run id, which goes against the dispatch `residue` rule. The STATEMENT discloses it, with the reason. The control plane removes it after reading it | `ls` readback |

## Per-check table

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1a | Item 1, condition line | PASS, byte-exact | Script `R79-1_exact.py` reads `git show <candidate>:…` blobs, so no checkout line endings are involved. It extracts each text from the ticket blob at the candidate. `AGENTS.md:10` equals the ticket text, at heading + 2, and the old line is absent. The blobs hold no CR |
| 1b | Item 2, anchor with its blank lines, and the paragraph | PASS, byte-exact | After step 5 (`AGENTS.md:18`) come `""`, `<a id="read-only-lookup"></a>` (`:20`), `""`, the paragraph (`:22`, 548 characters, once), and `""`. Line `:24` begins 「狀態只保存」. This is the same shape as `p0-source-type` |
| 1c | Item 3, description | PASS, byte-exact | `SKILL.md:3` equals `description: ` + the ticket text (633 characters). PyYAML 6.0.3 `safe_load` on the committed frontmatter gives keys `{name, description}`, and the description equals the ticket text |
| 1d | Item 4, start step 1 with its link; steps 2 to 5 | PASS, byte-exact | `SKILL.md:13` equals the ticket text. Base steps 1 to 4, each renumbered +1 with nothing else changed, equal candidate lines 14 to 20. A blank line follows |
| 1e | No other sentence changed | PASS | `git diff 69b4cdfb 12304e85 -- AGENTS.md skills/`: one changed line, plus the 4-line anchor and paragraph block in `AGENTS.md`; in `SKILL.md`, the description line, the new step 1 and four renumbered prefixes. `git diff --check` is clean |
| 2 | The link and the payload closure | PASS | `skills/johnny-project-takeover/../../AGENTS.md` resolves to the root `AGENTS.md`, a declared payload file (`plugin.json:36`). The id `read-only-lookup` occurs exactly once. P1 `PayloadClosureTests` pass: no escaping reference and no stray token. The new inline tokens `AGENTS.md` and `Workflow.md` resolve inside the payload. CM2 (link changed to `../AGENTS.md`) and CM3 (anchor id renamed) are both red, with the intended defect messages |
| 3a | The test pins each item-5 rule | PASS for item 5's list. Item 1's "five steps stay" is not pinned (S79-01) | Condition line: `:169-172` and `:186-192`. Anchor, blank lines and paragraph between step 5 and 狀態只保存: `:208-216`. Description: `:240`. Start steps: `:245-251`, exact block |
| 3b | It fails for the right reason | PASS | `find_defects` messages per mutation (`…-defects-and-yaml-differential.txt`). CM1: "paragraph must appear exactly once, word for word". CM2: "'## Start' must be … word for word". CM3: "anchor … must stand on its own line exactly once". CM5: "starts with the indicator '\"'". CM6: "contains a space and a number sign" |
| 3c | Reviewer counter-mutations, through other doors | 9 run. 7 red; CM4 and CM4b zero red (S79-01) | In a disposable `--no-hardlinks` clone, a CRLF checkout (`core.autocrlf=true`). Each runs the full new test file, without `-x`, and is restored with porcelain empty. The output was read unfiltered, with no output-reducing wrapper. R1 reruns the seat's M1.1 (condition line without its carve-out): red. CM1, a one-character change in an unnamed paragraph sentence: red. CM2, link retarget: red. CM3, anchor id renamed: red. CM4, start-order step 3 reworded: **zero red**, also zero across the other four P1 files. CM4b, step 2 deleted: **zero red**. CM5, description double-quoted (valid YAML): red, failing closed. CM6, ` #` in the description: red. CM7 and CM8, `\t#` and `:\t`: red through the exact pin |
| 3d | Seat flag 1: YAML parse by a local reader | ACCEPTED, with S79-02 | Colon plus space: rejected, and PyYAML agrees (`ScannerError`). This is the S79R-15 case. ` #`: rejected, which is stricter than YAML: YAML truncates to a comment, and the exact pin would catch that too. Leading indicators: the set `,[]{}#&*!\|>'"%@\`` plus `-?:` followed by a space or alone matches the YAML 1.2 c-indicator rule, and the differential agrees on all 17 indicator probes. Quotes: a leading quote is rejected (stricter); an inner quote is accepted, as YAML does (`plugin's`). The reasons for not importing PyYAML hold. It is not in `requirements-dev.txt`, and `tests/test_gate_evidence.py:2057` and `tests/test_usage_report.py:391` ban `import yaml` in the shipped scripts. I checked independently with PyYAML 6.0.3 from the venv that the frontmatter parses (1c). The contract "parses the frontmatter as YAML" is met in substance: the reader together with the exact pins rejects every non-string or invalid form of the shipped value |
| 3e | Seat flag 2: line endings | ACCEPTED | The blobs are LF (`git ls-files --eol`: `i/lf`). The test normalises only `\r\n`, so a lone CR still fails. My CRLF clone is green unmodified (`find_defects` → `[]`), and Linux CI runs LF. Normalising cannot hide a CRLF blob, because no `.gitattributes` rule makes these files CRLF |
| 3f | Seat flag 3: the paragraph as one line | ACCEPTED | The ticket gives one string, and the test pins it as one line (`:208`). A hard wrap would add CommonMark soft breaks inside CJK text. No line-length rule in the suite objects (P1 and CI are green) |
| 3g | Seat flag 4: the extra mutation | ACCEPTED (S79-03 records the dispatch and ticket wording) | M1.9 is TDD 2's "description's last sentence removed": RED, restored |
| 3h | mypy | PASS | `mypy --strict --python-version 3.11 tests/test_entry_read_only_lookup.py`: "Success: no issues found", exit 0 |
| 4 | The boundary | PASS | I read the boundary with the repository's own `document_mutation_gate.read_boundary` from the ticket at `cp/wave3` `2f2f96e8` → `DECLARED`. `parse_raw_diff` of `git diff --raw -z --no-renames 69b4cdfb 12304e85` → `AGENTS.md` MODIFY, `SKILL.md` MODIFY, `tests/test_entry_read_only_lookup.py` CREATE. `evaluate_changes` → `(None, None)`. No forbidden path is touched |
| 5a | Receipt: P1 rerun | PASS, matches | Rerun at the candidate in my worktree: `4 failed, 218 passed, 9 skipped, 549 subtests`. The four failures are exactly the registered names in the dispatch. The receipt's P1 shows the same (`79-rev03-initial-P1.txt`) |
| 5b | Receipt: one mutation rerun | PASS, matches | R1 = M1.1: red, 11 failing tests, the defect naming the condition line |
| 5c | Receipt: E1 and P9 | PASS, with a note | E1 on the final `RETURN.md` with the candidate's gate: `cells=6 defects=0`, exit 0. E1 on `RETURN.as-returned.md`: same. P9 on `RETURN.as-returned.md`: `receipt defects: 0`, exit 0. Note: P9 on the final `RETURN.md` exits 1, because the 48-era `receipt_check.py` reads the USAGE cell the control plane appended as an evidence cell. That is a control-plane artefact after return, not a seat defect. The dispatch binds P9 to the receipt as returned |
| 5d | Receipt: CI, F1, STATEMENT | PASS, apart from S79-01 | `gh run view 45649388402`: headSha is the candidate, conclusion success, `test (windows)` and `test (linux)` both success. F1: 5 failed, exactly the registered base set, and `UNREGISTERED_FAILURE`/`REGISTERED_NOT_FAILING` appear 0 times. The STATEMENT's line numbers for items 1 to 3 are right; item 4 says "13 to 18" where it should be 13 to 20, and its "pins the unchanged five steps" is untrue (S79-01). The commit trailers name Claude Sonnet 5.5, which matches the dispatch `model` and the USAGE cell |
| 6 | Full suite | Not rerun | I took no host lock and started no full suite. The seat's F1 and CI run 45649388402, green on both jobs at the candidate, cover it. Because I ran no full suite, I did not need to check for an orphan lease |

### Commands (reviewer)

- `git show <rev>:<path>` and `R79-1_exact.py`: byte-exact texts and the PyYAML parse.
- `python -m pytest <p1_tests> -q -rfEs -p no:cacheprovider`: P1, one pytest at a time.
- `python -m mypy --strict --python-version 3.11 tests/test_entry_read_only_lookup.py`.
- `R79-1_mut.py`: 9 counter-mutations, the full new test file each time, plus the other P1 files for CM4.
- `R79-1_why.py`: `find_defects` messages per mutation, and the reader-against-PyYAML differential.
- `R79-1_boundary.py`: `document_mutation_gate` boundary evaluation.
- `receipt_check.py` (P9) and `evidence_gate.py` (E1), run on both receipt copies.
- `gh run view 45649388402 --json headSha,conclusion,jobs`.

Captures are kept beside this file: `79-rev03-initial-P1.txt`, `79-rev03-initial-counter-mutations.txt`, `79-rev03-initial-defects-and-yaml-differential.txt`, `79-rev03-initial-P9-as-returned.txt`, `79-rev03-initial-P9-final-receipt.txt`, `79-rev03-initial-E1.txt`.

### What the correction must show

- One additive commit on `cp/wave3-79-lookup`, without reset, amend or force.
- The five start-order step lines pinned exactly, with one injection case.
- CM4 and CM4b turn red with a defect that names the start-order steps.
- A rebuilt receipt with a true STATEMENT: the "pins the unchanged five steps" wording, and "lines 13 to 20".
- P1, T1, M1 (the new case added), CI on the new head, P9 and E1.

S79-02, S79-03 and S79-04 do not need to change on this branch.

### Residual risk and not verified

- I did not read the CI logs line by line. I relied on the "Compare failures with the registered list" step being success, and on the seat's F1 capture.
- I did not judge how a host's skill loader (Codex or Claude Code) treats the frontmatter beyond PyYAML's verdict.

```review-verdict
candidate: 12304e8557dfc92a7377c1657cdfc3986ba9cd94
verdict: CHANGES_REQUESTED
round: initial
closure_revision: revision03
reviewer: ticket-review seat R79-1 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 12304e8557dfc92a7377c1657cdfc3986ba9cd94
round: 1
kind: INITIAL
verdict: CHANGES_REQUESTED
causes: RETURN_UNTRUE
```

## Revision03 correction review

- **Candidate:** `74b637d5c7930570cbc29355c38b5bb3919de0b9`. It is one additive commit on top of `12304e85`, committed 2026-11-26 00:25 +0800. The trailer names Claude Sonnet 5.5.
- **Label:** correction review of closure revision03, the second and last review of this closure revision under `CodeReview.md` §5. Rule B applies.
- **Seat:** `ticket-review`, run id R79-2. Worktree `.worktrees/79-lookup-review`, detached at the candidate, porcelain empty.
- **Scope:** new defects were looked for only in `git diff 12304e85 74b637d5`.

**Verdict: `APPROVED`.** S79-01 is closed.
- The constant equals base `AGENTS.md` lines 12 to 18, byte for byte.
- My CM4 and CM4b are now red, for the intended reason. So are my three new counter-mutations.
- The STATEMENT is now true.
- The diff touches only the test file. It brings no new defect.
- S79-04 is closed: the control plane removed the file.
- S79-02 and S79-03 are `OUT_OF_SCOPE_HARDENING`. They do not block, and they go to the control plane as follow-ups.

### Closure of the initial findings

| id | status | evidence |
| --- | --- | --- |
| S79-01 | **CLOSED** | `check_agents` now compares `lines[heading + 4 : cursor]` with `START_ORDER_STEP_LINES` (`tests/test_entry_read_only_lookup.py:42-52, 205-211`). Constant against base: the 7 lines, UTF-8 encoded, equal `git show 69b4cdfb:AGENTS.md` lines 12 to 18, split on `\n`. Base lines 11 and 19 are blank, and the candidate's lines 12 to 18 equal the constant. Reruns in a CRLF `--no-hardlinks` clone, each with the full new test file and its unfiltered output: CM4, step 3 reworded, is red; CM4b, step 2 deleted, is red. Each gives the defect `the start order must keep its five steps exactly as they were (ticket item 1)` and turns `test_the_committed_texts_carry_the_rule` red. Two injection cases were added, `test_a_start_order_step_reworded_is_red` and `test_a_start_order_step_deleted_is_red`; both pass on the candidate. STATEMENT item 1 now reads "lines 13 to 20", and item 4 says the steps are pinned "word for word", both now true. M1.10 and M1.11 are CM4 and CM4b, both RED |
| S79-02 | Carried (`OUT_OF_SCOPE_HARDENING`, does not block) | Unchanged, as expected. Follow-up: make `" #"` and `": "` match a tab as well as a space in the reader, or note in the docstring that the reader together with the exact pin is what proves the value |
| S79-03 | Carried (`OUT_OF_SCOPE_HARDENING`, control plane) | Ticket and dispatch wording ("five cases" against eight TDD 2 bullets; M1 in the dispatch lacks one bullet). Nothing is open on the candidate |
| S79-04 | **CLOSED** | `C:/Temp/claude/jas79_edit.py` no longer exists (`ls` readback). The STATEMENT residue item says so |

### New findings in `12304e85..74b637d5`

None. The diff only does three things:
- it removes `STEP_LINE` and the last-step scan;
- it adds the constant and the exact block comparison, which keeps the early `return` that was there before;
- it adds two injection cases.

`mypy --strict` passes. The `while` loop still stops at the first blank line, so the anchor and paragraph checks after it keep their positions. All three new counter-mutations are red with the steps defect:
- CM9 appends a sixth step directly after step 5;
- CM10 rewords the continuation line of step 4;
- CM11 inserts a blank line inside step 3.

### Per-check table

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | CM4 and CM4b rerun | PASS, both red | `79-rev03-correction-counter-mutations.txt`. The unmodified CRLF clone gives `find_defects` → `[]`. Each mutation is restored with porcelain empty |
| 2 | Constant against base, byte for byte | PASS | Script `R79-2_const.py`, comparing `git show` blobs. `AGENTS.md` is byte-identical between `12304e85` and `74b637d5` |
| 3 | The diff touches only the test file | PASS | `git diff --name-status 12304e85 74b637d5`: `M tests/test_entry_read_only_lookup.py`. `git diff --check` is clean. Against base the change set is still the three boundary paths, so the initial boundary verdict stands |
| 4 | P1 rerun | PASS, matches | `4 failed, 220 passed, 9 skipped, 549 subtests`, exit 1. The four failures are the registered base names. That is 218 + 2 new cases, the same as the receipt's P1 (`79-rev03-correction-P1.txt`) |
| 5 | CI read back | PASS | `gh run view 45653704427`: headSha `74b637d5…`, conclusion success, `test (linux)` and `test (windows)` both success |
| 6 | STATEMENT true | PASS | Items 1 and 4 are as checked in S79-01. F1 lists 5 failures, exactly the registered base set, with 0 `UNREGISTERED_FAILURE`/`REGISTERED_NOT_FAILING`. M1 has 11 mutations, all RED. The CI run id and the residue claims are confirmed |
| 7 | Receipt gates | PASS | E1 with `--candidate 74b637d5`: `cells=6 defects=0`, exit 0, on both `RETURN.md` and `RETURN.as-returned.md`. P9 on `RETURN.as-returned.md`: `receipt defects: 0`, exit 0 (`79-rev03-correction-E1.txt`, `79-rev03-correction-P9-as-returned.txt`) |
| 8 | Full suite | Not rerun | No host lock was taken. The seat's F1 and both CI jobs cover it |

```review-verdict
candidate: 74b637d5c7930570cbc29355c38b5bb3919de0b9
verdict: APPROVED
round: correction
closure_revision: revision03
reviewer: ticket-review seat R79-2 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 74b637d5c7930570cbc29355c38b5bb3919de0b9
round: 2
kind: CORRECTION
verdict: APPROVED
causes:
```

## Seat token use (readiness criterion 5)

Host-reported usage per seat, summed per unique message id, against the expectation the owner confirmed on 2026-11-18 ("1A"); appended to the receipt as `USAGE` cells at integration.

| Seat | Model | input | cache write | cache read | output | processed | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seat:implementation-standard/JAS79R1` | claude-sonnet-5-5 | 174 | 318173 | 10405423 | 56767 | 10723770 | WITHIN |
| `seat:ticket-review/R79` | claude-opus-5-5 | 110 | 306938 | 6771202 | 50613 | 7078250 | WITHIN |
