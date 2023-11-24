import duckdb
import sys
import os

def get_env() -> str:

    try:
        env = sys.argv[1]
    except IndexError:
        raise Exception("Please provide an environment argument (dev/prod)")
    
    if env in ["dev", "prod"]:
        return env
    raise Exception(f"Error: environment set to '{env}'. Must be either 'dev' or 'prod'")


def load_data(con) -> None:
    
    query = """
        CREATE SCHEMA IF NOT EXISTS raw;

        CREATE OR REPLACE TABLE raw.heats AS
        SELECT 
            *
        FROM read_json_auto('scrapper/data/raw_heats/*.json');

        CREATE OR REPLACE TABLE raw.results AS
        SELECT 
            *
        FROM read_json_auto('scrapper/data/raw_results/*.json'); 
    """

    con.sql(query)

if __name__=="__main__":
    env = get_env()
    model_path = "dbt/wsl_analytics/models"
    # db_path = os.path.join(model_path, f"{env}.duckdb")
    db_path = f"{env}.duckdb"
    con = duckdb.connect(db_path)
    load_data(con)

    con.sql("SELECT * FROM raw.results LIMIT 20;").show()
    con.close()
