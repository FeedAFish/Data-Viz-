from src.config.settings import CITIES
from src.analytics.aqicn import get_latest_air_kpis

if __name__ == "__main__":
    name = [city["name"] for city in CITIES]
    print(get_latest_air_kpis(name))
