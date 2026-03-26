from config.settings import DATABASE_URL
from sqlalchemy import create_engine, text


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def get_latest_air_kpis(city_name: str | None = None) -> dict:
    try:
        engine = get_engine()
        sql = f"""
            SELECT DISTINCT ON (c.name)
                c.name AS city,
                a.aqi,
                a.pm25
            FROM air_quality_records a
            JOIN cities c ON c.id = a.city_id
            ORDER BY c.name, a.recorded_at DESC
        """
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]

        return {"success": True, "data": data, "message": ""}
    except Exception as e:
        error_msg = f"Error fetching KPIs: {str(e)}"
        print(error_msg)
        return {"success": False, "data": [], "message": error_msg}
