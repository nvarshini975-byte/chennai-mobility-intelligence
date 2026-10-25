import requests
import pandas as pd
from pathlib import Path


# Chennai coordinates
LATITUDE = 13.0827
LONGITUDE = 80.2707

# Initial date range
START_DATE = "2025-01-01"
END_DATE = "2025-01-07"

# Open-Meteo historical API
URL = "https://archive-api.open-meteo.com/v1/archive"

PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m"
    ],
    "timezone": "Asia/Kolkata"
}


def fetch_weather_data():

    response = requests.get(
        URL,
        params=PARAMS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def transform_weather_data(data):

    hourly_data = data["hourly"]

    df = pd.DataFrame(hourly_data)

    df["time"] = pd.to_datetime(df["time"])

    return df


def save_data(df):

    output_path = Path(
        "data/raw/chennai_weather.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved {len(df)} records to {output_path}"
    )


def main():

    print("Fetching Chennai weather data...")

    data = fetch_weather_data()

    df = transform_weather_data(data)

    print("\nFirst 5 records:")
    print(df.head())

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumn information:")
    print(df.info())

    save_data(df)


if __name__ == "__main__":
    main()