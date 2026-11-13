from dataclasses import asdict
from datetime import date
from decimal import Decimal

import pytest

from finance_tracker import FinanceTracker, Transaction


def entry(id, **changes):
    fields = dict(amount=Decimal("10.0"), date=date(2026, 1, 1), type="income")
    fields.update(changes)
    return Transaction(id=id, **fields)


def tracker_with(*items):
    tracker = FinanceTracker()
    for item in items:
        tracker.add(item)
    return tracker


def test_empty_and_single_trackers():
    assert FinanceTracker().find_duplicates() == []
    assert tracker_with(entry("one")).find_duplicates() == []


def test_four_argument_construction_and_default_same_day_match():
    first = Transaction("z", Decimal("10.0"), date(2026, 1, 1), "income")
    assert first.description == ""
    tracker = tracker_with(first, entry("a", amount=Decimal("10.00")),
                           entry("next", date=date(2026, 1, 2)))
    assert tracker.find_duplicates() == [("z", "a")]


@pytest.mark.parametrize("left,right", [
    ("  Coffee\t SHOP\n", "coffee shop"),
    ("Straße", "STRASSE"),
    ("", " \t\n"),
])
def test_description_normalization(left, right):
    tracker = tracker_with(entry("one", description=left), entry("two", description=right))
    assert tracker.find_duplicates() == [("one", "two")]


@pytest.mark.parametrize("changes", [
    {"description": "different"}, {"amount": Decimal("10.01")}, {"type": "expense"},
])
def test_different_content_does_not_match(changes):
    assert tracker_with(entry("one"), entry("two", **changes)).find_duplicates(10) == []


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("days,expected", [(1, []), (2, [("z", "a")])])
def test_inclusive_window_across_year_boundary(reverse, days, expected):
    dates = [date(2025, 12, 31), date(2026, 1, 2)]
    if reverse:
        dates.reverse()
    tracker = tracker_with(entry("z", date=dates[0]), entry("a", date=dates[1]))
    assert tracker.find_duplicates(days) == expected


def test_three_matching_entries_and_disjoint_sets_in_insertion_order():
    tracker = tracker_with(entry("z"), entry("x", description="other"), entry("a"),
                           entry("y", description="OTHER"), entry("b"))
    assert tracker.find_duplicates() == [("z", "a"), ("z", "b"), ("x", "y"), ("a", "b")]


def test_date_chain_does_not_introduce_transitive_matches():
    tracker = tracker_with(entry("one"), entry("two", date=date(2026, 1, 2)),
                           entry("three", date=date(2026, 1, 3)))
    assert tracker.find_duplicates(1) == [("one", "two"), ("two", "three")]


def test_extreme_dates_and_large_window():
    tracker = tracker_with(entry("last", date=date.max), entry("first", date=date.min))
    assert tracker.find_duplicates(10**20) == [("last", "first")]


@pytest.mark.parametrize("window", [True, False, -1, 0.0, 1.5, "1", None, Decimal("1"), [], {}])
@pytest.mark.parametrize("populated", [False, True])
def test_invalid_windows_raise_value_error(window, populated):
    tracker = tracker_with(entry("one")) if populated else FinanceTracker()
    with pytest.raises(ValueError):
        tracker.find_duplicates(window)


@pytest.mark.parametrize("description", [None, 1, 0.1, True, [], {}, b"text"])
def test_non_string_descriptions_raise_value_error(description):
    with pytest.raises(ValueError):
        entry("one", description=description)


def test_detection_preserves_objects_fields_order_balance_and_results_are_independent():
    items = [entry("z", description=" Pay\t DAY "),
             entry("a", description="pay day", amount=Decimal("10.00")),
             entry("expense", type="expense")]
    tracker = tracker_with(*items)
    fields_before = [asdict(item) for item in items]
    balance_before = tracker.balance()
    pairs = tracker.find_duplicates(1)
    assert pairs == [("z", "a")]
    assert tracker.list_transactions() == items
    assert all(actual is original for actual, original in zip(tracker.list_transactions(), items))
    assert [asdict(item) for item in tracker.list_transactions()] == fields_before
    assert tracker.balance() == balance_before == Decimal("10.00")
    pairs.clear()
    assert tracker.find_duplicates(1) == [("z", "a")]
