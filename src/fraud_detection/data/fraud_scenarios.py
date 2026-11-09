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

def is_unusual_transaction_time(
    hour: int,
    start_hour: int = 0,
    end_hour: int = 5,
) -> bool:
    """Identify transactions occurring during configured unusual hours."""
    if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 23:
        raise ValueError("Hour must be an integer between 0 and 23.")

    if not 0 <= start_hour < end_hour <= 24:
        raise ValueError("Invalid unusual-hour range.")

    return start_hour <= hour < end_hour