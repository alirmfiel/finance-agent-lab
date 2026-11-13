"""Minimal in-memory personal finance tracker with explicit monetary types."""
from dataclasses import dataclass
from datetime import date as Date
from decimal import Decimal
from itertools import combinations


@dataclass(frozen=True)
class Transaction:
    id: str
    amount: Decimal
    date: Date
    type: str
    description: str = ""

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("ID must be a nonempty string")
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite() or self.amount <= 0:
            raise ValueError("Amount must be a positive finite Decimal")
        if type(self.date) is not Date:
            raise ValueError("Date must be a datetime.date, without a time")
        if self.type not in ("income", "expense"):
            raise ValueError("Type must be income or expense")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")


class FinanceTracker:
    def __init__(self):
        self._transactions: dict[str, Transaction] = {}

    def add(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise ValueError("Expected a Transaction")
        if transaction.id in self._transactions:
            raise ValueError("ID must be unique")
        self._transactions[transaction.id] = transaction

    def list_transactions(self) -> list[Transaction]:
        """Return a copy in insertion order."""
        return list(self._transactions.values())

    def balance(self) -> Decimal:
        """Return total income minus expenses using Decimal arithmetic."""
        return sum((item.amount if item.type == "income" else -item.amount
                    for item in self._transactions.values()), Decimal("0"))

    def find_duplicates(self, window_days: int = 0) -> list[tuple[str, str]]:
        """Return potential duplicate ID pairs in insertion order without mutation.

        Compare every pair directly using equal amounts, types, normalized
        descriptions, and an inclusive absolute calendar-day distance.
        """
        if isinstance(window_days, bool) or not isinstance(window_days, int) or window_days < 0:
            raise ValueError("Window days must be a nonnegative integer")

        entries = [
            (item, " ".join(item.description.casefold().split()))
            for item in self._transactions.values()
        ]
        return [
            (first.id, second.id)
            for (first, first_description), (second, second_description) in combinations(entries, 2)
            if first.amount == second.amount
            and first.type == second.type
            and first_description == second_description
            and abs((first.date - second.date).days) <= window_days
        ]
