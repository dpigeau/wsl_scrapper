import duckdb

con = duckdb.connect("dbt/wsl_analytics/models/dev.duckdb")

query = """
    SELECT * FROM raw_results
"""

con.sql(query).show()