# Ticket 80, closure revision02: initial code review

- **Candidate:** `7ec1f53997a95e6bed2d38d44580fde5b5145c80` on `cp/wave3-80-index`. It is two commits on base `acf813f6fdc81ba507a7247f0281fe37cfc31147`: `bf6544d2` (items 1 to 4 and 6) and `7ec1f539` (the repin and the eight registered rows). `git ls-remote origin refs/heads/cp/wave3-80-index` gives the candidate.
- **Ticket:** `modules/tickets/workflow-governance/80-lookup-through-the-index.md` revision02, read from `640ec852`. Its state row carries `dispatch=sha256:f63daf3a…19ea1`. Between `acf813f6` and `640ec852` the ticket changes only in its state row. `origin/cp/wave3` is now `461212b3`, and `640ec852..461212b3` touches none of the candidate's five files and not the ticket.
- **Dispatch:** `doc/handoffs/2026/workflow-governance/dispatch/JAS-80-1.yaml`. Its sha256 is `f63daf3a038b415f33939b0ac0ad560433541d92d75f812b372ea3366e819ea1`, both on disk and at `640ec852`.
- **Receipt:** `.worktrees/80-index-out/RETURN.md`. Above the control plane's USAGE cell, it differs from `RETURN.as-returned.md` by one blank line.
- **Publication commit:** `193777a7a8503d869c521425befc0d41ab323c28`.
- **Reviewer:** `ticket-review` seat, run id `R80-1` (claude-opus-5-5).
- **Label:** initial review of closure revision02, set before dispatch.
- **Process tier:** strict.
- **References applied:** `CodeReview.md` §2 to §5, and `review-checks.md`, including the defect categories and "Reviewer counter-mutation" points 1 to 5.
- **References not applicable**, each with its reason:
  - XSS: no browser, WebView or DOM input (ticket row).
  - Security boundary: no Secret, Log or Provider is touched; the publication repository receives no push.
  - Profile fan-out: one implementer, per the dispatch `profile:`.
  - POC/staging: none.

The reviewer modified nothing in the candidate and pushed, merged and tagged nothing. `refs/heads/publication-0.5.0` was not moved: it was read with `rev-parse`, `reflog` and `--verify-only`. The reviewer ran neither `claude` nor `codex`.

## Findings

| id | §4 class | severity | location | finding | evidence | smallest fix |
| --- | --- | --- | --- | --- | --- | --- |
| S80-01 | `OUT_OF_SCOPE_HARDENING` (row texts fixed by ticket item 2 and the owner decision "一起補"; the tie-break is in the item 3 sentence) | Low. It does not block: the owner's question resolves to one leaf, and every branch stays inside the index with no search | `AGENTS.md:72` (the 唯讀查詢 row); `AGENTS.md:24` (「同時符合 P0 列與其他列時取 P0 列」) | The 唯讀查詢 row's 情境 is 「唯讀查詢（文件內容、票的狀態、規則寫法）」. Read literally, it fits every rule lookup, and the tie-break settles a tie only in favour of a P0 row. So the 啟動順序 question and the target-sources question each fit two rows: the specific row and the 唯讀查詢 row. Read naturally, each still reaches one leaf. Read strictly, an agent could either take the 唯讀查詢 row, which leads to the lookup paragraph and back to the index, or call it 「索引有歧義」 and answer "not found". Both of those fail closed, and neither scans. The P0 question is not affected (check 2) | Hand walk in the per-check table, check 2 | Control plane, follow-up. Narrow the 唯讀查詢 row's 情境 to the lookup rule itself, for example 「唯讀查詢本身怎麼做（…）」. Or extend the tie-break: 「同時符合唯讀查詢列與其他列時取其他列」. Either way the owner's text changes, so the publication commit must be rebuilt again. If the owner wants it in 0.5.0, decide before release step 3 |
| S80-02 | `OUT_OF_SCOPE_HARDENING` (ticket item 2 says "the table's header and its other rows do not change"; item 4 does not ask the test to pin that) | Low | `tests/test_entry_read_only_lookup.py:262-281` (`check_index_rows`); module docstring `:20-21` | `check_index_rows` checks the five rows only at their positions, below the separator. A second 「P0 原始碼型別…」 row that contradicts the first, appended at the end of the table and linking `Workflow.md#tickets` and `language-policy.md`, leaves the lookup test green (CM5). Today the candidate is correct: `git diff acf813f6 7ec1f539 -- AGENTS.md` changes no other row. The only test that went red under CM5 is `test_l5_stale_candidate_pin_is_named_before_generation`, which fires on any uncommitted payload drift, and a regenerated pin would clear it. A smaller point: the docstring still says "a temporary copy of the two files", but `copy_texts` now copies six | `80-initial-mutations.txt`, section CM5: lookup file 54 passed, the P1 set `1 failed, 230 passed`, and that one failure is the l5 drift check | Follow-up hardening. Pin the whole 流程索引 table, from its header to the blank line, as a constant: the five rows followed by the base rows. Or require each 情境 cell to appear once. Say "the six files" in the docstring |
| S80-03 | `OUT_OF_SCOPE_HARDENING` (the dispatch `residue` rule; control plane) | Low | `.worktrees/80-index-scratch/edit_agents.py` (2460 B, 10:40) and `edit_cl.py` (888 B, 10:42) | Seat flag 1. The two one-shot edit scripts carry no run id, which goes against the dispatch rule "every other … carries your run id". The STATEMENT discloses them with the reason. I read both. They apply only the ticket's exact edits to `AGENTS.md` and `doc/HARNESS-CHANGELOG.md`, and they assert one match each. Nothing else is touched. This is the same shape as S79-04 | `cat` readback | The control plane removes both files after this review. No candidate change |
| S80-04 | `OUT_OF_SCOPE_HARDENING` (host lock practice; control plane) | Low (note) | STATEMENT, Tests item; `F1.started` 02:46:08Z | Seat flag 2. Shortly before the seat took the lock, a foreign pytest was running: pid 62456, `C:\Temp\codex\vd2-026-c10\…`, on the owner's Codex side, and it did not take the host lock. It ran in a different checkout, so the same-checkout runtime-root family (register C1/B2) does not apply. The F1 failure set is the one registered `test_acr2…` failure. CI ran the full suite on the candidate and both jobs are `success`. So the F1 evidence is not weakened. The STATEMENT names the process, as the F1 assert requires | `F1.txt` tail; CI run 45744238963 | None for this ticket. If host runs should exclude each other, the owner's Codex-side runs would have to take `jas-fullsuite.lock` too. That is a control-plane decision |

There are no `IMPLEMENTATION_DEFECT`, `EVIDENCE_DEFECT`, `TICKET_DEFECT` or `REQUIREMENT_CHANGED` findings.

## Per-check table

| # | check | result | evidence |
| --- | --- | --- | --- |
| 1a | The three anchors, each with its blank lines | PASS | Blob `7ec1f539:AGENTS.md`, which is LF with no CR. `startup-order` is at line 8, `p0-permissions` at 47 and `target-sources` at 108. Each has a blank line before and after it and its heading directly below, and each occurs once. The model anchor `p0-source-type` is at line 33 in the same shape. File: `80-initial-exact-texts.txt` |
| 1b | The five rows, exact and in order, directly below the separator | PASS | The rows were extracted from the ticket's `text` block at `640ec852`. They equal lines 72 to 76. The separator is line 71, and line 77 begins `| 任一事件` |
| 1c | The replaced sentence | PASS | The old sentence appears in the base and not in the candidate. The base paragraph with the old sentence replaced by the ticket's new text equals the candidate paragraph, which is still one line (line 24) |
| 1d | No other line of `AGENTS.md` changed | PASS | The base blob plus exactly the ticket's edits (three anchor inserts, five rows, one sentence) equals the candidate blob, byte for byte. `git diff acf813f6 7ec1f539 -- AGENTS.md` shows only those hunks |
| 2 | The owner's finding is closed (hand walk, index only, no search) | PASS, with S80-01 | **The P0 question, 「P0 原始碼型別的規定是什麼？」.** The user names no file, so read the 流程索引. Four rows fit: the P0 原始碼型別 row, the 唯讀查詢 row, the `TDD、strict type…` row and the `SPEC、ticket…type preflight` row. The tie-break picks the P0 row. Column 2 links `#p0-source-type` in this file, so the leaf is `## P0：原始碼型別` (lines 33 to 45). Exactly one leaf. **The 啟動順序 question, 「動手前要先讀什麼？」.** The 啟動順序 row links `#startup-order`, so the leaf is `## 啟動順序` (anchor at line 8, the five steps ending at line 20). That is one leaf when read naturally; S80-01 covers the literal overlap. **The target-sources question, 「target project 正式來源的標準位置在哪？」.** The target-sources row links `#target-sources`, so the leaf is `## Target project 正式來源` (lines 108 to 135). One leaf, with the same S80-01 note. Every link resolves in the shipped package. `pkg-R80-1/AGENTS.md` is identical to the candidate blob, and the four references are present. No step needs Workflow, Router or a search |
| 3a | The test: new constants and checks | PASS | `INDEX_SENTENCE` (`:104`) and `NO_SEARCH_SENTENCE` (`:109`) are in `REQUIRED_SENTENCES` (`:129`). `PARAGRAPH` (`:115`) has the new text. `ANCHORED_HEADINGS` (`:50`) and `INDEX_ROWS` (`:61`) are new. `check_anchored_headings` requires one occurrence, the blank lines and the heading. `check_index_rows` requires the header and separator, the five rows exactly at their positions, and the `| 任一事件` row after them. `link_defects` requires each `#name` to match exactly one `<a id>` line, a path to exist as a file under the root with no `..`, and no link to be empty. The diff's `-` lines are the old docstring line, the old sentence inside `PARAGRAPH`, the `check_agents` signature (it gains `root`) and the `copy_texts` file tuple. No existing check is removed. Three TDD 3 cases are present: a missing file is named, the separator removed is named, and an empty table is named |
| 3b | `copy_texts` copies the four references | PASS | `:399-403` iterates `(AGENTS, SKILL, *ROW_REFERENCES)`, and the four paths in `ROW_REFERENCES` (`:73-78`) are exactly the four the rows name. The unmodified copy stays green in every `assert_red` |
| 3c | Each TDD 2 case turns it red | PASS | Rerun by me in a disposable `--no-hardlinks` clone (`core.autocrlf false`), with the full test file, unfiltered output (no reducing wrapper), and `git checkout -- .` after each run with porcelain empty. The eight cases were: row 2 removed; rows 4 and 5 swapped; the rows below `| 任一事件`; `target-sources` removed; `p0-permissions` renamed `p0-perms`; `(#p0-source-type)` changed to `(#p0-source)`; the no-search sentence removed; the old sentence put back. All eight are RED, and in each `test_the_committed_texts_carry_the_rule` fails with the intended named defect. The other cases differ from the seat's M1 rows and anchors. File: `80-initial-mutations.txt` |
| 3d | Counter-mutations through other doors | PASS (CM1 to CM4 red); CM5 green is S80-02 | **CM1, the prefix door** on the one anchor the heading check does not cover: `p0-source-type` → `p0-source-type-x`. RED, and only `link_defects` names it: `the link (#p0-source-type) resolves to no single line`. **CM2**, the P0 row's column 2 linked to `Workflow.md#workflow-router`. RED, on both the exact row and "names no file under the root". **CM3**, a second `<a id="p0-source-type"></a>`. RED on the exactly-one rule. **CM4**, `security-boundary.md` deleted from the repository. RED in the lookup test, and also in the payload closure tests. **CM5**, a contradicting duplicate P0 row at the end of the table. The lookup test stays green; see S80-02 |
| 3e | `mypy --strict` (T1) | PASS | `Success: no issues found in 1 source file`, exit 0. mypy is 2.3.0 |
| 4a | Regenerate in a disposable clone | PASS | `git clone --no-hardlinks`, detached at the candidate. Before generating, I deleted `refs/remotes/origin/publication-0.5.0`, then ran `reflog expire` and `gc --prune=now`. `cat-file -e 193777a7` then fails, and so does `d355b4a2`, so the id was really regenerated, not found. Two runs with `--ref refs/heads/publication-0.5.0-r80` both print `publication commit 193777a7a8503d869c521425befc0d41ab323c28`, and porcelain stays empty. `--verify-only` on the r80 ref in the clone gives exit 0. File: `80-initial-rebuild.txt` |
| 4b | `--verify-only --ref refs/heads/publication-0.5.0` at the candidate | PASS | In the review worktree (candidate, porcelain empty) the output is `verified 193777a7…`, exit 0. `git show-ref refs/heads/publication-0.5.0-t80` prints nothing (exit 1). The reflog shows `d355b4a2` and then `193777a7` at `2026-11-26T10:42:39+08:00`, which equals the STATEMENT's 02:42:39Z |
| 4c | The extracted `193777a7` | PASS | `git archive` into an empty directory gives 149 files, the same count as `git ls-tree -r 193777a7`. `AGENTS.md` is identical to the candidate blob and holds all five rows. The new sentence appears once and the old one zero times. `plugin.json` says `software-factory` and `0.5.0`. There are 0 `.codex-plugin`, 0 of `install.ps1`, `johnny-install.cmd`, `johnny-router.ps1` and `requirements-runtime.lock`, and 0 paths under `library/local_orchestration`. The package marketplace copy is `"sha": "0000000000000000000000000000000000000000"` (line 15). The commit is parentless, with author and committer at time 0 |
| 4d | The eight registered reasons; no other byte | PASS | In the `acf813f6` blob of `ci/registered-failures.json`, `d355b4a2…` occurs 8 times. The base with that id replaced by `193777a7…` equals the candidate, byte for byte (84847 B each). The old id occurs 0 times in the candidate. `.claude-plugin/marketplace.json` changes in the same way: one id, byte-exact |
| 4e | The local marketplace equals the package | PASS | `diff -r pkg-R80-1 C:/Temp/claude/sf-050-local/plugins/software-factory` exits 0, with 149 files each side and no links. The sha256 values of the two marketplace files equal those in the STATEMENT (`92a9ab75…`, `72f4e770…`). Read only |
| 5 | Item 6: the changelog row and bullet | PASS | The row, extracted from the ticket, equals line 17, directly below the ticket 79 row, and occurs once. The bullet equals the last `- ` line of `### What to read instead` (line 37) |
| 6 | The boundary (`document_mutation_gate`) | PASS | `read_boundary` of the ticket at `640ec852` gives `DECLARED`. `parse_raw_diff` of `git diff --raw -z --no-renames acf813f6 7ec1f539` gives five MODIFY entries, all in `modify`, and `evaluate_changes` gives `(None, None)`. The same holds for each commit alone. The merge base with `640ec852` is `acf813f6`. File: `80-initial-boundary.txt` |
| 7a | P1 rerun | PASS | The four files at the candidate in the review worktree, with the anchor ref at `193777a7`: `240 passed, 892 subtests passed`, exit 0, the same counts as the receipt. In the clone without the shared ref (only the r80 ref): 240 passed |
| 7b | CI readback | PASS | Run 45744238963: `headSha` is the candidate, `headBranch` is `cp/wave3-80-index`, and the run conclusion and both jobs (`test (linux)`, `test (windows)`) are `success`. The full log has 14989 lines, the same count the STATEMENT gives, and 0 `UNREGISTERED_FAILURE` or `REGISTERED_NOT_FAILING`. File: `80-initial-C1.txt` |
| 7c | The STATEMENT's refresh commands and cache paths against item 5 | PASS | The Claude Code `uninstall` / `install … --scope local` commands in `C:\Temp\claude\sf-test-project`, the Codex `remove` / `add … --json` commands, the two cache paths with the `$CODEX_HOME` default, the `| P0 原始碼型別` check and the remove-and-reinstall fallback are word for word item 5. The two extra local-marketplace test commands are additions that the seat did not run. They are harmless |
| 7d | The rest of the receipt | PASS | The line numbers the STATEMENT cites match the files: `AGENTS.md` 8, 47, 108, 71 to 77 and 24; `HARNESS-CHANGELOG.md` 17 and 37; marketplace line 15; test constants `:50`, `:61`, `:104`, `:109`, `:115` and `:129`. The M1 claims match my 3c rerun. F1 is `1 failed, 3455 passed`, and the failure is the registered `test_acr2…`. E1 rerun by me: `cells=10 defects=0`, exit 0. Both commits are authored by `Johnny Liu <johnny.liu365@gmail.com>` with the trailer `Co-Authored-By: Claude Sonnet 5.5`, which matches dispatch `model: claude-sonnet-5-5`. The first commit's subject is the one the dispatch gives |
| — | Full suite | Not rerun | The check list does not require it. CI ran the whole suite on the candidate, on both OSes. When I looked, the host lock `C:/Temp/claude/jas-fullsuite.lock` was held by `jas77-r3` |

### Commands (reviewer)

- `git diff acf813f6 7ec1f539 -- AGENTS.md doc/HARNESS-CHANGELOG.md .claude-plugin/marketplace.json ci/registered-failures.json`
- `exact_R80-1.py`: byte comparison of the blobs at `acf813f6`, `7ec1f539` and the ticket at `640ec852`.
- In the clone, run twice: `python -m library.local_orchestration.plugin_publication --repo . --manifest .claude-plugin/plugin.json --marketplace .claude-plugin/marketplace.json --ref refs/heads/publication-0.5.0-r80`. Then `--verify-only` on the same ref.
- In the review worktree: the same module with `--verify-only --ref refs/heads/publication-0.5.0`.
- `git archive 193777a7… | tar -x`, then `grep`, `find`, `cmp` and `diff -r` against `C:/Temp/claude/sf-050-local/plugins/software-factory`.
- `boundary_R80-1.py`: `read_boundary`, `parse_raw_diff` and `evaluate_changes` from `library/local_orchestration/document_mutation_gate.py`.
- `mutate_R80-1.py`: thirteen mutations in the clone, run one after another, one pytest at a time.
- P1, then T1 (`mypy --strict --python-version 3.11`), one pytest at a time.
- `gh run view 45744238963 --json …` and `--log`.
- `evidence_gate.py` (E1) on the receipt.

### Residual risk and not verified

- I did not refresh the installed copies or check the two host cache copies. That is the owner's work after integration, and running `claude` or `codex` is not allowed.
- Ticket 77's lifecycle rerun with `--expected-publication 193777a7…` is control-plane work after integration.
- From 02:42:39Z until this ticket integrates, the four publication tests fail on this host in any checkout that still pins `d355b4a2`. This was announced, as item 5 says. If the ticket closes without integration, the restore command is in the STATEMENT.

```review-verdict
candidate: 7ec1f53997a95e6bed2d38d44580fde5b5145c80
verdict: APPROVED
round: initial
closure_revision: revision02
reviewer: ticket-review seat R80-1 (claude-opus-5-5)
reviewed_at: 2026-11-26
```

```rework-record
candidate: 7ec1f53997a95e6bed2d38d44580fde5b5145c80
round: 1
kind: INITIAL
verdict: APPROVED
causes:
```

## Seat token use (readiness criterion 5)

Host-reported usage per seat, summed per unique message id, against the expectation the owner confirmed on 2026-11-18 ("1A"); appended to the receipt as `USAGE` cells at integration.

| Seat | Model | input | cache write | cache read | output | processed | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seat:implementation-standard/JAS80R1` | claude-sonnet-5-5 | 168 | 144514 | 11235753 | 57553 | 11380435 | WITHIN |
| `seat:ticket-review/R80` | claude-opus-5-5 | 116 | 186438 | 7741829 | 47415 | 7928383 | WITHIN |
