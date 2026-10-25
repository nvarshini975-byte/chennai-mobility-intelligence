
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "chennai_mobility",
    "user": "postgres",
    "password": input("Enter your PostgreSQL password: "),
}

try:
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), version()")
            result = cur.fetchone()

            print("Connection successful!")
            print("Database:", result[0])
            print("Version:", result[1])

except psycopg.Error as error:
    print("Database connection failed:", error)
