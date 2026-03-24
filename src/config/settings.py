import os
from dotenv import load_dotenv

load_dotenv()

# ── Base de données PostgreSQL ──────────────────────────────────────────────
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME     = os.getenv("DB_NAME", "algo_db")
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── API Keys ────────────────────────────────────────────────────────────────
AQICN_TOKEN         = os.getenv("AQICN_TOKEN", "demo")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo")

