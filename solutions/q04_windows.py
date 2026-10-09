"""Q04 · Windows into the Fire                                  [Query Crucible]

PLAIN IDEA
  GROUP BY squashes many rows into one. But sometimes you want to KEEP every
  row and still see something about its group — like a bank statement that
  shows each transaction AND your running balance next to it.

JARGON
  WINDOW FUNCTIONS compute over a "window" of related rows without collapsing
  them: SUM(...) OVER (PARTITION BY ... ORDER BY ...). PARTITION BY = which
  group; ORDER BY = order inside the group. ROW_NUMBER / RANK / DENSE_RANK
  rank rows within a partition. This is the single most-tested SQL topic in DE
  interviews.
"""


def running_total_sql() -> str:
    """Every transaction, with that customer's cumulative spend up to and
    including it (ordered by ts).
    Columns: (customer_id, txn_id, running_total). Order: customer_id, ts.
    """
    raise NotImplementedError


def biggest_txn_per_province_sql() -> str:
    """The single largest transaction in each province.
    Columns: (province, txn_id, amount). Order: province asc.
    Hint: rank inside each province, then keep rank 1.
    """
    raise NotImplementedError
