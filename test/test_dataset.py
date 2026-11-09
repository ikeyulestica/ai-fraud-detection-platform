
"""Unit tests for synthetic dataset preparation and CSV export."""

import csv

import pytest

from fraud_detection.data.dataset import (
    CSV_FIELDS,
    export_dataset_csv,
    prepare_dataset,
)


def test_prepare_dataset_count():
    """Dataset should contain the requested number of records."""
    transactions = prepare_dataset(count=100, seed=42)
    assert len(transactions) == 100


def test_prepare_dataset_reproducibility():
    """The same seed should produce identical datasets."""
    first = prepare_dataset(count=100, seed=42)
    second = prepare_dataset(count=100, seed=42)
    assert first == second


@pytest.mark.parametrize("count", [0, -1, True, False])
def test_prepare_dataset_invalid_count(count):
    """Invalid transaction counts should be rejected."""
    with pytest.raises(ValueError):
        prepare_dataset(count=count)


def test_export_dataset_csv(tmp_path):
    """Exported CSV should contain the expected records and headers."""
    transactions = prepare_dataset(count=10, seed=42)
    output_path = tmp_path / "transactions.csv"

    result = export_dataset_csv(transactions, output_path)

    assert result == output_path
    assert output_path.exists()

    with output_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        assert reader.fieldnames == CSV_FIELDS

    assert len(rows) == 10
    assert rows[0]["transaction_id"] == transactions[0]["transaction_id"]


def test_export_empty_dataset(tmp_path):
    """An empty dataset should be rejected."""
    output_path = tmp_path / "empty.csv"

    with pytest.raises(ValueError, match="Dataset cannot be empty"):
        export_dataset_csv([], output_path)

    assert not output_path.exists()


def test_export_invalid_transaction(tmp_path):
    """Invalid transactions should not be exported."""
    transactions = prepare_dataset(count=1)
    transactions[0]["amount"] = -100

    output_path = tmp_path / "invalid.csv"

    with pytest.raises(ValueError):
        export_dataset_csv(transactions, output_path)

    assert not output_path.exists()
