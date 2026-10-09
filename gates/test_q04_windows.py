"""GATE q04 · Windows into the Fire"""
from collections import defaultdict
from decimal import Decimal

from _seed import TRANSACTIONS
from conftest import run
from q04_windows import biggest_txn_per_province_sql, running_total_sql


def _d(x):
    return Decimal(str(x)).quantize(Decimal("0.01"))


def test_running_total_keeps_every_row(forge_db):
    rows = run(forge_db, running_total_sql())
    assert len(rows) == len(TRANSACTIONS), "window functions must NOT collapse rows"


def test_running_total_values(forge_db):
    expected, acc = [], defaultdict(Decimal)
    for t in sorted(TRANSACTIONS, key=lambda t: (t[1], t[5])):
        acc[t[1]] += _d(t[4])
        expected.append((t[1], t[0], acc[t[1]]))
    got = [(c, t, _d(r)) for c, t, r in run(forge_db, running_total_sql())]
    assert got == expected


def test_biggest_txn_per_province(forge_db):
    best = {}
    for t in TRANSACTIONS:
        if t[2] not in best or t[4] > best[t[2]][4]:
            best[t[2]] = t
    expected = [(p, best[p][0], _d(best[p][4])) for p in sorted(best)]
    got = [(p, t, _d(a)) for p, t, a in run(forge_db, biggest_txn_per_province_sql())]
    assert got == expected
