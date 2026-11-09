"""Transaction data validation utilities."""

import math
from numbers import Real


def validate_transaction_amount(amount: Real) -> float:
    """Validate a transaction amount and return it as a float."""
    if isinstance(amount, bool) or not isinstance(amount, Real):
        raise TypeError("Transaction amount must be a numeric value.")

    if not math.isfinite(amount):
        raise ValueError("Transaction amount must be finite.")

    if amount < 0:
        raise ValueError("Transaction amount cannot be negative.")

    return float(amount)