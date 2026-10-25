
from pathlib import Path
from zipfile import ZipFile
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ZIP_PATH = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "chennai-unified-gtfs.zip"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"

GTFS_FILES = [
    "agency.txt",
    "routes.txt",
    "stops.txt",
    "trips.txt",
    "stop_times.txt",
    "calendar.txt",
    "calendar_dates.txt",
]


def main():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            f"GTFS ZIP not found: {ZIP_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    saved_count = 0

    with ZipFile(ZIP_PATH, "r") as archive:
        available_files = archive.namelist()

        for filename in GTFS_FILES:
            matches = [
                name for name in available_files
                if name == filename
                or name.endswith("/" + filename)
            ]

            if not matches:
                print(f"SKIPPED: {filename} not found")
                continue

            output_path = OUTPUT_DIR / filename

            with archive.open(matches[0]) as source:
                with output_path.open("wb") as destination:
                    shutil.copyfileobj(source, destination)

            size_kb = output_path.stat().st_size / 1024

            print(
                f"Saved {filename} "
                f"({size_kb:,.1f} KB)"
            )

            saved_count += 1

    print(f"\nIngestion complete: {saved_count} files saved.")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
