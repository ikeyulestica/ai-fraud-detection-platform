"""Unit tests for synthetic banking transaction generation."""

import pytest

from fraud_detection.data.generator import generate_transactions


def test_generate_transaction_count():
    """Generator should return the requested number of transactions."""
    transactions = generate_transactions(count=100, seed=42)

    assert len(transactions) == 100

def test_generate_transactions_reproducibility():
    """The same seed should produce identical transactions."""
    first_run = generate_transactions(count=100, seed=42)
    second_run = generate_transactions(count=100, seed=42)

    assert first_run == second_run


@pytest.mark.parametrize("count", [0, -1, True, False])
def test_generate_transactions_invalid_count(count):
    """Invalid transaction counts should raise ValueError."""
    with pytest.raises(ValueError):
        generate_transactions(count=count)

def test_high_amount_transactions_are_labeled_fraud():
    """High-amount synthetic transactions should receive a fraud label."""
    transactions = generate_transactions(count=100, seed=42)

    high_amount_transactions = [
        transaction
        for transaction in transactions
        if transaction["amount"] > 8000.0
    ]

    assert high_amount_transactions, "Expected at least one high-amount transaction."
    assert all(
        transaction["is_fraud"] == 1
        for transaction in high_amount_transactions
    )