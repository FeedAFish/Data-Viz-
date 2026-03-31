set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
COMPOSE_CMD="docker-compose -f ${COMPOSE_FILE}"

start() {
    echo "Starting services..."
    $COMPOSE_CMD up -d
    sleep 3
    echo "Services started successfully."
}

stop() {
    echo "Stopping services..."
    $COMPOSE_CMD down
    echo "Services stopped"
}

restart() {
    stop
    sleep 2
    start
    sleep 5
    $COMPOSE_CMD exec -T postgres psql -U postgres -d algo_db -f /docker-entrypoint-initdb.d/02-init-algo-db.sql
}

shell() {
    local service="${1:-airflow-scheduler}"
    $COMPOSE_CMD exec "$service" /bin/bash
}

build() {
    echo "Building images..."
    $COMPOSE_CMD build
    echo "Build complete"
}

clean() {
    echo "Cleaning up..."
    $COMPOSE_CMD down --rmi all --volumes --remove-orphans
    echo "Removing pgdata directory..."
    rm -rf "${SCRIPT_DIR}/docker/pgdata"
    echo "Cleanup complete"
}

db() {
    echo "Starting database only..."
    $COMPOSE_CMD up -d postgres
    sleep 3
    echo "Database started successfully."
}

afd() {
    echo "Stopping all services except database..."
    $COMPOSE_CMD stop airflow-webserver airflow-scheduler airflow-worker airflow-triggerer airflow-init
    echo "Services stopped. Database is still running."
}

help() {
    echo "Usage: $0 {start|stop|restart|db|stop-services|shell|build|clean|help}"
}

case "${1:-help}" in
    start|up)    start ;;
    stop|down)   stop ;;
    restart)     restart ;;
    db|database) db ;;
    afd|airflowdown) afd ;;
    shell|sh)    shell "$2" ;;
    build)       build ;;
    clean)       clean ;;
    help|-h|--help) help ;;
    *)
        echo "Unknown command: $1"
        help
        exit 1
        ;;
esac
