from datetime import date, datetime
from decimal import Decimal

import pytest

from finance_tracker import FinanceTracker, Transaction


def transaction(**changes):
    values = dict(id="one", amount=Decimal("10.10"), date=date(2026, 10, 27), type="income")
    values.update(changes)
    return Transaction(**values)


def test_empty_tracker():
    tracker = FinanceTracker()
    assert tracker.list_transactions() == []
    assert tracker.balance() == Decimal("0")
    assert isinstance(tracker.balance(), Decimal)


def test_add_list_and_exact_balance():
    tracker = FinanceTracker()
    first = transaction(amount=Decimal("0.1"))
    second = transaction(id="two", amount=Decimal("0.2"))
    third = transaction(id="three", amount=Decimal("0.05"), type="expense")
    for item in (first, second, third):
        tracker.add(item)
    assert tracker.list_transactions() == [first, second, third]
    assert tracker.balance() == Decimal("0.25")


def test_duplicate_id_rejected_without_changing_state():
    tracker = FinanceTracker()
    first = transaction()
    tracker.add(first)
    with pytest.raises(ValueError, match="ID"):
        tracker.add(transaction(type="expense"))
    assert tracker.list_transactions() == [first]


def test_equal_content_with_distinct_ids_is_allowed():
    tracker = FinanceTracker()
    tracker.add(transaction())
    tracker.add(transaction(id="two"))
    assert len(tracker.list_transactions()) == 2
    assert tracker.balance() == Decimal("20.20")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("sNaN"), Decimal("Infinity"), Decimal("-Infinity"), 1, 0.1, "1", None, True])
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        transaction(amount=amount)


@pytest.mark.parametrize("value", ["", "  ", 1, None])
def test_invalid_id(value):
    with pytest.raises(ValueError):
        transaction(id=value)


@pytest.mark.parametrize("value", ["transfer", "Income", "", None, 1, []])
def test_invalid_type(value):
    with pytest.raises(ValueError):
        transaction(type=value)


@pytest.mark.parametrize("value", ["2026-02-30", "2026-10-27", None, datetime(2026, 10, 27), 1])
def test_invalid_date(value):
    with pytest.raises(ValueError):
        transaction(date=value)


def test_valid_leap_day():
    assert transaction(date=date(2024, 2, 29)).date == date(2024, 2, 29)


def test_returned_list_cannot_modify_tracker():
    tracker = FinanceTracker()
    tracker.add(transaction())
    tracker.list_transactions().clear()
    assert len(tracker.list_transactions()) == 1


def test_transaction_is_immutable():
    from dataclasses import FrozenInstanceError
    item = transaction()
    with pytest.raises(FrozenInstanceError):
        item.id = "changed"


def test_add_rejects_non_transaction():
    with pytest.raises(ValueError):
        FinanceTracker().add({})


def test_expense_can_make_balance_negative():
    tracker = FinanceTracker()
    tracker.add(transaction(type="expense"))
    assert tracker.balance() == Decimal("-10.10")
