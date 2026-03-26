from src.config.settings import CITIES
from src.analytics.aqicn import get_latest_air_kpis
from src.dashboard import run_dashboard

if __name__ == "__main__":
    # cards = []
    # reponse = get_latest_air_kpis()
    # for row in reponse["data"]:
    #     aqi = row["aqi"] if row["aqi"] else "N/A"

    run_dashboard()
