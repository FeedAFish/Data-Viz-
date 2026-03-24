import os
from dotenv import load_dotenv

load_dotenv()

# ── Base de données PostgreSQL ──────────────────────────────────────────────
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "algo_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── API Keys ────────────────────────────────────────────────────────────────
AQICN_TOKEN = os.getenv("AQICN_TOKEN", "demo")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo")

# ── Villes surveillées ──────────────────────────────────────────────────────
CITIES = [
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "Lyon", "lat": 45.7640, "lon": 4.8357},
    {"name": "Marseille", "lat": 43.2965, "lon": 5.3698},
    {"name": "Toulouse", "lat": 43.6047, "lon": 1.4442},
    {"name": "Bordeaux", "lat": 44.8378, "lon": -0.5792},
    {"name": "Nantes", "lat": 47.2184, "lon": -1.5536},
    {"name": "Strasbourg", "lat": 48.5734, "lon": 7.7521},
    {"name": "Lille", "lat": 50.6292, "lon": 3.0573},
]
