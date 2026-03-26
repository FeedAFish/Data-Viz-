from fastapi import FastAPI
from .get import get_latest_air_kpis

app = FastAPI(title="GoodAir API", version="1.0.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/air-quality/latest")
async def get_latest():
    response = get_latest_air_kpis()
    return response["data"], 200 if response["success"] else 500
