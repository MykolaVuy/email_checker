#!/bin/bash

# befor first run
# chmod +x manage.sh

# usage: ./manage.sh [-start | -stop | -destroy]

PROJECT_NAME="email_checker"
COMPOSE_FILE="docker-compose.yml"

function start() {
  echo "🟢 Starting the container..."
  docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build
}

function stop() {
  echo "🛑 Stopping the container..."
  docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down
}

function destroy() {
  echo "⚠️ Attention! You are about to delete the containers, images, volumes of this project: $PROJECT_NAME"
  read -p "Are you sure? (yes/no): " confirm
  if [ "$confirm" == "yes" ]; then
    docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --rmi all --volumes --remove-orphans
    echo "🧹 All related to $PROJECT_NAME has been removed."
  else
    echo "❌ Nothing has been removed."
  fi
}

case "$1" in
  -start)
    start
    ;;
  -stop)
    stop
    ;;
  -destroy)
    destroy
    ;;
  *)
    echo "Usage: ./manage.sh [-start | -stop | -destroy]"
    ;;
esac
