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
