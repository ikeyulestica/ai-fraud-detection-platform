"""Unit tests for transaction data validation."""

import pytest

from fraud_detection.data.validation import validate_transaction_amount


def test_valid_transaction_amount():
    """A valid positive amount should be accepted."""
    assert validate_transaction_amount(125.50) == 125.50


def test_negative_transaction_amount():
    """A negative transaction amount should be rejected."""
    with pytest.raises(ValueError):
        validate_transaction_amount(-100.00)

def test_string_transaction_amount():
    """A nonnumeric transaction amount should be rejected."""
    with pytest.raises(TypeError):
        validate_transaction_amount("ABC")  

@pytest.mark.parametrize("amount", [True, False])
def test_boolean_transaction_amount(amount):
    """Boolean values should not be accepted as transaction amounts."""
    with pytest.raises(TypeError):
        validate_transaction_amount(amount) 

@pytest.mark.parametrize(
    "amount",
    [float("nan"), float("inf"), float("-inf")],
)
def test_non_finite_transaction_amount(amount):
    """NaN and infinity values should be rejected."""
    with pytest.raises(ValueError):
        validate_transaction_amount(amount)