from fastapi import FastAPI
from .get import get_latest_air_kpis, get_latest_meteo_kpis

app = FastAPI(title="GoodAir API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/aqi/latest")
async def get_latest_air():
    response = get_latest_air_kpis()
    return response["data"], 200 if response["success"] else 500


@app.get("/meteo/latest")
async def get_latest_meteo():
    response = get_latest_meteo_kpis()
    return response["data"], 200 if response["success"] else 500
