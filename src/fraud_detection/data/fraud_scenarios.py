"""Synthetic fraud scenario rules for transaction simulation."""


def is_high_amount_transaction(
    amount: float,
    threshold: float = 8000.0,
) -> bool:
    """Identify transactions exceeding the configured amount threshold."""
    if amount < 0:
        raise ValueError("Transaction amount cannot be negative.")

    if threshold <= 0:
        raise ValueError("Threshold must be greater than zero.")

    return amount > threshold