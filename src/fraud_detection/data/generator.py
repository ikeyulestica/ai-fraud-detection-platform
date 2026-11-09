"""Generate reproducible synthetic banking transaction data."""

import random
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid5

from fraud_detection.data.fraud_scenarios import (
    is_high_amount_transaction,
    is_unusual_transaction_time,
)

MERCHANT_CATEGORIES = (
    "groceries",
    "retail",
    "fuel",
    "travel",
    "electronics",
    "restaurants",
)

TRANSACTION_NAMESPACE = UUID("12345678-1234-5678-1234-567812345678")


def generate_transactions(count: int = 1000, seed: int = 42) -> list[dict]:
    """Generate synthetic transactions for fraud detection experiments."""
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("count must be a positive integer.")

    rng = random.Random(seed)
    start_time = datetime(2026, 1, 1, tzinfo=UTC)
    transactions = []

    for index in range(count):
        amount = round(rng.uniform(1.0, 10000.0), 2)
        category = rng.choice(MERCHANT_CATEGORIES)
        timestamp = start_time + timedelta(minutes=index * 5)
        is_fraud = int(
            is_high_amount_transaction(amount)
            or is_unusual_transaction_time(timestamp.hour)
        )

        transaction = {
            "transaction_id": str(uuid5(TRANSACTION_NAMESPACE, f"{seed}-{index}")),
            "timestamp": timestamp.isoformat(),
            "amount": amount,
            "merchant_category": category,
            "is_fraud": is_fraud,
        }
        transactions.append(transaction)

    return transactions