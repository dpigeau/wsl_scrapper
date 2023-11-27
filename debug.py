import duckdb

con = duckdb.connect("dbt/wsl_analytics/dev.duckdb")

query = """
    SHOW ALL TABLES;
"""

con.sql(query).show()