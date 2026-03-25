from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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


if __name__ == "__main__":
    # Example usage
    sample_records = [
        {
            "city": "Paris",
            "lat": 48.8566,
            "lon": 2.3522,
            "aqi": 75,
            "pm25": 12.5,
            "pm10": 20.0,
            "no2": 15.0,
            "o3": 10.0,
            "timestamp": "2024-06-01T12:00:00",
        }
    ]
    insert_air_quality_records(sample_records)
