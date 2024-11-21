#!/bin/bash

# Build Docker images and start services
function start_service {
  echo "Building and starting the Flask app and its services..."
  docker-compose up --build -d
}

# Stop and remove services
function stop_service {
  echo "Stopping and removing the Flask app and its services..."
  docker-compose down
}

# Show logs
function show_logs {
  echo "Showing logs for Flask app and services..."
  docker-compose logs -f
}

# Help message
function show_help {
  echo "Usage: ./endpoint.sh [start|stop|logs]"
}

case $1 in
  start)
    start_service
    ;;
  stop)
    stop_service
    ;;
  logs)
    show_logs
    ;;
  *)
    show_help
    ;;
esac
