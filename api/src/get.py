from config.settings import DATABASE_URL
from sqlalchemy import create_engine, text


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def get_latest_kpis() -> dict:
    """Get combined latest air quality and weather data for all cities"""
    try:
        engine = get_engine()
        sql = f"""
            SELECT DISTINCT ON (c.name)
                c.name AS city,
                w.recorded_at AS weather_time,
                a.recorded_at AS air_time,
                w.temp,
                w.feels_like,
                w.weather_description,
                w.icon_weather,
                w.wind_speed,
                w.wind_deg,
                w.humidity,
                a.aqi,
                a.pm25
            FROM weather_records w
            JOIN cities c ON c.id = w.city_id
            LEFT JOIN air_quality_records a ON a.city_id = w.city_id 
                AND DATE(a.recorded_at) = DATE(w.recorded_at)
            ORDER BY c.name, w.recorded_at DESC
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


def get_latest_air_kpis() -> dict:
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


def get_latest_meteo_kpis() -> dict:
    try:
        engine = get_engine()
        sql = f"""
            SELECT DISTINCT ON (c.name)
                c.name AS city,
                a.temp,
                a.feels_like,
                a.weather_description,
                a.icon_weather,
                a.wind_speed,
                a.wind_deg,
                a.humidity
            FROM weather_records a
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
