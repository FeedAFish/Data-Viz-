import sys
import os

# Import src setup to add to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DATABASE_URL
from sqlalchemy import create_engine, text
import json


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def get_latest_air_kpis(city_name: str | None = None) -> dict:
    """Derniers KPIs de qualité de l'air par ville (1 ligne / ville)."""
    engine = get_engine()
    sql = f"""
        SELECT DISTINCT ON (c.name)
            c.name AS city,
            a.aqi
        FROM air_quality_records a
        JOIN cities c ON c.id = a.city_id
        ORDER BY c.name, a.recorded_at DESC
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()

    data = [dict(row._mapping) for row in rows]

    return {"success": True, "data": data, "count": len(data)}
