"""GATE q05 · Read the Smoke"""
from q05_plans import explain, most_expensive_operator

SAMPLE_PLAN = """\
PROJECTION  time=0.4ms  rows=3
  ORDER_BY  time=1.1ms  rows=3
    HASH_GROUP_BY  time=38.7ms  rows=3
      FILTER  time=12.2ms  rows=840000
        SEQ_SCAN  time=21.5ms  rows=1000000
"""


def test_explain_returns_a_plan(forge_db):
    plan = explain(forge_db, "SELECT province, SUM(amount) FROM transactions GROUP BY province")
    assert isinstance(plan, str)
    assert "SCAN" in plan.upper(), "the plan should show how the table is read"
    assert "GROUP" in plan.upper() or "AGGREGATE" in plan.upper()


def test_finds_the_hot_operator():
    assert most_expensive_operator(SAMPLE_PLAN) == "HASH_GROUP_BY"


def test_handles_a_different_plan():
    plan = "PROJECTION  time=2.0ms  rows=10\n  HASH_JOIN  time=5.5ms  rows=10\n    SEQ_SCAN  time=91.0ms  rows=5000000\n"
    assert most_expensive_operator(plan) == "SEQ_SCAN"
