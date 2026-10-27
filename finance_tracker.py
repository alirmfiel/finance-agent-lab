"""Minimal in-memory personal finance tracker with explicit monetary types."""
from dataclasses import dataclass
from datetime import date as Date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    id: str
    amount: Decimal
    date: Date
    type: str

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("ID must be a nonempty string")
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite() or self.amount <= 0:
            raise ValueError("Amount must be a positive finite Decimal")
        if type(self.date) is not Date:
            raise ValueError("Date must be a datetime.date, without a time")
        if self.type not in ("income", "expense"):
            raise ValueError("Type must be income or expense")


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
