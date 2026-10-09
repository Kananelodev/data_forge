"""A tiny, deterministic dataset the SQL quests run against.

Gates compute the expected answers from this list in plain Python, so the test
checks your SQL is *correct* without ever showing you the SQL.
"""
TRANSACTIONS = [
    # txn_id, customer_id, province,        merchant,     amount, ts
    ("T01", "C1", "Gauteng",       "Checkers",   120.00, "2026-10-01 09:00"),
    ("T02", "C1", "Gauteng",       "Takealot",   850.50, "2026-10-01 18:30"),
    ("T03", "C2", "Western Cape",  "Woolworths", 310.00, "2026-10-02 10:15"),
    ("T04", "C3", "KwaZulu-Natal", "Checkers",    75.25, "2026-10-02 12:00"),
    ("T05", "C1", "Gauteng",       "Checkers",    60.00, "2026-10-03 08:45"),
    ("T06", "C2", "Western Cape",  "Takealot",  1299.99, "2026-10-03 20:10"),
    ("T07", "C4", "Gauteng",       "Uber Eats",  189.00, "2026-10-04 19:00"),
    ("T08", "C3", "KwaZulu-Natal", "Woolworths", 420.00, "2026-10-05 11:30"),
    ("T09", "C4", "Gauteng",       "Checkers",   230.40, "2026-10-05 17:20"),
    ("T10", "C2", "Western Cape",  "Checkers",    99.99, "2026-10-06 09:05"),
    ("T11", "C5", "Free State",    "Takealot",   540.00, "2026-10-06 14:00"),
    ("T12", "C1", "Gauteng",       "Uber Eats",  145.00, "2026-10-07 20:45"),
]
COLUMNS = ["txn_id", "customer_id", "province", "merchant", "amount", "ts"]
