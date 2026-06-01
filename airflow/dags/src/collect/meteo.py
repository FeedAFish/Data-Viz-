from datetime import datetime
from config.settings import OPENWEATHER_API_KEY, CITIES
import requests


BASE_URL = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&units=metric&appid={key}"


def collect_city_meteo(city: dict) -> dict | None:

    url = BASE_URL.format(lat=city["lat"], lon=city["lon"], key=OPENWEATHER_API_KEY)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if result and "current" in result:
            return {
                "city": city["name"],
                "timestamp": datetime.utcfromtimestamp(result["current"]["dt"]),
                "temp": result["current"].get("temp"),
                "feels_like": result["current"].get("feels_like"),
                "wind_speed": result["current"].get("wind_speed"),
                "wind_deg": result["current"].get("wind_deg"),
                "rain": result["current"].get("rain"),
                "humidity": result["current"].get("humidity"),
                "pressure": result["current"].get("pressure"),
                "weather": result["current"]["weather"][0]["description"],
                "icon_weather": result["current"]["weather"][0]["icon"],
            }
        return None
    except Exception as e:
        print(f"Erreur inattendue Openweathermap : {e}")
        return None


def collect_all_meteo() -> list[dict]:
    results = []
    for city in CITIES:
        record = collect_city_meteo(city)
        if record:
            results.append(record)
    return results
