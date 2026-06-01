-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS algo_db;

\c algo_db

-- Create airflow user if it doesn't exist
DO $$ BEGIN
    CREATE USER airflow WITH PASSWORD 'airflow';
EXCEPTION WHEN duplicate_object THEN
    ALTER USER airflow WITH PASSWORD 'airflow';
END $$;

GRANT ALL PRIVILEGES ON DATABASE algo_db TO airflow;

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    country VARCHAR(10) DEFAULT 'FR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Air Quality Records - AQI data
CREATE TABLE IF NOT EXISTS air_quality_records (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities (id),
    recorded_at TIMESTAMP NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aqi FLOAT,
    pm25 FLOAT,
    pm10 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    o3 FLOAT,
    co FLOAT,
    UNIQUE (city_id, recorded_at)
);

-- Weather Records - Meteorological data
CREATE TABLE IF NOT EXISTS weather_records (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities (id),
    recorded_at TIMESTAMP NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temp FLOAT,
    feels_like FLOAT,
    wind_speed FLOAT,
    wind_deg FLOAT,
    rain FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    weather_description VARCHAR(100),
    icon_weather VARCHAR(100),
    UNIQUE (city_id, recorded_at)
);

-- Grant all privileges to airflow user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO airflow;