"""Unit tests for synthetic fraud scenario detection."""

import pytest

from fraud_detection.data.fraud_scenarios import is_high_amount_transaction


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