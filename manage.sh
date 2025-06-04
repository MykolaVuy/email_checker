#!/bin/bash

PROJECT_NAME="email_checker"
COMPOSE_FILE="docker-compose.yml"

start() {
  echo "🟢 Starting the container..."
  docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build
}

stop() {
  echo "🛑 Stopping the container..."
  docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down
}

destroy() {
  echo "⚠️ Attention! You are about to delete the containers, images, volumes of this project: $PROJECT_NAME"
  read -p "Are you sure? (yes/no): " confirm
  if [ "$confirm" == "yes" ]; then
    docker-compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --rmi all --volumes --remove-orphans
    echo "🧹 All related to $PROJECT_NAME has been removed."
  else
    echo "❌ Nothing has been removed."
  fi
}

logs() {
  echo "📄 Following cron logs..."
  docker exec -it "$PROJECT_NAME" tail -f /var/log/cron.log
}

batch() {
  echo "📬 Running batch email check..."
  docker exec -it "$PROJECT_NAME" check_batch
}

check() {
  if [ -z "$2" ]; then
    echo "❌ Please provide an email to check. Usage: ./manage.sh -check someone@example.com [-S|-F]"
    exit 1
  fi
  email="$2"
  flag="$3"

  echo "✅ Checking single email: $email $flag"
  if [ -n "$flag" ]; then
    docker exec -it "$PROJECT_NAME" check_email "$email" "$flag"
  else
    docker exec -it "$PROJECT_NAME" check_email "$email"
  fi
}

update() {
  echo "🔄 Updating disposable domains list..."
  docker exec -it "$PROJECT_NAME" update_domains
}

set_user_config() {
  if [ -z "$2" ]; then
    echo "❌ Usage: ./manage.sh -set_user_config KEY=VALUE"
    exit 1
  fi
  echo "⚙️  Setting user config: $2"
  docker exec -it "$PROJECT_NAME" set_user_config "$2"
}

get_user_config() {
  echo "🧾 Displaying user config..."
  docker exec -it "$PROJECT_NAME" get_user_config
}

help() {
  echo ""
  echo "📘 Available commands:"
  echo "  -start                   🟢 Start the Docker container with build"
  echo "  -stop                    🛑 Stop the container"
  echo "  -destroy                 ⚠️  Remove container, images, volumes"
  echo "  -logs                    📄 Tail cron logs"
  echo "  -batch                   📬 Run batch email check"
  echo "  -check [email] [flag]    ✅ Run single email check (optional: -S/-F)"
  echo "  -update                  🔄 Update list of disposable domains"
  echo "  -set_user_config k=v     ⚙️  Set user config param"
  echo "  -get_user_config         🧾 Show current user config"
  echo "  -help                    ℹ️  Show this help message"
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
  -set_user_config) set_user_config "$@" ;;
  -get_user_config) get_user_config ;;
  -help | *) help ;;
esac
