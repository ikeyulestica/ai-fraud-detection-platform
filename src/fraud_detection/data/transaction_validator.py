
"""Validate synthetic banking transaction records."""

from datetime import datetime
from uuid import UUID

from fraud_detection.data.generator import MERCHANT_CATEGORIES
from fraud_detection.data.validation import validate_transaction_amount

REQUIRED_FIELDS = {
    "transaction_id",
    "timestamp",
    "amount",
    "merchant_category",
    "is_fraud",
}


def validate_transaction(transaction: dict) -> bool:
    """Validate the structure and values of a transaction."""
    if not isinstance(transaction, dict):
        raise TypeError("Transaction must be a dictionary.")

    missing_fields = REQUIRED_FIELDS - transaction.keys()
    if missing_fields:
        raise ValueError(f"Missing required fields: {sorted(missing_fields)}")

    try:
        UUID(transaction["transaction_id"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("Invalid transaction ID.") from exc

    try:
        timestamp = datetime.fromisoformat(transaction["timestamp"])
    except (ValueError, TypeError) as exc:
        raise ValueError("Invalid transaction timestamp.") from exc

    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Transaction timestamp must include a timezone.")

    validate_transaction_amount(transaction["amount"])

    if transaction["merchant_category"] not in MERCHANT_CATEGORIES:
        raise ValueError("Invalid merchant category.")

    if type(transaction["is_fraud"]) is not int or transaction["is_fraud"] not in (0, 1):
        raise ValueError("Fraud label must be 0 or 1.")

    return True
