
from pathlib import Path
from getpass import getpass

import pandas as pd
import psycopg

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql" / "analytics"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "analytics"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "chennai_mobility",
    "user": "postgres",
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    password = getpass("PostgreSQL password: ")

    queries = {
        "transport_mode_summary": "01_transport_mode_summary.sql",
        "top_bus_routes": "02_top_bus_routes.sql",
        "top_stops": "03_top_stops.sql",
        "route_summary": "04_route_summary.sql",
    }

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        for output_name, sql_filename in queries.items():
            sql_path = SQL_DIR / sql_filename

            if not sql_path.exists():
                raise FileNotFoundError(
                    f"SQL file not found: {sql_path}"
                )

            query = sql_path.read_text(encoding="utf-8")
            df = pd.read_sql_query(query, conn)

            output_path = OUTPUT_DIR / f"{output_name}.csv"
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

            print(
                f"Exported {output_name}: "
                f"{len(df):,} rows -> {output_path}"
            )

    print("\nAll analytics exports completed!")


if __name__ == "__main__":
    main()
