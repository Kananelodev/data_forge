"""Q02 · Light the Warehouse                                    [Foundry Floor]

PLAIN IDEA
  A kitchen keeps raw ingredients, prepped ingredients and finished plates in
  separate places, so you never confuse them and can always go back to the raw
  stuff if a recipe goes wrong. Data teams do the same thing with tables.

JARGON
  The MEDALLION ARCHITECTURE: three layers (as SCHEMAS in the warehouse) —
    bronze : raw data exactly as it arrived. Never edited. Everything text.
    silver : cleaned, typed, deduplicated.
    gold   : business-ready tables ("marts") that answer real questions.
  Bronze stores everything as VARCHAR because source data lies about types —
  you enforce types later, in silver, where you can catch the liars.
  This quest is the warm-up for passport-pipeline Iteration 1.
"""


def create_medallion_schemas(con) -> None:
    """Create bronze, silver and gold schemas in the given DuckDB connection.

    Must be safe to call twice (calling again must not error). That property has
    a name you'll meet properly in q12 — for now, just make it true.
    """
    raise NotImplementedError


def create_bronze_table(con, name: str, columns: list[str]) -> None:
    """Create bronze.<name> with the given column names, every column VARCHAR.

    Also add two lineage columns at the end:
      _ingested_at  TIMESTAMP   — when the row landed
      _source_file  VARCHAR     — which file it came from
    """
    # raise NotImplementedError 
