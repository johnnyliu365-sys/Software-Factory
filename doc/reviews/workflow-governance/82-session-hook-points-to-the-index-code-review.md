# Ticket 82 — initial review of closure revision02

- Ticket: `modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md`, revision02, read from `origin/cp/wave3` at `9d17e0428f4a9655f8bbc7296cddc3520bc1eba6`. Its state row carries dispatch digest `669a489d…a38aa935f`. `JAS-82-1.yaml` at that commit hashes to that value.
- Candidate: `bea29f4b23b5f4d0281f582799cae9c78dcb2b05` (branch `cp/wave3-82-hook`). It is two commits on base `94acca3ad35ad629cf6d8fc0d48b80fdf9059fa9`:
  - `46264b9a` holds items 1 to 5 and 7;
  - `bea29f4b` holds the marketplace repin and the eight registered rows.
- Label: initial review, closure revision02. Process tier: strict.
- Reviewer: independent `ticket-review` seat, run id `R82-1`, worktree `.worktrees/82-hook-review` (detached at the candidate, porcelain empty before and after).
- Publication commit under review: `838bb3540960f1cbb3a086c411136766235277d5`.
- Applicable references: `CodeReview.md` §3 to §5, the ticket's items 1 to 7, TDD, defect table, 完成定義 (with A1) and boundary block, and ticket 80 item 5 (the rebuild procedure).
- Every capture named below is in this folder (`.worktrees/82-hook-review-out/`). The four scripts that produced them are copied here as `exact_texts.py`, `run_hook.py`, `boundary.py` and `counter_mutations.py`.

## Findings

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | No finding. Every item, every TDD 2 case, the rebuild and the receipt hold under independent rerun. | The per-check table below | — |

Notes. None of these is a finding, and none asks for a change.

- **N1.** The payload line's position (directly after `"Workflow.md",`) is pinned by A1, not by a test. My CM5 moved it to the end of `payload.files`. It went red only because the injection test's own guard ("the damage changed nothing") fired, not because a check reads the position. Item 5 asks only that the declaration list the file, and the position has no effect on what ships.
- **N2.** `check_hook_file` compares bytes after it replaces CRLF with LF. The module docstring says "byte for byte". The normalisation is needed: this host's system gitconfig sets `core.autocrlf=true`, so a fresh clone checks the file out as CRLF. The committed blob itself is LF-only, with one final line feed, and is byte-equal to item 1 (`exact-texts.txt`). K1 `cmp` pins the shipped bytes.
- **N3.** In `tests/test_entry_read_only_lookup.py`, the docstring addition "; ticket 82 adds `process-index` above `## 流程索引`" is wrapped across two lines. Its text is the ticket's text, whitespace aside.

## Per-check table

| # | Check | Result | Evidence and notes |
| --- | --- | --- | --- |
| 1a | Item 1: `hooks/hooks.json` byte for byte | PASS | `exact_texts.py` reads the JSON block of item 1 out of the ticket at `9d17e042` and strips the 3-space list indent. The candidate blob equals that text plus one LF: 548 bytes, no CR, mode 100644. The command is ASCII only, and the group has no `matcher` key. `exact-texts.txt` |
| 1b | Item 2: the payload line | PASS | `plugin.json` equals the base with exactly `      "hooks/hooks.json",` inserted after `      "Workflow.md",` (line 43). `payload.trees` is unchanged, and no `hooks` tree is present. |
| 1c | Item 3: the anchor in `AGENTS.md` | PASS | `AGENTS.md` equals the base with `<a id="process-index"></a>` and one blank line inserted before `## 流程索引`. Line 67 is blank, line 68 is the anchor, line 69 is blank and line 70 is the heading. This is the same shape as `p0-source-type`. Each of `process-index` and `read-only-lookup` stands exactly once. |
| 1d | Item 4: the README sentence | PASS | The sentence (taken from the ticket) appears once in the file, at line 165. It is its own paragraph and the last paragraph of `## 8. 它怎麼運作`, followed by a blank line and `## 9. 路線`. The README equals the base plus that sentence and a blank line. It holds no backtick, path or link. |
| 1e | Item 7: the changelog row and bullet | PASS | The row stands directly below the ticket 81 row (line 19). The bullet is the last bullet of `### What to read instead` (line 40). Both equal the ticket text, and the diff against the base holds only those two lines. |
| 1f | A1 | PASS | `git diff --unified=0 94acca3a bea29f4b -- AGENTS.md .claude-plugin/plugin.json` gives two hunks: the anchor line plus a blank line, and the payload line. The output is byte-identical to the receipt's `A1.txt`. `A1-review.txt` |
| 2a | The hook command, run by hand | PASS | `run_hook.py` reads the command from the candidate blob, substitutes `${CLAUDE_PLUGIN_ROOT}` and runs it in `C:\Program Files\Git\bin\bash.exe -c` (never a bare `bash`) and in Windows PowerShell 5.1.26100 (`powershell -NoProfile -NonInteractive -Command`). Four paths were used: forward-slash, backslash, a path with spaces (backslashes) and the same with forward slashes. All 8 runs give exit 0 and empty stderr. Each prints exactly the test's `EXPECTED_TEXT` with that path plus one line feed. Git Bash ends the line with LF, PowerShell with CRLF; the test normalises CRLF. `hook-run.txt` |
| 2b | The instruction is accurate against `AGENTS.md` | PASS | Both named anchors exist once in the candidate's `AGENTS.md`. The text limits itself to "a read-only question about one of those rules", which is the scope of the paragraph (本插件規則的查詢), so S82R-01 is not reopened. It defers the "how" to the paragraph, so the paragraph's other branches still govern: the exact-file case, the target project's own governance and the P0 limits. "Do not locate a rule with grep, a full-text search or by browsing files" matches 不以關鍵字搜尋（grep、全文搜尋）或逐檔瀏覽來找. |
| 2c | P0 question walked from the hook text only | PASS | Example: "may source code use `Any`?" The hook gives `<root>/AGENTS.md`, and the `read-only-lookup` paragraph sends it to the 流程索引. At `process-index`, the row "P0 原始碼型別（強型別、外部輸入、strict checker）" matches; the P0 row wins any tie. Its second column links `#p0-source-type`, a section of this file, so the leaf is `## P0：原始碼型別`. One route, no search. |
| 2d | "PRD 放哪" walked from the hook text only | PASS | Same entry path. Two rows could match: "target project 正式來源的標準位置" (row 5) and "PRD／CHG 建立、取代、封存" (row 11). The paragraph's tie-break takes the upper row, row 5. Its link `#target-sources` is a section of this file, whose list names `PRD.md`. One route, no search. |
| 3a | `tests/test_plugin_session_hook.py` against item 5 | PASS | Bash: on Windows it runs `CLAUDE_CODE_GIT_BASH_PATH`, else the Git Bash file, and skips with "Git Bash not found" when the file is absent; elsewhere it uses `shutil.which("bash")`. PowerShell: it is `skipUnless(win32)`, uses `[which("powershell"), "-NoProfile", "-NonInteractive", "-Command", cmd]`, and skips with "Windows PowerShell not found". The root is a temporary directory: forward slashes for bash, native separators for PowerShell. Each run asserts exit 0 and `stderr == b""`, then compares UTF-8 stdout with CRLF→LF against the expected text plus LF. The file also covers: `materialise_publication_tree(REPO, payload, <tmp>/tree)` writing byte-identical `hooks/hooks.json`; the README check (exactly once, own paragraph, last paragraph of section 8); both anchors (once each, `process-index` with its blank lines directly above the heading, a `-x` prefix anchor refused); and a missing or unparsable file, or a missing `AGENTS.md`, as a named defect. 28 tests pass, none skipped on this host. `hook-tests-verbose.txt` |
| 3b | `ANCHORED_HEADINGS` and `test_the_session_hook_is_carried` | PASS | The `("process-index", "## 流程索引")` entry sits between `p0-permissions` and `target-sources`. The docstring gains the ticket's clause (N3). `PayloadDeclarationTests.test_the_session_hook_is_carried(self) -> None` asserts the file is in `files` and `hooks` is not in `trees`. |
| 3c | TDD 2 cases are red (the seat's M1) | PASS | `M1.txt` holds seven blocks, each with a real `git diff` and an unfiltered pytest run of the five files, each `exit=1`, each restored with empty porcelain. The cases: (1) the payload line removed; (2) `pluginé` in the command; (3) `"matcher": "startup"`; (4) the anchor removed; (5) the anchor moved below the heading; (6) "locate" changed to "find"; (7) the README sentence removed. Each turns named tests of `test_plugin_session_hook.py` red. 4 and 5 also turn 33 entry-lookup tests red, and 1 also turns `test_the_session_hook_is_carried` red. In every block, the l5 publication test also fails, and 9 publication tests are skipped as "pin C is pending". Both happen in the clone, which lacks the local anchor ref, and l5 is a registered base failure. |
| 3d | My counter-mutations | PASS | `counter_mutations.py` ran in a disposable `--no-hardlinks` clone, keeping each file's own line ends; it ran the three hook, payload and lookup test files in full. CM1, `matcher: "startup"` only: red, 4 failed. CM2, `"shell": "powershell"` added: red, 3 failed. CM3, a second `process-index` anchor above the lookup paragraph: red, 61 failed, including `test_each_anchor_it_names_stands_once_in_the_rules_file`. CM4, the README sentence moved to the end of section 7: red, including `test_the_readme_sentence_is_the_last_paragraph_of_section_8`. CM5, the payload line moved to the end of `files`: red, but only via an injection test's guard (N1). CM6, the key order swapped: red on the byte check, JSON-equal. Porcelain was empty after each restore. `M1-review.txt` |
| 3e | P1 and T1 rerun | PASS | P1 (the five files, `-rfEs`): 286 passed, 904 subtests passed, exit 0, no skip. The local anchor ref names `838bb354`. `P1-review.txt` T1, `mypy --strict --python-version 3.11` (mypy 2.3.0) on the three files: "no issues found", exit 0. `T1-review.txt` Both match the receipt. |
| 4a | Rebuild in a disposable clone, `--ref refs/heads/publication-0.5.0-r82` | PASS | The generator ran twice at `bea29f4b`, and both runs print `publication commit 838bb3540960f1cbb3a086c411136766235277d5` and exit 0. Porcelain is empty after them. A third run at `46264b9a`, the commit the seat generated at, prints the same id and repins `6d04fa6d → 838bb354`. That gives exactly the one-line marketplace change of `bea29f4b`. The clone's ref names `838bb354`: a parentless commit with tree `e5595a92…`. The ref existed only in the clone, which was then removed. The clone was a CRLF checkout, and the id still matches. `G1-review.txt` |
| 4b | `--verify-only` on the shared ref | PASS | `verified 838bb3540960f1cbb3a086c411136766235277d5`, exit 0. The reflog of `refs/heads/publication-0.5.0` shows `6d04fa6d` at 12:20:09+08:00, then `838bb354` at 15:09:01+08:00 (07:09:01Z). That is the time the STATEMENT gives. No `-t82` or `-r82` ref remains in the shared repository. I did not move the ref. `V1-review.txt` |
| 4c | The extracted package | PASS | `git archive 838bb354` was extracted into an empty directory. `hooks/` holds only `hooks.json`, `cmp`-equal to the candidate blob. `AGENTS.md` has the anchor once (line 68, blanks at 67 and 69, heading at 70). `plugin.json` carries line 43, `software-factory` and `0.5.0`. Its own marketplace has forty zeros. It holds no `.codex-plugin`, none of the Level 2 files and nothing under `local_orchestration`. `K1-review.txt` |
| 4d | The eight registered rows | PASS | The base holds 8 occurrences of `6d04fa6d…`. The candidate file equals the base with each occurrence replaced by `838bb354…`, and no other byte differs; no OLD remains and there is no CR. The marketplace likewise differs only in the pin, 40 lower-case hex. `rows-review.txt` |
| 4e | The local marketplace plugin tree | PASS | `diff -r` of the package against `C:/Temp/claude/sf-050-local/plugins/software-factory` prints nothing. The sha256 of both marketplace files equals the receipt's before-and-after values (`92a9ab75…` and `72f4e770…`). `K1-review.txt` |
| 5 | The boundary (`document_mutation_gate`) | PASS | `read_boundary` of the ticket at `9d17e042` gives `DECLARED`: 2 create, 8 modify, 8 forbid. `parse_raw_diff` of `git diff --raw -z --no-renames` gives `(None, None)` from `evaluate_changes` for the whole range and for each commit alone. The range holds 2 `CREATE` and 8 `MODIFY`, and every changed file is in the block. A control `MODIFY Workflow.md` gives `PATH_FORBIDDEN`. `boundary-review.txt` |
| 6a | The receipt is true: P1, T1, A1, G1, V1, K1, L1 | PASS | My reruns match the receipt's numbers and ids: 3e, 1f, 4a to 4e. Every file and line number in STATEMENT item 2 was read back at the candidate and is correct. The commits are authored `Johnny Liu <johnny.liu365@gmail.com>` with a `Co-Authored-By: Claude Sonnet 5.5` trailer, which matches the dispatch model and USAGE. |
| 6b | The CRLF claim about M1 | PASS | The STATEMENT says the first attempt of mutations 1, 3 and 4 changed nothing because the clone is CRLF, and that those three were rerun. My first counter-mutation run hit the same trap in a fresh clone. The system gitconfig `C:/Program Files/Git/etc/gitconfig` sets `core.autocrlf=true`, and my edit assertion stopped on "mutation changed nothing". `M1.txt` holds exactly one block per mutation, each with a non-empty diff, so the reruns are the ones recorded. |
| 6c | CI read back | PASS | Run 45773219088: `headSha` is `bea29f4b…`, branch `cp/wave3-82-hook`, completed `success`. `test (linux)` and `test (windows)` both report `success`. The 14,987-line log has 0 `UNREGISTERED_FAILURE` or `REGISTERED_NOT_FAILING` lines, and no `FAILED` line names `test_plugin_session_hook`. Against base run 45772641725, Windows has +29 passed with the same 18 skips. So both shell cases ran on the Windows job, the PowerShell case included. Linux has +28 passed and +1 skip, which is the PowerShell case's `skipUnless(win32)`. `C1-review.txt`, `ci-counts.txt` |
| 6d | E1 rerun on the receipt with USAGE appended | PASS | `evidence_gate.py … --candidate bea29f4b …` gives `cells=11 defects=0`, exit 0. `E1-review.txt` |
| 6e | F1 | READ | Not rerun, because this review was not asked to. The capture shows 1 failed (`test_acr2_linux_requires_an_actual_linux_kernel_and_backend`, registered), 3566 passed and 13 skipped. That is a subset of the registered base failures. |
| 6f | Pushes | PASS (partial) | On `origin`, `cp/wave3-82-hook` names `bea29f4b`, `cp/wave3` names `9d17e042`, and no tag names this work. `ls-remote` of the publication repository answers "Repository not found" from this host. So "nothing pushed there" rests on that answer and on the local ref history, not on a listing. |

```review-verdict
candidate: bea29f4b23b5f4d0281f582799cae9c78dcb2b05
verdict: APPROVED
round: initial
closure_revision: revision02
reviewer: ticket-review seat R82-1 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: bea29f4b23b5f4d0281f582799cae9c78dcb2b05
round: 1
kind: INITIAL
verdict: APPROVED
causes:
```

## Not done here, and why

- **The full suite was not rerun.** It was not among the checks asked for. The receipt's F1 was read (6e).
- **The control plane's list after integration is unchanged and not done here.** It covers:
  - ticket 77's lifecycle rerun with `--expected-publication 838bb354…`;
  - the owner-assisted test: `/hooks` in a desktop session, the P0 and PRD questions with the files read, and whether Codex runs the hook and with which path;
  - ticket 77's cloud trigger;
  - the repin of the `agents` row in the work log, with `index_pins.py --check`.
- **Until this ticket integrates,** the publication tests on this host fail in any checkout that still pins `6d04fa6d`, because the shared ref has named `838bb354` since 07:09:01Z.
- **Residue.**
  - My scratch `.worktrees/82-hook-review-scratch/` (the clone `clone-R82-1-gen` with its `-r82` ref, the package `pkg-R82-1`, the CI log and the `_R82-1` scripts) was removed, together with the directory itself.
  - I did not touch the host lock, `refs/heads/publication-0.5.0`, the candidate, or the local marketplace.
  - PROCESSES_LEFT=0.

# Revision04 initial review

- **Ticket.** Revision04, read with `git show c263e6f7:modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md`. Its state row at `c3f4b700` carries the dispatch digest `5c60d9a3…5b3208`, and `JAS-82-2.yaml` from `c3f4b700` hashes to that value. Wording sources: the revision03 paragraph, S82R-12 to S82R-18 of the ticket-review record, and the REQ-043 row "放進 hook".
- **Candidate.** `b629db41624fce07298a110f5e6beedd6096f796`. It is two additive commits on `bea29f4b`:
  - `bdb942ff` holds the revision04 texts and tests;
  - `b629db41` holds the repin and the eight rows.
  - Both are authored `Johnny Liu <johnny.liu365@gmail.com>`, with a `Co-Authored-By: Claude Sonnet 5.5` trailer that matches the dispatch model and USAGE.
- **Label.** Initial review of closure revision04. It is a new closure revision, so the §5 count restarts. Process tier: strict.
- **Reviewer.** Independent `ticket-review` seat, run id `R82-2`, worktree `.worktrees/82-hook-review`, detached at the candidate, with porcelain empty before and after.
- **Publication commit.** `9cda3f9ef53389339f010a8a183c62dadbf3f5c9`.
- **Captures.** Every capture of this section is in `r04/` beside this file, with the scripts that produced it: `exact_texts_r04.py`, `run_hook_r04.py`, `counter_mutations_r04.py` and `boundary_r04.py`.

## Findings (revision04)

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S82-01 | `OUT_OF_SCOPE_HARDENING` | Low (non-blocking) | `.worktrees/82-hook-out/`; the residue item of the revision04 STATEMENT; `JAS-82-2.yaml` `residue_limit` | The seat moved the revision02 receipt and captures into `prev-r82b`, a directory carrying its new run id, and then removed it. Those files carried no revision04 run id: `RETURN.md` with the control plane's USAGE section, `P1.txt`, `M1.txt` and the rest. Fixed cell paths (`<out_dir>/P1.txt` …) force a correction round to overwrite the earlier captures, so the candidate is not affected. The revision02 raw blocks survive in `RETURN.as-returned.rev02.md`, which equals the revision02 receipt as returned (446480 bytes). Two things are lost. (1) The revision02 USAGE numbers are no longer recorded on disk. (2) The citations of `82-hook-out/*.txt` in this record's revision02 section now resolve to revision04 files. | STATEMENT residue item ("the previous round's captures prev-r82b (the revision02 receipt and captures, moved there out of 82-hook-out)"). `ls .worktrees/82-hook-out`. The revision02 USAGE values occur in no `.md` outside review worktrees (`grep -rl 9934582`). | No new mechanism. (a) For the record, the revision02 USAGE I read on 2026-11-26 before the correction was: seat `implementation-standard/JAS82R1`, `claude-sonnet-5-5`, effort high, input 152, cache write 190183, cache read 9934582, output 50727. The control plane can copy it next to `RETURN.as-returned.rev02.md`. (b) Revision02 evidence is read from `RETURN.as-returned.rev02.md`. (c) The next correction dispatch names where the previous round's receipt goes before the seat starts, for example `RETURN.revNN.md` made by the control plane. Carried to the control plane's dispatch practice; it does not block this candidate. |

Notes. None of these is a finding.

- **N4. The "777" figure (S82R-17).** 777 is the length of the text between the quotes with both `${CLAUDE_PLUGIN_ROOT}` placeholders unsubstituted (21 characters each). The printed text is 735 + 2 × len(path) characters plus a line feed:
  - 883 for the seat's scratch path, as its STATEMENT says;
  - 885 for a 75-character cache path such as `C:/Users/User/.claude/plugins/cache/software-factory/software-factory/0.5.0`;
  - 837 or 838 for my space paths.

  The figure appears only in the scope paragraph, as a size comparison against option A's 2 to 3 KB and the 10,000-character cap. It is not an exact text, no test reads it, and the candidate cannot be wrong against it. It is not a defect of the candidate. Saying "777 characters before substitution" is optional wording for the control plane's next touch of the ticket; it is not a blocking `TICKET_DEFECT`.
- **N5. The boundary per commit.** The boundary declares `hooks/hooks.json` and `tests/test_plugin_session_hook.py` as `create` only. `evaluate_changes` on the correction delta by itself (`bea29f4b..b629db41`, or `bdb942ff` alone) therefore gives `MODIFICATION_OUTSIDE_BOUNDARY` for `hooks/hooks.json`. The gate does not judge that range. `admit_document_mutation` diffs from `git merge-base <integration branch> <candidate>`, which is `94acca3a` for `cp/wave3` (`b70ad63d`). From there both files are `CREATE` and the range is admitted. This is expected for a branch that a correction round extends. It matters only if this branch were integrated in pieces, and it is not.
- **N6. My revision02 notes still hold.** N1 (the payload position is pinned only by A1), N2 (CRLF normalisation in the byte check) and N3 (the docstring wrap) are unchanged in this revision.

## Per-check table (revision04)

| # | Check | Result | Evidence and notes |
| --- | --- | --- | --- |
| R1a | `hooks/hooks.json` byte-exact, replaced in place | PASS | The blob equals the revision04 item 1 JSON block plus one LF: 961 bytes, no CR. Against `bea29f4b`, only the `"command"` line differs, and the line count is the same. The command is ASCII, has no matcher, and holds `${CLAUDE_PLUGIN_ROOT}` exactly twice. `r04/exact-texts.txt` |
| R1b | The tests' `COMMAND` and `EXPECTED_TEXT` | PASS | `COMMAND` (parsed with `ast.literal_eval`) equals the item 1 command. `EXPECTED_TEXT` equals the quoted text with both placeholders as `{root}`. Each is defined once, replaced in place. |
| R1c | The README section 8 sentence | PASS | The revision04 sentence appears once. It is its own paragraph and the last paragraph of section 8. Exactly one line differs from `bea29f4b`, and no revision02 sentence remains. It holds no backtick, path or link. It names the terminal for `/hooks` (S82R-15). |
| R1d | The changelog row and bullet | PASS | The row sits directly below the ticket 81 row and cites "A" and "放進 hook" (S82R-18). The bullet is the last bullet of `### What to read instead`. The file has exactly one ticket 82 row and one SessionStart bullet, and exactly two lines differ from `bea29f4b` (S82R-13). |
| R1e | Untouched files | PASS | Against `bea29f4b`, these are byte-identical: `skills/johnny-project-takeover/SKILL.md`, `AGENTS.md`, `.claude-plugin/plugin.json`, `tests/test_entry_read_only_lookup.py` (which holds the ticket 81 pins of the guard step) and `tests/test_plugin_payload_boundary.py`. README section 5 is identical at `94acca3a`, `bea29f4b` and `b629db41`. A1 (base to `b629db41`) is byte-identical to the receipt's `A1.txt`, with only the anchor lines and the payload line. `r04/A1-review.txt` |
| R2 | The new command run by hand | PASS | I ran it in `C:\Program Files\Git\bin\bash.exe -c` and in Windows PowerShell 5.1.26100 (`-NoProfile -NonInteractive -Command`) with four paths: forward-slash, backslash, backslash with spaces, and forward-slash with spaces. All 8 runs: exit 0, empty stderr. Each output equals the expected text with the path in both places (`path_count=2`), and no `CLAUDE_PLUGIN_ROOT` or `${` remains. Git Bash ends with LF, PowerShell with CRLF. The guard sentence agrees with `SKILL.md` step 1: same two conditions, same stop, removal commands in README section 5, a new session, nothing else. README section 5 does hold the Claude Code and Codex removal commands. `r04/hook-run.txt` |
| R3a | The S82R-16 cross-check test | PASS | `check_guard` requires exactly one line of `SKILL.md` that begins `1. Before anything else`. It requires each of `name begins with johnny-ai-skill:` and `file lies in a folder named johnny-ai-skill` exactly once in that line and exactly once in the command. A missing hook command or a missing `SKILL.md` is a named defect. `check_guard` is part of `hook_defects`, and the injection copy now carries five files. `test_the_guard_conditions_match_the_skill_step_word_for_word` checks the repository. Injection cases cover: the sentence removed, each condition changed in the command, a condition changed in `SKILL.md`, and `SKILL.md` missing. |
| R3b | My counter-mutations on `SKILL.md` only | PASS | Run in a disposable `--no-hardlinks` clone at `b629db41` (a CRLF checkout; line ends kept), with the three hook, payload and lookup test files in full. CM7, condition 1 changed in `SKILL.md` only (`its name begins with` to `its name starts with`): red. CM8, condition 2 changed in `SKILL.md` only (`folder` to `directory`): red. In both, `test_the_guard_conditions_match_the_skill_step_word_for_word` and `test_the_committed_hook_has_no_defect` fail. The ticket 81 pins of the guard step in `test_entry_read_only_lookup.py` also fail (60 or 61 failed in all). Porcelain was empty after each restore. `r04/M1-review.txt` |
| R4a | The seat's two new M1 mutations | PASS | `M1.txt` has nine blocks, each `exit=1` with a real diff. Mutation 8 removes the whole old-plugin sentence from the command: 11 failed, including the S82R-16 test, both shell tests and `test_the_old_plugin_sentence_removed_from_the_command_is_red`. Mutation 9 drops `-skill` from `folder named johnny-ai-skill` in the command: 10 failed, including the S82R-16 test. Mutations 1 to 7 repeat revision02 and are each red. In every block, the l5 publication test fails and 9 tests are skipped as "pin C is pending", because the clone has no local anchor ref; l5 is a registered base failure. |
| R4b | My own counter-mutations on the hook | PASS | CM9 drops the second placeholder (`section 5 of README.md`): red, 7 failed, including both shell tests and the byte check. CM10 changes `section 5` to `section 6`: red, 7 failed. `r04/M1-review.txt` |
| R5a | Rebuild in a disposable clone, `--ref refs/heads/publication-0.5.0-r82` | PASS | Two runs at `b629db41` each print `publication commit 9cda3f9ef53389339f010a8a183c62dadbf3f5c9`, exit 0, and leave porcelain empty. A third run at `bdb942ff` prints the same id and repins `838bb354 → 9cda3f9e`, which is exactly `b629db41`'s marketplace line. The clone's ref names a parentless commit with tree `42d1bdb7…`. The clone and its ref were removed. `r04/G1-review.txt` |
| R5b | `--verify-only` on the shared ref | PASS | `verified 9cda3f9ef53389339f010a8a183c62dadbf3f5c9`, exit 0. The reflog shows `838bb354` at 15:09:01+08:00, then `9cda3f9e` at 16:10:16+08:00 (08:10:16Z), as the STATEMENT says. No `-t82` or `-r82` ref is left in the shared repository. I did not move the ref. `r04/V1-review.txt` |
| R5c | The package, the rows and the local marketplace | PASS | `git archive 9cda3f9e`: `hooks/` holds only `hooks.json`, `cmp`-equal to the candidate blob, with the guard text `If this session also lists a skill whose name begins with johnny-ai-skill:` once. The package also has the anchor once and the revision04 README sentence once. Its `plugin.json` has line 43, `software-factory` and `0.5.0`, and its marketplace has forty zeros. It holds no `.codex-plugin`, no Level 2 files and nothing under `local_orchestration`. `ci/registered-failures.json` equals `bea29f4b`'s with the 8 occurrences of `838bb354` changed to `9cda3f9e` and nothing else; no OLD is left. The marketplace likewise differs only in the pin. `diff -r` of the package against `C:/Temp/claude/sf-050-local/plugins/software-factory` prints nothing. Both local marketplace files keep the sha256 values `92a9ab75…` and `72f4e770…`. `r04/K1-review.txt`, `r04/rows-review.txt` |
| R6 | The STATEMENT's cache check (S82R-12) | PASS | It tells the owner to look, in each host's `0.5.0` cache folder, for `hooks\hooks.json` holding the text `If this session also lists a skill whose name begins with johnny-ai-skill:`. A cache with no such file, or a file without that text, holds an earlier build, since `838bb354` already ships `hooks/hooks.json`. The owner then removes that host's `0.5.0` folder and installs again. That is item 6's wording, with both cache paths given. |
| R7 | The boundary (`document_mutation_gate`) | PASS | `read_boundary` of the ticket at `c3f4b700` gives `DECLARED`, with the same block as revision02. Merge-base range (`94acca3a..b629db41`, the range `admit_document_mutation` judges): 2 `CREATE` and 8 `MODIFY`, `(None, None)`. `b629db41` alone also gives `(None, None)`. The correction delta by itself is refused, as explained in N5. Controls: `Workflow.md` and `skills/johnny-project-takeover/SKILL.md` both give `PATH_FORBIDDEN`, and the candidate touches neither. `r04/boundary-review.txt` |
| R8a | P1 and T1 rerun | PASS | P1 (five files, `-rfEs`): 292 passed, 906 subtests passed, exit 0, no skip. T1: mypy 2.3.0 `--strict` on three files reports "no issues", exit 0. Both match the receipt. The hook test file alone has 34 passed and 0 skipped, both shell cases included. `r04/P1-review.txt`, `r04/T1-review.txt`, `r04/hook-tests-verbose.txt` |
| R8b | CI read back | PASS | Run 45780938741: `headSha` `b629db41…`, branch `cp/wave3-82-hook`, completed `success`, with `test (linux)` and `test (windows)` both `success`. The 14,985-line log has 0 `UNREGISTERED_FAILURE` or `REGISTERED_NOT_FAILING` lines and no `FAILED` line naming `test_plugin_session_hook`. Against run 45773219088 (`bea29f4b`), both jobs have +6 passed with unchanged skips (Windows 18, Linux 80). So the six new tests ran on both, and the PowerShell case still runs on the Windows job. `r04/C1-review.txt`, `r04/ci-counts.txt` |
| R8c | E1 and F1 | PASS / READ | E1 on the receipt with USAGE appended, `--candidate b629db41`: `cells=11 defects=0`, exit 0 (`r04/E1-review.txt`). F1 was read, not rerun: 1 failed (`test_acr2_linux_requires_an_actual_linux_kernel_and_backend`, registered), 3572 passed and 13 skipped, a subset of the registered base failures. |
| R8d | The rest of the receipt | PASS with S82-01 | The STATEMENT's numbers, ids, times, sizes (883 characters) and K1, L1 and A1 claims match my reruns. Its residue item is truthful, but it describes the removal recorded in S82-01. |

```review-verdict
candidate: b629db41624fce07298a110f5e6beedd6096f796
verdict: APPROVED
round: initial
closure_revision: revision04
reviewer: ticket-review seat R82-2 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: b629db41624fce07298a110f5e6beedd6096f796
round: 2
kind: INITIAL
verdict: APPROVED
causes:
```

## Not done here, and why (revision04)

- **The full suite was not rerun.** It was not asked for. F1 was read.
- **The control-plane list after integration is unchanged and not done here.** It covers ticket 77's rerun with `9cda3f9e`, the owner-assisted test (including the two-versions case as a plain question), ticket 77's cloud trigger, and the `agents` repin with `index_pins.py --check`.
- **Until this ticket integrates,** the publication tests on this host fail in any checkout that pins `838bb354` or `6d04fa6d`.
- **Residue.**
  - My scratch `.worktrees/82-hook-review-scratch/` was removed, including the clone `clone-R82-2` with its `-r82` ref, the package `pkg-R82-2`, the CI log and the `_R82-2` scripts.
  - I did not touch the host lock, `refs/heads/publication-0.5.0`, the candidate, the receipt or the local marketplace.
  - PROCESSES_LEFT=0.

## Control-plane note on S82-01 (2026-11-26)

The seat removed the revision02 receipt with the control plane's appended USAGE section in it. The revision02 round's seat use, as the reviewer recovered it, was claude-sonnet-5-5, effort high: input 152, cache write 190183, cache read 9934582, output 50727. From the next correction on, the dispatch names where the previous round's receipt goes before the seat starts.

# Revision06 initial review

- **Ticket.** Revision06, read with `git show 44018a0b:modules/tickets/workflow-governance/82-session-hook-points-to-the-index.md`. Its state row at `5769c0d8` carries the dispatch digest `d0eea2ec…507d70`, and `JAS-82-3.yaml` from `5769c0d8` hashes to that value. The boundary block is unchanged since revision02.
  - Wording sources: S82R-19 to S82R-25 of the ticket-review record, and the REQ-043 rows for items 4b ("Codex asks to trust the plugin hook") and 4c ("併進票 82").
- **Candidate.** `4be37a7aa52ea77bd12ff4dbecac1d0296eab88e`. It is two additive commits on `b629db41`:
  - `6c4cb7e1` holds the two README paragraphs, the tests and the changelog row;
  - `4be37a7a` holds the repin.
  - Both are authored `Johnny Liu <johnny.liu365@gmail.com>`, with a `Co-Authored-By: Claude Sonnet 5.5` trailer that matches the dispatch model and USAGE (`seat:implementation-standard/JAS82R3`).
- **Label.** Initial review of closure revision06. It is a new closure revision, so the §5 count restarts. Process tier: strict.
- **Reviewer.** Independent `ticket-review` seat, run id `R82-3`. The worktree `.worktrees/82-hook-review` was detached from `b629db41` to the candidate, with porcelain empty before and after.
- **Publication commit.** `3ab86d439f236880db92648ab28724a626dc360b`.
- **Captures.** Every capture is in `r06/` beside this file, with the scripts that produced it: `exact_texts_r06.py`, `counter_mutations_r06.py` and `boundary_r06.py`.

## Findings (revision06)

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | No finding. Every item, every TDD 2 case, the rebuild and the receipt hold under independent rerun. | The per-check table below | — |

Notes. None of these is a finding.

- **N7. S82-01 is closed in practice.** The seat copied the whole revision04 out directory to `.worktrees/82-hook-out-rev04` before it changed anything. That copy holds `RETURN.md` with its USAGE section and every revision04 capture. Its `RETURN.as-returned.md` is byte-identical to `82-hook-out/RETURN.as-returned.rev04.md`. The revision04 section of this record should be read against `82-hook-out-rev04/`.
- **N8. The seat's bare `bash -c` slip does not touch any evidence.**
  - A Python `subprocess` call of a bare `bash` on Windows resolves through the CreateProcess search order to `C:\Windows\System32\bash.exe`, the WSL launcher, before `PATH`. On this host the only WSL distribution is `docker-desktop`. The WSL VM has been running since 2026-11-19, so the slip did not start it.
  - There is no non-Git `bash.exe` process and no `r82c` process now.
  - The helper ran one read-only `grep` under scratch, and its output was discarded.
  - The K1 capture is valid UTF-8 with no CR. Its `grep -n -o` line gives README lines 79 and 107, which I confirmed on the candidate.
  - Every K1 fact is reproduced by my own K1, run in Git Bash (R4c).
  - The S82R-03 rule governs the test's bash case. That case is unchanged and still selects the Git Bash file.
- **N9. The test's character check reads the constants.** `test_neither_new_paragraph_holds_code_a_path_or_a_link` and the check in `_check_placed_paragraph` test the constants, not the README text. This is equivalent, because the README line must equal the constant exactly. Accordingly, the injection "path character" case goes red as "not found", not on the character rule.

## Per-check table (revision06)

| # | Check | Result | Evidence and notes |
| --- | --- | --- | --- |
| R1a | `git diff b629db41 4be37a7a`: what changes | PASS | Changed: `README.md`, `tests/test_plugin_session_hook.py`, `doc/HARNESS-CHANGELOG.md`, `.claude-plugin/marketplace.json` and `ci/registered-failures.json`. Byte-identical to `b629db41`: `hooks/hooks.json`, `skills/johnny-project-takeover/SKILL.md`, `AGENTS.md`, `plugin.json` and both other test files. The README delta is exactly the two paragraphs, each with one blank line. README equals `b629db41` with those two insertions. Section 8 is identical. Section 4's numbered steps 1 to 5 are unchanged. Ticket 81's two section 5 paragraphs (`新舊兩版同時裝著時…` and `在 Claude Code 2.1.332 上…`) are unchanged and each appears once. `r06/exact-texts.txt` (`exact_texts_r06.py`) |
| R1b | The changelog row | PASS | The row is byte-exact to revision06 item 7, directly below the ticket 81 row. The file has exactly one ticket 82 row, and exactly one line differs from `b629db41` (replaced in place, S82R-25). The bullet is unchanged and still last. |
| R2 | Items 4b and 4c byte-exact and placed | PASS | Both paragraphs, taken from the ticket, appear exactly once in the README. 4b sits in `## 4. 安裝：Codex`. The three lines before it are `codex plugin list --marketplace software-factory --json`, ```` ``` ```` and a blank line. The two lines after it are a blank line and `5. 要移除時，先移除 plugin，再移除 marketplace：`. 4c sits in `## 5.`. The three lines before it are `claude plugin marketplace remove johnny-ai-skill`, ```` ``` ```` and a blank line. The two lines after it are a blank line and exactly `Codex：`. Neither paragraph holds `` ` ``, `](`, `/` or `\`. The tests' `CODEX_TRUST_PARAGRAPH` and `SCOPE_PARAGRAPH` equal 4b and 4c. The README has no CR. |
| R3a | The seat's two new M1 mutations | PASS | `M1.txt` has 11 blocks, and each is `exit=1`. Mutation 10 removes the trust paragraph: 5 failed, including `test_the_codex_trust_and_scope_paragraphs_stand_at_their_places` and `test_the_codex_trust_paragraph_removed_is_red`. Mutation 11 removes the scope paragraph: 6 failed, including the same placement test and `test_the_scope_paragraph_removed_is_red`. The other failure in each block is the registered l5 test in the clone. |
| R3b | My counter-mutations | PASS | Run in a disposable `--no-hardlinks` clone at `4be37a7a` (a CRLF checkout; line ends kept), with the three hook, payload and lookup test files in full. CM11 adds one character to 4b (`請選信任` to `請選擇信任`): red, 4 failed. CM12 moves 4c below the Codex removal block of section 5: red, 6 failed, including ticket 81's three section 5 tests in `test_plugin_payload_boundary.py`. CM13 removes the blank line after 4b: red, 5 failed. CM14 adds a second copy of 4c at the end of section 6: red, 3 failed. Porcelain was empty after each restore. `r06/M1-review.txt` (`counter_mutations_r06.py`) |
| R4a | Rebuild in a disposable clone, `--ref refs/heads/publication-0.5.0-r82c` | PASS | Two runs at `4be37a7a` each print `publication commit 3ab86d439f236880db92648ab28724a626dc360b`, exit 0, and leave porcelain empty. A third run at `6c4cb7e1` prints the same id and repins `9cda3f9e → 3ab86d43`, which is exactly `4be37a7a`'s marketplace line. The clone's ref names a parentless commit with tree `9277f3e8…`. The clone and its ref were removed. `r06/G1-review.txt` |
| R4b | `--verify-only` on the shared ref | PASS | `verified 3ab86d439f236880db92648ab28724a626dc360b`, exit 0. The reflog shows `9cda3f9e` at 16:10:16+08:00, then `3ab86d43` at 17:10:07+08:00 (09:10:07Z), as the STATEMENT says. No `-t82` or `-r82*` ref is left in the shared repository. I did not move the ref. `r06/V1-review.txt` |
| R4c | The package, the rows and the local marketplace | PASS | `git archive 3ab86d43` gives a package that holds both paragraphs once each (lines 79 and 107). Its README equals the candidate's byte for byte. Its `hooks/hooks.json` is `cmp`-equal to `9cda3f9e`'s and to the candidate's. `git diff 9cda3f9e 3ab86d43` is README only, with +4 lines. The package also has the anchor once, `plugin.json` line 43, `software-factory` and `0.5.0`, and forty zeros in its marketplace. It holds no `.codex-plugin`, no Level 2 files and nothing under `local_orchestration`. `ci/registered-failures.json` equals `b629db41`'s with the 8 occurrences of `9cda3f9e` changed to `3ab86d43` and nothing else; the marketplace likewise differs only in the pin. `diff -r` of the package against `C:/Temp/claude/sf-050-local/plugins/software-factory` prints nothing, and both local marketplace files keep their sha256 values. A1 is byte-identical to the receipt's. `r06/K1-review.txt`, `r06/rows-review.txt`, `r06/A1-review.txt` |
| R5 | The STATEMENT's cache check (S82R-19) | PASS | It tells the owner to look, in each host's `0.5.0` cache folder, in `README.md` for a line that begins `上面的 uninstall 指令針對裝在 user 範圍的舊版`, and it gives both cache paths. A cache without that line holds an earlier build, since `9cda3f9e` already ships the hook with the old-plugin sentence. The owner then removes that host's `0.5.0` folder and installs again. That is item 6's revision06 wording. |
| R6 | The boundary (`document_mutation_gate`) | PASS | `read_boundary` of the ticket at `5769c0d8` gives `DECLARED`. The merge-base range (`94acca3a..4be37a7a`, with `cp/wave3` at `d83a2c17`) gives 2 `CREATE` and 8 `MODIFY`, `(None, None)`. `4be37a7a` alone also gives `(None, None)`. As in N5, the correction delta by itself is refused, here on `tests/test_plugin_session_hook.py`, but the gate does not judge that range. The `Workflow.md` and `SKILL.md` controls give `PATH_FORBIDDEN`. `r06/boundary-review.txt` |
| R7a | P1 and T1 rerun, under the host lock | PASS | I held the host lock `C:/Temp/claude/jas-fullsuite.lock` as `R82-3`: acquired by `mkdir` at 09:56:57Z, released by rename and remove after `owner.txt` was checked. P1 (five files, `-rfEs`): 298 passed, 914 subtests passed, exit 0, no skip. T1: mypy `--strict` on three files reports "no issues", exit 0. The hook test file alone has 40 passed and 0 skipped. All match the receipt. My counter-mutation runs also ran under the lock. `r06/P1-review.txt`, `r06/T1-review.txt`, `r06/hook-tests-verbose.txt` |
| R7b | CI read back | PASS | Run 45789512934: `headSha` `4be37a7a…`, branch `cp/wave3-82-hook`, completed `success`, with `test (linux)` and `test (windows)` both `success`. The 14,989-line log has 0 `UNREGISTERED_FAILURE` or `REGISTERED_NOT_FAILING` lines and no `FAILED` line naming `test_plugin_session_hook`. Against run 45780938741 (`b629db41`), both jobs have +6 passed with unchanged skips (Windows 18, Linux 80). `r06/C1-review.txt`, `r06/ci-counts.txt` |
| R7c | E1 and F1 | PASS / READ | E1 on the receipt with USAGE, `--candidate 4be37a7a`: `cells=11 defects=0`, exit 0 (`r06/E1-review.txt`). F1 was read, not rerun: 1 failed (`test_acr2_linux…`, registered), 3578 passed and 13 skipped. |
| R7d | The rest of the receipt | PASS | The STATEMENT's ids, the move time, the eight rows, V1, K1, L1 and A1 match my reruns. Its residue item names the preserved `82-hook-out-rev04` (N7) and reports the slip truthfully (N8). |

```review-verdict
candidate: 4be37a7aa52ea77bd12ff4dbecac1d0296eab88e
verdict: APPROVED
round: initial
closure_revision: revision06
reviewer: ticket-review seat R82-3 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 4be37a7aa52ea77bd12ff4dbecac1d0296eab88e
round: 3
kind: INITIAL
verdict: APPROVED
causes:
```

## Not done here, and why (revision06)

- **The full suite was not rerun.** It was not asked for. F1 was read.
- **The control-plane list after integration is unchanged and not done here.** It covers ticket 77's rerun with `3ab86d43`, the owner-assisted test (Codex with the hook trusted, and the two-versions case in both hosts), ticket 77's cloud trigger, and the `agents` repin with `index_pins.py --check`.
- **Until this ticket integrates,** the publication tests on this host fail in any checkout that pins an earlier id.
- **Residue.**
  - My scratch `.worktrees/82-hook-review-scratch/` was removed, including the clone `clone-R82-3` with its `-r82c` ref, the package `pkg-R82-3`, the CI log and the `_R82-3` scripts.
  - The host lock I took was released; it is absent now.
  - I did not touch `refs/heads/publication-0.5.0`, the candidate, the receipt, `82-hook-out-rev04` or the local marketplace.
  - PROCESSES_LEFT=0.

## Seat token use (readiness criterion 5)

Host-reported usage per seat, summed per unique message id, against the expectation the owner confirmed on 2026-11-18 ("1A"); appended to the receipt as `USAGE` cells at integration.

| Seat | Model | input | cache write | cache read | output | processed | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seat:implementation-standard/JAS82R3` | claude-sonnet-5-5 | 346 | 736328 | 33201482 | 117648 | 33938156 | OVER_PROCESSED |
| `seat:ticket-review/R82` | claude-opus-5-5 | 240 | 797057 | 23523699 | 118491 | 24320996 | OVER_OUTPUT,OVER_PROCESSED |

**Control-plane note on the usage verdicts (2026-11-26).** Each of the two seats ran three rounds of this ticket by resumption: the implementation seat for revisions 02, 04 and 06, and the review seat for the initial reviews of revisions 02, 04 and 06. The host transcript sums all three, so each row is a three-round total against a one-round expectation. The implementation seat's revision04 receipt recorded 20,274,328 cache-read tokens at its return, so revision06 alone added about 12.9 million processed tokens, within one round's expectation. Every round was a new closure revision after an owner decision ("放進 hook", "併進票 82") or a delta review, not rework of a refused candidate. The rework report shows this as three rounds with empty causes. REQ-044 T13 to T15 aim at this cost.
