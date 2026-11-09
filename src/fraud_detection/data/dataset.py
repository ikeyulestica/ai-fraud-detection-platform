
"""Prepare and export validated synthetic transaction datasets."""

import csv
from pathlib import Path

from fraud_detection.data.generator import generate_transactions
from fraud_detection.data.transaction_validator import validate_transaction

CSV_FIELDS = [
    "transaction_id",
    "timestamp",
    "amount",
    "merchant_category",
    "is_fraud",
]


def prepare_dataset(count: int = 1000, seed: int = 42) -> list[dict]:
    """Generate and validate a synthetic transaction dataset."""
    transactions = generate_transactions(count=count, seed=seed)

    for transaction in transactions:
        validate_transaction(transaction)

    return transactions


def export_dataset_csv(
    transactions: list[dict],
    output_path: str | Path,
) -> Path:
    """Export validated transactions to a CSV file."""
    path = Path(output_path)

    if not transactions:
        raise ValueError("Dataset cannot be empty.")

    for transaction in transactions:
        validate_transaction(transaction)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(transactions)

    return path
