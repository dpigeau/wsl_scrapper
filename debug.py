import duckdb

con = duckdb.connect("wsl.db")

query = """
    CREATE OR REPLACE TABLE raw_heats AS
    SELECT 
        *
    FROM read_json(
        'data/raw_heats/*.json',
        columns = {
            round_id: 'VARCHAR',
            heat_id: 'VARCHAR',
            athlete_id: 'VARCHAR',
            athlete_name: 'VARCHAR',
            total_score: DOUBLE
        }
    );
"""

con.sql(query)
con.sql("SELECT * FROM raw_heats").show()