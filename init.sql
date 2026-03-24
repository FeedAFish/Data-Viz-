CREATE DATABASE algo_db;

\c algo_db

-- Create airflow user for Airflow connections
CREATE USER airflow WITH PASSWORD 'airflow';

GRANT ALL PRIVILEGES ON DATABASE algo_db TO airflow;

-- Cities table
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    country VARCHAR(10) DEFAULT 'FR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Air Quality Records table
CREATE TABLE air_quality_records (
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
    -- is_valid BOOLEAN DEFAULT TRUE,
    -- anomaly BOOLEAN DEFAULT FALSE,
    UNIQUE (city_id, recorded_at)
);

-- Grant all privileges to airflow user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO airflow;