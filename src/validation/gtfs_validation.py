
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GTFS_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"


def main():
    print("CHENNAI GTFS DATA QUALITY REPORT")
    print("=" * 40)

    # Load the core GTFS tables
    routes = pd.read_csv(GTFS_DIR / "routes.txt", low_memory=False)
    stops = pd.read_csv(GTFS_DIR / "stops.txt", low_memory=False)
    trips = pd.read_csv(GTFS_DIR / "trips.txt", low_memory=False)
    stop_times = pd.read_csv(
        GTFS_DIR / "stop_times.txt",
        low_memory=False
    )

    # 1. Check row counts
    print("\n1. ROW COUNTS")
    for name, df in {
        "routes": routes,
        "stops": stops,
        "trips": trips,
        "stop_times": stop_times,
    }.items():
        print(f"{name}: {len(df):,} rows")

    # 2. Check duplicate primary identifiers
    print("\n2. DUPLICATE IDENTIFIER CHECKS")
    checks = [
        ("routes.route_id", routes, "route_id"),
        ("stops.stop_id", stops, "stop_id"),
        ("trips.trip_id", trips, "trip_id"),
    ]

    for label, df, column in checks:
        duplicates = df[column].duplicated().sum()
        print(f"{label}: {duplicates:,} duplicate values")

    # 3. Check missing values in important columns
    print("\n3. MISSING REQUIRED VALUES")
    required_columns = {
        "routes": (routes, ["route_id", "route_type"]),
        "stops": (stops, ["stop_id", "stop_name", "stop_lat", "stop_lon"]),
        "trips": (trips, ["trip_id", "route_id", "service_id"]),
        "stop_times": (
            stop_times,
            ["trip_id", "arrival_time", "departure_time",
             "stop_id", "stop_sequence"]
        ),
    }

    for table_name, (df, columns) in required_columns.items():
        for column in columns:
            missing = df[column].isna().sum()
            print(f"{table_name}.{column}: {missing:,} missing")

    # 4. Check referential integrity
    print("\n4. RELATIONSHIP CHECKS")

    invalid_trip_routes = (
        ~trips["route_id"].isin(routes["route_id"])
    ).sum()

    invalid_trip_ids = (
        ~stop_times["trip_id"].isin(trips["trip_id"])
    ).sum()

    invalid_stop_ids = (
        ~stop_times["stop_id"].isin(stops["stop_id"])
    ).sum()

    print(f"Trips with unknown route IDs: {invalid_trip_routes:,}")
    print(f"Stop times with unknown trip IDs: {invalid_trip_ids:,}")
    print(f"Stop times with unknown stop IDs: {invalid_stop_ids:,}")

    # 5. Check geographic coordinate ranges
    print("\n5. GEOGRAPHIC COORDINATE CHECKS")

    invalid_lat = (
        ~stops["stop_lat"].between(-90, 90)
    ).sum()

    invalid_lon = (
        ~stops["stop_lon"].between(-180, 180)
    ).sum()

    print(f"Invalid latitude values: {invalid_lat:,}")
    print(f"Invalid longitude values: {invalid_lon:,}")

    print("\nValidation checks completed.")


if __name__ == "__main__":
    main()
