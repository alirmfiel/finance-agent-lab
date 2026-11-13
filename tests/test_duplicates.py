from dataclasses import astuple
from datetime import date, timedelta
from decimal import Decimal

import pytest

from finance_tracker import FinanceTracker, Transaction


def entry(id, day=0, amount="10.0", type="income", description=""):
    return Transaction(id, Decimal(amount), date(2026, 1, 1) + timedelta(days=day),
                       type, description)


def tracker_with(*entries):
    tracker = FinanceTracker()
    for item in entries:
        tracker.add(item)
    return tracker


def test_four_argument_construction_defaults_description():
    item = Transaction("old", Decimal("10"), date(2026, 1, 1), "income")
    assert item.description == ""


@pytest.mark.parametrize("description", [None, 1, True, 1.5, [], {}, b"text"])
def test_invalid_description(description):
    with pytest.raises(ValueError):
        entry("a", description=description)


def test_empty_and_single_have_no_pairs():
    assert FinanceTracker().find_duplicates() == []
    assert tracker_with(entry("a")).find_duplicates() == []


@pytest.mark.parametrize("first,second", [
    (" Coffee  SHOP\t", "coffee\nshop"),
    ("Straße", "STRASSE"),
    ("", " \t\n"),
    ("", ""),
])
@pytest.mark.parametrize("type", ["income", "expense"])
def test_normalization_and_decimal_scale(first, second, type):
    tracker = tracker_with(entry("z", description=first, type=type),
                           entry("a", amount="10.00", description=second, type=type))
    assert tracker.find_duplicates() == [("z", "a")]


@pytest.mark.parametrize("changes", [
    {"amount": "10.01"}, {"type": "expense"}, {"description": "different"},
])
def test_different_content_does_not_match(changes):
    tracker = tracker_with(entry("a"), entry("b", **changes))
    assert tracker.find_duplicates(window_days=100) == []


@pytest.mark.parametrize("days,window,expected", [
    (0, 0, [("z", "a")]), (1, 0, []),
    (2, 2, [("z", "a")]), (3, 2, []),
])
@pytest.mark.parametrize("reverse", [False, True])
def test_inclusive_window_and_chronological_order(days, window, expected, reverse):
    first_day, second_day = (days, 0) if reverse else (0, days)
    tracker = tracker_with(entry("z", first_day), entry("a", second_day))
    assert tracker.find_duplicates(window) == expected


def test_three_entries_return_all_pairs_in_insertion_order():
    tracker = tracker_with(entry("z"), entry("a"), entry("m"))
    assert tracker.find_duplicates() == [("z", "a"), ("z", "m"), ("a", "m")]


def test_disjoint_groups_and_non_transitive_chain():
    tracker = tracker_with(entry("z", 4), entry("b", 1, description="other"),
                           entry("a", 0), entry("m", 2),
                           entry("c", 1, description="OTHER"))
    assert tracker.find_duplicates(2) == [("z", "m"), ("b", "c"), ("a", "m")]


@pytest.mark.parametrize("window", [True, False, -1, 1.0, "1", None, Decimal("1"), [], {}])
@pytest.mark.parametrize("populated", [False, True])
def test_invalid_window(window, populated):
    tracker = tracker_with(entry("a")) if populated else FinanceTracker()
    with pytest.raises(ValueError):
        tracker.find_duplicates(window)


def test_detection_preserves_fields_order_identity_and_balance():
    tracker = tracker_with(entry("z", description=" COFFEE\t"),
                           entry("a", amount="10.00", description="coffee"),
                           entry("expense", type="expense"))
    before = tracker.list_transactions()
    fields = [astuple(item) for item in before]
    balance = tracker.balance()
    result = tracker.find_duplicates()
    assert result == [("z", "a")]
    result.clear()
    after = tracker.list_transactions()
    assert [astuple(item) for item in after] == fields
    assert all(old is new for old, new in zip(before, after))
    assert tracker.balance() == balance == Decimal("10.00")
    assert tracker.find_duplicates() == [("z", "a")]


def test_extreme_calendar_dates_and_large_window():
    tracker = tracker_with(Transaction("max", Decimal("1"), date.max, "income"),
                           Transaction("min", Decimal("1"), date.min, "income"))
    assert tracker.find_duplicates(10**20) == [("max", "min")]
