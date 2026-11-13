# Duplicate Detection Implementation Plan

**Goal:** Implement Issue #2 without changing existing validation or tracker state.

**Architecture:** Append a validated description field to the frozen Transaction.
Compare each pair directly in insertion order using Decimal equality, type,
casefolded and whitespace-normalized descriptions, and absolute calendar-day distance.
Use an O(n²) scan with O(n) local preparation plus the returned pairs; no dependencies.

**Tech stack:** Python 3.10+, dataclasses, datetime, Decimal, pytest.

**Spec:** GitHub Issue #2. Its request to remove amount validation conflicts with
the acceptance criteria and is rejected; all baseline checks stay intact.
The user requested independent execution on the current experimental branch.

## Tasks

- [x] Run all 35 baseline tests before changes.
- [x] Add tests for default and invalid descriptions; empty/single trackers;
  normalization including Unicode, blank descriptions and Decimal scale;
  amount/type/description mismatches; inclusive and reversed date windows;
  deterministic pairs, disjoint groups and non-transitive chains;
  invalid windows on empty and populated trackers; unchanged fields/order/balance.
- [x] Run new tests against baseline and confirm missing-feature failures.
- [x] Add description validation and find_duplicates(window_days=0), rejecting
  bool, negative and non-integer windows before examining transactions.
- [x] Update README with the API, read-only behavior, ordering, and complexity.
- [x] Run the complete pytest suite and review the full diff against the issue.
- [ ] Commit, push experiment/issue-2, and open a PR against main with Closes #2.

## Review focus

Preserve all baseline validation; do not sort or mutate transactions; use absolute
date differences without date arithmetic overflow; compare pairs directly rather
than joining groups transitively; return insertion order regardless of ID spelling.

## Verification and review

Baseline: `.venv/bin/python -m pytest -q` — 35 passed.
New tests before implementation: 50 failed due to missing functionality.
Complete suite after implementation: 85 passed in 0.02s.
`git diff --check` passed. Independent final code review found no issues.
