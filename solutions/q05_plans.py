"""Q05 · Read the Smoke                                         [Query Crucible]

PLAIN IDEA
  Before cooking, a chef has a plan: chop, then fry, then plate. A database
  makes a plan too before running your query. Reading that plan tells you WHY a
  query is slow — which step is doing all the work.

JARGON
  EXPLAIN shows the QUERY PLAN — a tree of OPERATORS (scans, filters, joins,
  aggregations). EXPLAIN ANALYZE also runs it and reports real timings/rows.
  Juniors guess at slow queries; seniors read the plan.
"""


def explain(con, sql: str) -> str:
    """Return DuckDB's plan for `sql` as one string (use EXPLAIN).
    Hint: EXPLAIN returns rows; find which column holds the plan text.
    """
    raise NotImplementedError


def most_expensive_operator(plan: str) -> str:
    """Given a simplified plan where each line looks like

        <indent>OPERATOR_NAME  time=<ms>ms  rows=<n>

    return the OPERATOR_NAME with the largest time. (Indentation shows the tree
    shape; you can ignore it for this function.)
    """
    raise NotImplementedError
