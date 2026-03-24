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

case "${1:-help}" in
    start|up)    start ;;
    stop|down)   stop ;;
    restart)     restart ;;
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
