from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.collect.meteo import collect_all_meteo
from config.settings import DATABASE_URL

# Create engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def insert_air_quality_records(records: list[dict]) -> None:
    session = SessionLocal()
    try:
        for record in records:
            city_result = session.execute(
                text("SELECT id FROM cities WHERE name = :city_name"),
                {"city_name": record["city"]},
            )
            city_row = city_result.fetchone()

            if not city_row:
                # Insert city if it doesn't exist
                session.execute(
                    text(
                        "INSERT INTO cities (name, latitude, longitude) "
                        "VALUES (:name, :lat, :lon) "
                        "ON CONFLICT (name) DO NOTHING"
                    ),
                    {
                        "name": record["city"],
                        "lat": record.get("lat"),
                        "lon": record.get("lon"),
                    },
                )
                session.commit()
                city_result = session.execute(
                    text("SELECT id FROM cities WHERE name = :city_name"),
                    {"city_name": record["city"]},
                )
                city_row = city_result.fetchone()

            city_id = city_row[0]

            # Insert air quality record
            session.execute(
                text(
                    "INSERT INTO air_quality_records "
                    "(city_id, recorded_at, aqi, pm25, pm10, no2, o3) "
                    "VALUES (:city_id, :recorded_at, :aqi, :pm25, :pm10, :no2, :o3) "
                    "ON CONFLICT (city_id, recorded_at) DO UPDATE SET "
                    "aqi = EXCLUDED.aqi, pm25 = EXCLUDED.pm25, "
                    "pm10 = EXCLUDED.pm10, no2 = EXCLUDED.no2, o3 = EXCLUDED.o3"
                ),
                {
                    "city_id": city_id,
                    "recorded_at": record["timestamp"],
                    "aqi": record.get("aqi"),
                    "pm25": record.get("pm25"),
                    "pm10": record.get("pm10"),
                    "no2": record.get("no2"),
                    "o3": record.get("o3"),
                },
            )

        session.commit()
        print(f"Successfully inserted {len(records)} air quality records.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting air quality records: {e}")
        raise
    finally:
        session.close()


def insert_meteo_records(records: list[dict]) -> None:
    session = SessionLocal()
    try:
        for e, record in enumerate(records):
            print(e)
            city_result = session.execute(
                text("SELECT id FROM cities WHERE name = :city_name"),
                {"city_name": record["city"]},
            )
            city_row = city_result.fetchone()

            if not city_row:
                # Insert city if it doesn't exist
                session.execute(
                    text(
                        "INSERT INTO cities (name, latitude, longitude) "
                        "VALUES (:name, :lat, :lon) "
                        "ON CONFLICT (name) DO NOTHING"
                    ),
                    {
                        "name": record["city"],
                        "lat": record.get("lat"),
                        "lon": record.get("lon"),
                    },
                )
                session.commit()
                city_result = session.execute(
                    text("SELECT id FROM cities WHERE name = :city_name"),
                    {"city_name": record["city"]},
                )
                city_row = city_result.fetchone()

            city_id = city_row[0]

            # Insert weather record
            session.execute(
                text(
                    "INSERT INTO weather_records "
                    "(city_id, recorded_at, temp, feels_like, wind_speed, wind_deg, rain, humidity, pressure, weather_description, icon_weather) "
                    "VALUES (:city_id, :recorded_at, :temp, :feels_like, :wind_speed, :wind_deg, :rain, :humidity, :pressure, :weather_description, :icon_weather) "
                    "ON CONFLICT (city_id, recorded_at) DO UPDATE SET "
                    "temp = EXCLUDED.temp, feels_like = EXCLUDED.feels_like, "
                    "wind_speed = EXCLUDED.wind_speed, wind_deg = EXCLUDED.wind_deg, rain = EXCLUDED.rain, "
                    "humidity = EXCLUDED.humidity, pressure = EXCLUDED.pressure, weather_description = EXCLUDED.weather_description, icon_weather = EXCLUDED.icon_weather"
                ),
                {
                    "city_id": city_id,
                    "recorded_at": record["timestamp"],
                    "temp": record.get("temp"),
                    "feels_like": record.get("feels_like"),
                    "wind_speed": record.get("wind_speed"),
                    "wind_deg": record.get("wind_deg"),
                    "rain": record.get("rain"),
                    "humidity": record.get("humidity"),
                    "pressure": record.get("pressure"),
                    "weather_description": record.get("weather"),
                    "icon_weather": record.get("icon_weather"),
                },
            )

        session.commit()
        print(f"Successfully inserted {len(records)} weather records.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting weather records: {e}")
        raise
    finally:
        session.close()
