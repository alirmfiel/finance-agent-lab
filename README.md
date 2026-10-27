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
There is no content-based duplicate detection: different IDs may have identical content.
Persistence, CLI, Issues and PRs are outside this baseline.

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
