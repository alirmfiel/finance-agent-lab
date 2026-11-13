# Personal Finance Tracker

Minimal Python 3.10+ library for laboratory №2. Data lives in memory.

```python
from datetime import date
from decimal import Decimal
from finance_tracker import FinanceTracker, Transaction

tracker = FinanceTracker()
tracker.add(Transaction("salary", Decimal("1000.00"), date(2026, 10, 27), "income"))
tracker.add(Transaction("food", Decimal("25.50"), date(2026, 10, 27), "expense"))
print(tracker.list_transactions())
print(tracker.balance())  # Decimal('974.50')
```

IDs are nonempty, case-sensitive strings and must be unique in a tracker.
Amounts must be positive finite `Decimal` values (no floats or implicit conversion).
Dates must be `datetime.date` values; Python rejects impossible calendar dates.
Only `income` and `expense` types are accepted. Invalid input raises `ValueError`.
Transactions are immutable; the returned list is a copy in insertion order.
Balances use Python Decimal arithmetic and its active context.
Transactions accept an optional string `description` as the fifth argument or a
keyword, defaulting to `""`. Non-string descriptions raise `ValueError`.
Different IDs may have identical content and can still be added.

Use `tracker.find_duplicates(window_days=0)` to find potential repeated entries
without removing transactions or changing their fields, order, or balance.
It returns ID pairs in insertion order, with each unordered pair appearing once.
Pairs must have equal Decimal amounts and types, descriptions equal after
`" ".join(description.casefold().split())`, and dates at most `window_days`
calendar days apart (inclusive). Stored descriptions remain unchanged.
The default matches only the same date; the window must be a nonnegative integer
(booleans are rejected). Invalid windows raise `ValueError`.
Each pair is compared directly, so matches do not extend transitively.

```python
tracker.add(Transaction("food-copy", Decimal("25.500"), date(2026, 10, 28), "expense"))
print(tracker.find_duplicates(window_days=1))  # [('food', 'food-copy')]
```

Persistence and CLI are outside this library.

## Tests

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest -q
```

## Initial repository state

Verified `main` / `origin/main` before implementation:
[`e1ddaf973bdaf668f6a425f86cdabcaea23d09f1`](https://github.com/alirmfiel/finance-agent-lab/commit/e1ddaf973bdaf668f6a425f86cdabcaea23d09f1).
This initial commit is distinct from the prepared application baseline.
