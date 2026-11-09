
"""Unit tests for banking transaction record validation."""

import pytest

from fraud_detection.data.generator import generate_transactions
from fraud_detection.data.transaction_validator import validate_transaction


def test_valid_transaction():
    """A generated transaction should pass validation."""
    transaction = generate_transactions(count=1)[0]
    assert validate_transaction(transaction) is True


@pytest.mark.parametrize(
    "field",
    ["transaction_id", "timestamp", "amount", "merchant_category", "is_fraud"],
)
def test_missing_required_field(field):
    """Missing required fields should raise ValueError."""
    transaction = generate_transactions(count=1)[0]
    del transaction[field]

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_transaction(transaction)


def test_invalid_transaction_id():
    """An invalid UUID should be rejected."""
    transaction = generate_transactions(count=1)[0]
    transaction["transaction_id"] = "invalid-uuid"

    with pytest.raises(ValueError, match="Invalid transaction ID"):
        validate_transaction(transaction)


@pytest.mark.parametrize(
    "timestamp",
    ["invalid-date", "2026-01-01T10:00:00"],
)
def test_invalid_timestamp(timestamp):
    """Invalid or timezone-naive timestamps should be rejected."""
    transaction = generate_transactions(count=1)[0]
    transaction["timestamp"] = timestamp

    with pytest.raises(ValueError):
        validate_transaction(transaction)


def test_invalid_amount():
    """Negative transaction amounts should be rejected."""
    transaction = generate_transactions(count=1)[0]
    transaction["amount"] = -100.00

    with pytest.raises(ValueError):
        validate_transaction(transaction)


def test_invalid_merchant_category():
    """Unknown merchant categories should be rejected."""
    transaction = generate_transactions(count=1)[0]
    transaction["merchant_category"] = "unknown"

    with pytest.raises(ValueError, match="Invalid merchant category"):
        validate_transaction(transaction)


@pytest.mark.parametrize("label", [-1, 2, True, False, "1"])
def test_invalid_fraud_label(label):
    """Fraud labels must be integers equal to zero or one."""
    transaction = generate_transactions(count=1)[0]
    transaction["is_fraud"] = label

    with pytest.raises(ValueError, match="Fraud label must be 0 or 1"):
        validate_transaction(transaction)


def test_transaction_not_dictionary():
    """Non-dictionary transactions should be rejected."""
    with pytest.raises(TypeError, match="Transaction must be a dictionary"):
        validate_transaction("invalid-transaction")
