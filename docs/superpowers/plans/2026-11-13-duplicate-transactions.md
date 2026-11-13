# Duplicate Transactions Implementation Plan

**Goal:** Implement GitHub Issue #1 independently on `experiment/issue-1` from baseline `4ac8e518e8938b86073fa386b68de51946fe78a6`.

**Spec:** https://github.com/alirmfiel/finance-agent-lab/issues/1

**Architecture:** Keep the frozen Transaction dataclass and insertion-ordered tracker dictionary. Add a validated optional description. Compare unordered pairs directly in insertion order, using equal Decimal amounts/types, casefolded whitespace-normalized descriptions, and inclusive absolute calendar-day distances. A nested pair scan is simple, deterministic, and avoids transitive matching; no indexing or dependencies are necessary.

**Constraints:** Preserve all baseline validation, four-argument construction, stored values/order/balance, and project layout. No runtime dependencies, CLI, persistence, main-branch changes, or merge.

## Tasks

- [x] Run the unchanged baseline suite (35 tests).
- [x] Add `tests/test_duplicates.py` with exact expected pairs for empty/single trackers, default same-day matching, normalization including Unicode casefold, blank descriptions, Decimal scale, amount/type/description mismatches, inclusive windows, reverse date insertion, three-way matches, disjoint groups, and non-transitive chains.
- [x] Test invalid descriptions and windows, four-argument construction, unchanged objects/fields/order/balance, returned-result independence, and preserved validation via the unchanged baseline tests.
- [x] Run new tests before implementation and confirm missing-feature failures.
- [x] Add `description: str = ""` plus ValueError validation and `find_duplicates(window_days: int = 0) -> list[tuple[str, str]]` in `finance_tracker.py`.
- [x] Update README with optional description, duplicate detection, ordering, validation, and non-mutating behavior.
- [x] Run the complete pytest suite. Review the diff against every issue requirement, retaining every baseline test.
- [ ] Commit and push the current experimental branch, then create a PR against main containing `Closes #1` and actual test command/results.

## Review focus

Check booleans and invalid windows even for empty trackers; absolute date distance across month/year boundaries and extreme dates; Unicode casefold versus lower; pair order by insertion rather than ID/date; no transitive matching or mutation.

## Execution record

User explicitly requested independent execution on the current experimental branch; work proceeds in that checkout without approval handoffs.

Verification: unchanged baseline `.venv/bin/python -m pytest -q` → 35 passed; new tests before implementation → 43 failed due to missing feature; complete suite after implementation → 78 passed. `git diff --check` passed. Baseline test file unchanged.
