"""GATE q02 · Light the Warehouse"""
from q02_warehouse import create_bronze_table, create_medallion_schemas


def _schemas(con):
    return {r[0] for r in con.execute(
        "SELECT schema_name FROM information_schema.schemata").fetchall()}


def test_three_layers_exist(con):
    create_medallion_schemas(con)
    assert {"bronze", "silver", "gold"} <= _schemas(con)


def test_safe_to_run_twice(con):
    create_medallion_schemas(con)
    create_medallion_schemas(con)   # must not raise
    assert {"bronze", "silver", "gold"} <= _schemas(con)


def test_bronze_is_all_text_plus_lineage(con):
    create_medallion_schemas(con)
    create_bronze_table(con, "customers", ["customer_id", "email", "signup_date"])
    cols = con.execute("""
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_schema = 'bronze' AND table_name = 'customers'
        ORDER BY ordinal_position
    """).fetchall()
    names = [c[0] for c in cols]
    types = dict(cols)
    assert names == ["customer_id", "email", "signup_date", "_ingested_at", "_source_file"]
    assert all(types[c] == "VARCHAR" for c in ["customer_id", "email", "signup_date", "_source_file"])
    assert types["_ingested_at"].startswith("TIMESTAMP")
