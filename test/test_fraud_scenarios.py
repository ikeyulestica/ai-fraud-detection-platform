"""Unit tests for synthetic fraud scenario detection."""

import pytest

from fraud_detection.data.fraud_scenarios import (
    is_high_amount_transaction,
    is_unusual_transaction_time,
)


def test_high_amount_transaction():
    """Amounts above the threshold should be flagged."""
    assert is_high_amount_transaction(9500.0) is True


def test_normal_amount_transaction():
    """Amounts below the threshold should not be flagged."""
    assert is_high_amount_transaction(500.0) is False


def test_amount_at_threshold():
    """Amounts equal to the threshold should not be flagged."""
    assert is_high_amount_transaction(8000.0) is False


def test_negative_transaction_amount():
    """Negative amounts should raise ValueError."""
    with pytest.raises(ValueError, match="Transaction amount cannot be negative"):
        is_high_amount_transaction(-500.0)


def test_zero_threshold():
    """A zero threshold should raise ValueError."""
    with pytest.raises(ValueError, match="Threshold must be greater than zero"):
        is_high_amount_transaction(500.0, threshold=0.0)

def test_unusual_transaction_time():
    """Transactions at 2 AM should be flagged as unusual."""
    assert is_unusual_transaction_time(2) is True


def test_normal_transaction_time():
    """Transactions at 2 PM should not be flagged."""
    assert is_unusual_transaction_time(14) is False


def test_unusual_time_boundary():
    """Transactions at 5 AM should not be flagged."""
    assert is_unusual_transaction_time(5) is False


def test_invalid_transaction_hour():
    """Hours outside the valid range should raise ValueError."""
    with pytest.raises(ValueError, match="Hour must be an integer between 0 and 23"):
        is_unusual_transaction_time(25)


def test_invalid_unusual_hour_range():
    """An invalid unusual-hour range should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid unusual-hour range"):
        is_unusual_transaction_time(2, start_hour=10, end_hour=5)        