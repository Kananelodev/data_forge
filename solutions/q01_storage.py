"""Q01 · Two Kinds of Database                                  [Foundry Floor]

PLAIN IDEA
  Imagine a spreadsheet with 50 columns and a million rows.
  - An APP (like a banking app) usually wants ONE whole row: "show me
    customer C1's everything." Storing data row-by-row makes that fast.
  - A REPORT usually wants TWO columns across ALL rows: "total amount by
    province." If data is stored column-by-column, the engine can read just
    those two columns and skip the other 48 entirely.

JARGON
  Row-by-row storage serves OLTP (Online Transaction Processing) — many small
  reads/writes of whole records. Column-by-column storage serves OLAP (Online
  Analytical Processing) — big scans of a few columns. Warehouses like
  Redshift, BigQuery, Snowflake and DuckDB are columnar. Columnar data also
  compresses better, because a column holds similar values.
"""


def bytes_scanned(store: str, total_cols: int, selected_cols: int,
                  rows: int, bytes_per_cell: int) -> int:
    """How many bytes must be read to answer a query that needs `selected_cols`
    columns across all `rows` rows.

    store = "row"    -> a row store must read every column of every row.
    store = "column" -> a column store reads only the selected columns.
    Raise ValueError for any other store type.
    (Ignore compression and indexes — this is the core intuition only.)
    """
    raise NotImplementedError


def best_store_for(workload: dict) -> str:
    """Return "OLTP" or "OLAP" for a workload description.

    `workload` keys (all booleans):
      single_record_lookups  — fetches one customer/order at a time
      frequent_updates       — rows change constantly (balances, statuses)
      scans_many_rows        — touches millions of rows per query
      few_columns_per_query  — needs a handful of columns, not the whole row

    Decide which signals point which way and implement the rule. Your journal
    should justify it.
    """
    raise NotImplementedError
