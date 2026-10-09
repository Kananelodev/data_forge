"""Q03 · Weigh the Ore                                          [Query Crucible]

PLAIN IDEA
  "How much did each province spend?" means: sort the receipts into piles by
  province, then add up each pile. "Which shops are busy?" means: count each
  shop's pile, and only keep the big piles.

JARGON
  GROUP BY makes the piles. Aggregate functions (SUM, COUNT, AVG, MIN, MAX)
  collapse each pile to one value. WHERE filters rows BEFORE grouping; HAVING
  filters groups AFTER grouping. Knowing which one to use is a classic
  interview question.

Each function returns a SQL STRING. The gate runs it against a seeded
`transactions(txn_id, customer_id, province, merchant, amount, ts)` table.
"""


def revenue_by_province_sql() -> str:
    """Total amount per province.
    Columns: (province, revenue). Order: revenue descending.
    """
    raise NotImplementedError


def busy_merchants_sql() -> str:
    """Merchants with MORE THAN 2 transactions.
    Columns: (merchant, txn_count). Order: txn_count desc, then merchant asc.
    """
    raise NotImplementedError


def avg_spend_per_customer_sql() -> str:
    """Average transaction amount per customer, rounded to 2 decimals.
    Columns: (customer_id, avg_amount). Order: customer_id asc.
    """
    raise NotImplementedError
