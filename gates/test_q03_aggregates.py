"""GATE q03 · Weigh the Ore"""
from collections import Counter, defaultdict
from decimal import ROUND_HALF_UP, Decimal

from _seed import TRANSACTIONS
from conftest import run
from q03_aggregates import avg_spend_per_customer_sql, busy_merchants_sql, revenue_by_province_sql


def _d(x):
    # SQL ROUND() rounds halves UP (247.625 -> 247.63). Python's Decimal defaults
    # to banker's rounding (-> 247.62). Mismatched rounding between two systems is
    # a classic cause of "the numbers don't reconcile" bugs — worth a journal line.
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def test_revenue_by_province(forge_db):
    totals = defaultdict(Decimal)
    for _, _, prov, _, amt, _ in TRANSACTIONS:
        totals[prov] += _d(amt)
    expected = sorted(totals.items(), key=lambda kv: -kv[1])
    got = [(p, _d(r)) for p, r in run(forge_db, revenue_by_province_sql())]
    assert got == expected


def test_busy_merchants(forge_db):
    counts = Counter(t[3] for t in TRANSACTIONS)
    expected = sorted([(m, c) for m, c in counts.items() if c > 2], key=lambda mc: (-mc[1], mc[0]))
    assert run(forge_db, busy_merchants_sql()) == expected


def test_avg_spend_per_customer(forge_db):
    per = defaultdict(list)
    for _, cust, _, _, amt, _ in TRANSACTIONS:
        per[cust].append(_d(amt))
    expected = [(c, _d(sum(v) / len(v))) for c, v in sorted(per.items())]
    got = [(c, _d(a)) for c, a in run(forge_db, avg_spend_per_customer_sql())]
    assert got == expected
