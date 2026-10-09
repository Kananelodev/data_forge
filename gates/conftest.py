import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
"""Shared fixtures for the gates."""
import duckdb
import pytest

from _seed import TRANSACTIONS


@pytest.fixture
def con():
    """Empty in-memory DuckDB — fast, isolated, thrown away after each test."""
    c = duckdb.connect(":memory:")
    yield c
    c.close()


@pytest.fixture
def forge_db(con):
    """In-memory DuckDB with a seeded `transactions` table."""
    con.execute("""
        CREATE TABLE transactions (
            txn_id VARCHAR, customer_id VARCHAR, province VARCHAR,
            merchant VARCHAR, amount DECIMAL(10,2), ts TIMESTAMP
        )
    """)
    con.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", TRANSACTIONS)
    return con


def run(con, sql):
    """Run your SQL and return rows as a list of tuples."""
    return con.execute(sql).fetchall()
