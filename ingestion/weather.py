from pathlib import Path


import requests
import yaml
from tenacity import retry, stop_after_attempt, wait_exponential
from .load import load_weather


OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


def load_cities(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config["cities"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
)
def fetch_weather(city, target_date):
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": target_date,
        "end_date": target_date,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "temperature_2m_mean,"
            "precipitation_sum,"
            "wind_speed_10m_max"
        ),
        "timezone": "UTC",
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def build_rows(city, weather_response):
    daily = weather_response["daily"]

    rows = []

    for i, weather_date in enumerate(daily["time"]):
        rows.append(
            {
                "city": city["name"],
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "weather_date": weather_date,
                "temperature_2m_max": daily["temperature_2m_max"][i],
                "temperature_2m_min": daily["temperature_2m_min"][i],
                "temperature_2m_mean": daily["temperature_2m_mean"][i],
                "precipitation_sum": daily["precipitation_sum"][i],
                "wind_speed_10m_max": daily["wind_speed_10m_max"][i],
            }
        )

    return rows


def run_pipeline(target_date):
    config_path = (
        Path(__file__).resolve().parents[1]
        / "config"
        / "cities.yml"
    )

    cities = load_cities(config_path)

    all_rows = []

    for city in cities:
        response = fetch_weather(city, target_date)
        rows = build_rows(city, response)
        all_rows.extend(rows)

    load_weather(all_rows)

    print(f"Loaded {len(all_rows)} rows for {target_date}")


if __name__ == "__main__":
    run_pipeline("2026-09-08")