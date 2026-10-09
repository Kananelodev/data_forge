"""GATE q01 · Two Kinds of Database"""
import pytest

from q01_storage import best_store_for, bytes_scanned


def test_row_store_reads_every_column():
    assert bytes_scanned("row", 50, 2, 1_000_000, 8) == 50 * 1_000_000 * 8


def test_column_store_reads_only_what_it_needs():
    assert bytes_scanned("column", 50, 2, 1_000_000, 8) == 2 * 1_000_000 * 8


def test_columnar_advantage_is_the_column_ratio():
    row = bytes_scanned("row", 40, 4, 10_000, 8)
    col = bytes_scanned("column", 40, 4, 10_000, 8)
    assert row / col == 10


def test_unknown_store_is_rejected():
    with pytest.raises(ValueError):
        bytes_scanned("graph", 10, 1, 10, 8)


def test_banking_app_is_oltp():
    assert best_store_for({
        "single_record_lookups": True, "frequent_updates": True,
        "scans_many_rows": False, "few_columns_per_query": False,
    }) == "OLTP"


def test_dashboard_is_olap():
    assert best_store_for({
        "single_record_lookups": False, "frequent_updates": False,
        "scans_many_rows": True, "few_columns_per_query": True,
    }) == "OLAP"
