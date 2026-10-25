
from pathlib import Path
from getpass import getpass

import pandas as pd
import psycopg

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "chennai_mobility",
    "user": "postgres",
}

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    password = getpass("PostgreSQL password: ")

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        query = """
            SELECT
                (SELECT COUNT(*) FROM warehouse.dim_stops) AS total_stops
        """
        df = pd.read_sql_query(query, conn)

    output_path = OUTPUT_DIR / "mobility_totals.csv"
    df.to_csv(output_path, index=False)
    print(df.to_string(index=False))
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
