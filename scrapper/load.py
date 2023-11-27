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
        FROM read_json(
            'scrapper/data/raw_heats/*.json',
            columns = {
                round_id: 'VARCHAR',
                heat_id: 'VARCHAR',
                athlete_id: 'VARCHAR',
                athlete_name: 'VARCHAR',
                total_score: 'FLOAT'
            }
            
        );

        CREATE OR REPLACE TABLE raw.results AS
        SELECT 
            *
        FROM read_json(
            'scrapper/data/raw_results/*.json',
            columns = {
                event: 'VARCHAR',
                location: 'VARCHAR',
                click_type: 'VARCHAR',
                click_text: 'VARCHAR',
                event_tab: 'VARCHAR',
                content_type: 'VARCHAR',
                content_id: 'VARCHAR',
                content_title: 'VARCHAR',
                video_name: 'VARCHAR',
                video_length: INTEGER,
                provider_id: 'VARCHAR',
                provider_name: 'VARCHAR',
                provider_video_id: 'VARCHAR',
                round_names: 'VARCHAR',
                round_numbers: INTEGER,
                round_ids: 'VARCHAR',
                tour_ids: 'VARCHAR',
                tour_codes: 'VARCHAR',
                tour_genders: 'VARCHAR',
                heat_numbers: INTEGER,
                heat_ids: 'VARCHAR',
                athlete_ids: 'VARCHAR',
                athlete_names: 'VARCHAR',
                wave_scores: 'VARCHAR',
                wave_ids: 'VARCHAR',
                event_ids: 'VARCHAR',
                event_names: 'VARCHAR',
                event_years: 'VARCHAR',
                event_group_ids: 'VARCHAR',
                event_group_names: 'VARCHAR',
                slug: 'VARCHAR'
            }
        ); 
    """

    con.sql(query)

if __name__=="__main__":
    env = get_env()
    model_path = "dbt/wsl_analytics/"
    db_path = os.path.join(model_path, f"{env}.duckdb")
    con = duckdb.connect(db_path)
    load_data(con)

    con.sql("SELECT * FROM raw.results LIMIT 20;").show()
    con.close()
