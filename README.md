# GoodAir – Air Quality Visualization Platform

A comprehensive air quality monitoring and visualization platform that collects, processes, and displays real-time air quality data using Airflow, FastAPI, and Dash.

## Project Overview

GoodAir monitors air quality across major French cities, collecting pollutant data and visualizing key performance indicators (KPIs) in an interactive dashboard.

### Features

- **Data Collection**: Automated hourly collection via Airflow DAG
- **API**: FastAPI endpoint for air quality data retrieval
- **Dashboard**: Real-time Dash visualization with auto-refresh
- **Database**: PostgreSQL for persistent data storage
- **Docker Support**: Full Docker Compose setup for easy deployment
- **AQI Visualization**: Color-coded air quality indicators


## Project Structure

```
Viz/
├── api/                    # FastAPI backend
│   ├── __main__.py
│   ├── requirements.txt
│   └── src/
│       ├── main.py        # FastAPI application
│       ├── get.py         # Data retrieval functions
│       └── config/
│           └── settings.py
├── app/                    # Dash dashboard frontend
│   ├── __main__.py
│   ├── requirements.txt
│   └── src/
│       ├── dashboard.py   # Main dashboard layout
│       ├── analytics/
│       │   └── aqicn.py   # API integration
│       └── config/
│           └── settings.py
├── airflow/               # Apache Airflow
│   ├── dags/
│   │   └── data_collect_dag.py
│   ├── logs/
│   └── plugins/
├── docker/                # Docker configuration
│   └── pgdata/           # PostgreSQL data volume
├── docker-compose.yml     # Multi-container orchestration
├── init.sql              # Database initialization script
└── requirements.txt      # Project dependencies
```

## Installation with Docker

### Prerequisites

- Docker & Docker Compose
- Git

### Full Stack (All Services)

1. **Clone the repository**
```bash
git clone https://github.com/FeedAFish/Data-Viz-.git Viz
cd Viz
```

2. **Start all services**

First create a `.env.example` file :

```bash
# API keys
AQICN_TOKEN=demo

# PostgreSQL Configuration
DB_HOST=postgres-database
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=algo_db

# API
API_URL=http://api-service:8000
```

`AQICN_TOKEN` can be generate at https://aqicn.org/api/


```bash
./docker.sh restart
```

Services will be available at:
- **Dashboard**: http://localhost:8050
- **API**: http://localhost:8000
- **Airflow UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432 (user: postgres, password: postgres)

## Installation locally

```bash
pip install -r api/requirements.txt
pip install -r app/requirements.txt
```

Required : Postgres Database required or other database but modifications required. You can just launch the Postgres DB service with docker by :

```bash
./docker.sh db
```

Update manually by using Python :

```python
from airflow.dags.data_collect_dag import collect_and_insert_air_quality_data

collect_and_insert_air_quality_data()
```

**Terminal 1 - API Server**
```bash
python api
```

**Terminal 2 - Dashboard**
```bash
python app
```

## Troubleshooting

### API Service Unhealthy
- Ensure PostgreSQL is running and accessible
- Check environment variables match your setup
- Verify database is initialized with `init.sql`

### Dashboard Shows No Data
- Ensure API service is healthy
- Check API_URL environment variable is correct
- Verify database contains data (check Airflow DAG execution)

## Dependencies Used

- **Backend**: FastAPI, SQLAlchemy, psycopg2
- **Frontend**: Dash
- **Data Pipeline**: Apache Airflow
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## License

See LICENSE file for details.

## Support

For issues or questions, please create an issue in the repository.
