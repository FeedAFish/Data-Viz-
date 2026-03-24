from datetime import datetime
from ..config.settings import AQICN_TOKEN, CITIES
import requests

BASE_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"


def collect_city(city: dict) -> dict | None:
    url = BASE_URL.format(lat=city["lat"], lon=city["lon"], token=AQICN_TOKEN)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if result["status"] == "ok":
            data = result["data"]
            return {
                "city": city["name"],
                "aqi": data.get("aqi"),
                "pm25": data.get("iaqi", {}).get("pm25", {}).get("v"),
                "pm10": data.get("iaqi", {}).get("pm10", {}).get("v"),
                "no2": data.get("iaqi", {}).get("no2", {}).get("v"),
                "o3": data.get("iaqi", {}).get("o3", {}).get("v"),
                "timestamp": datetime.fromtimestamp(data["time"]["v"]),
            }
    except Exception as e:
        print(f"Erreur inattendue AQICN : {e}")
        return None


def collect_all() -> list[dict]:
    results = []
    for city in CITIES:
        record = collect_city(city)
        if record:
            results.append(record)
    print(f"AQICN : {len(results)}/{len(CITIES)} villes collectées.")
    return results
