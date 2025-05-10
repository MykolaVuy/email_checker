#!/bin/bash

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

function logs() {
  echo "📄 Following cron logs..."
  docker exec -it "$PROJECT_NAME" tail -f /var/log/cron.log
}

function batch() {
  echo "📬 Running batch email check..."
  docker exec -it "$PROJECT_NAME" check_batch
}

function check() {
  if [ -z "$2" ]; then
    echo "❌ Please provide an email to check. Usage: ./manage.sh -check someone@example.com"
    exit 1
  fi
  echo "✅ Checking single email: $2"
  docker exec -it "$PROJECT_NAME" check_email "$2"
}

function update() {
  echo "🔄 Updating disposable domains list..."
  docker exec -it "$PROJECT_NAME" update_domains
}

function help() {
  echo ""
  echo "📘 Available commands:"
  echo "  -start         🟢 Start the container with build"
  echo "  -stop          🛑 Stop the container"
  echo "  -destroy       ⚠️  Remove container, images, volumes"
  echo "  -logs          📄 Tail cron logs"
  echo "  -batch         📬 Run batch email check"
  echo "  -check email   ✅ Run single email check"
  echo "  -update        🔄 Update list of disposable domains"
  echo "  -help          ℹ️  Show this help message"
  echo ""
}

case "$1" in
  -start) start ;;
  -stop) stop ;;
  -destroy) destroy ;;
  -logs) logs ;;
  -batch) batch ;;
  -check) check "$@" ;;
  -update) update ;;
  -help | *) help ;;
esac
