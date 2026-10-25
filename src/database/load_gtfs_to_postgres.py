
from pathlib import Path
from getpass import getpass
import csv
import psycopg
from psycopg import sql

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GTFS_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"

TABLE_FILES = {
    "agency": "agency.txt",
    "routes": "routes.txt",
    "stops": "stops.txt",
    "trips": "trips.txt",
    "stop_times": "stop_times.txt",
    "calendar": "calendar.txt",
    "calendar_dates": "calendar_dates.txt",
}

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "chennai_mobility",
    "user": "postgres",
}


def get_columns(file_path):
    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return next(csv.reader(file))


def main():
    password = getpass("PostgreSQL password: ")

    with psycopg.connect(
        **DB_CONFIG, password=password
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS staging")

            for table_name, filename in TABLE_FILES.items():
                file_path = GTFS_DIR / filename

                if not file_path.exists():
                    raise FileNotFoundError(file_path)

                columns = get_columns(file_path)

                column_definitions = sql.SQL(", ").join(
                    sql.SQL("{} TEXT").format(
                        sql.Identifier(column)
                    )
                    for column in columns
                )

                create_query = sql.SQL(
                    "CREATE TABLE IF NOT EXISTS staging.{} ({})"
                ).format(
                    sql.Identifier(table_name),
                    column_definitions,
                )

                cur.execute(create_query)

                cur.execute(
                    sql.SQL("TRUNCATE TABLE staging.{}").format(
                        sql.Identifier(table_name)
                    )
                )

                copy_query = sql.SQL(
                    "COPY staging.{} ({}) "
                    "FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
                ).format(
                    sql.Identifier(table_name),
                    sql.SQL(", ").join(
                        sql.Identifier(column)
                        for column in columns
                    ),
                )

                print(f"Loading {filename}...")

                with cur.copy(copy_query) as copy:
                    with file_path.open("rb") as file:
                        while chunk := file.read(1024 * 1024):
                            copy.write(chunk)

                cur.execute(
                    sql.SQL("SELECT COUNT(*) FROM staging.{}").format(
                        sql.Identifier(table_name)
                    )
                )

                row_count = cur.fetchone()[0]
                print(f"Loaded {row_count:,} rows into staging.{table_name}")

    print("\nGTFS loading completed successfully!")


if __name__ == "__main__":
    main()
