import requests
import os
from config.settings import API_URL


def get_latest_air_kpis(city_name: str | None = None) -> dict:
    try:
        endpoint = f"{API_URL}/air-quality/latest"
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {"success": True, "data": data[0], "message": ""}
    except Exception as e:
        error_msg = f"Error fetching KPIs: {str(e)}"
        print(error_msg)
        return {"success": False, "data": [], "message": error_msg}
