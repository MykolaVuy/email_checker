PROJECT_NAME = email_checker
COMPOSE_FILE = docker-compose.yml

.PHONY: help start stop destroy logs batch check update set_user_config get_user_config

help:
	@echo ""
	@echo "📘 Available commands:"
	@echo "  make start                             🟢 Start the Docker container with build"
	@echo "  make stop                              🛑 Stop the container"
	@echo "  make destroy                           ⚠️  Remove container, images, volumes"
	@echo "  make logs                              📄 Tail cron logs"
	@echo "  make batch                             📬 Run batch email check"
	@echo "  make check email=you@domain.com flag=-S|-F  ✅ Check one email (optional: -S for short, -F for full)"
	@echo "  make update                            🔄 Update list of disposable email domains"
	@echo "  make set_user_config key=VAL           ⚙️  Set a single user config parameter"
	@echo "  make get_user_config                   🧾 Show current user config"
	@echo "  make help                              ℹ️  Show this help message"
	@echo ""

start:
	@echo "🟢 Starting the container..."
	docker-compose -p $(PROJECT_NAME) -f $(COMPOSE_FILE) up -d --build

stop:
	@echo "🛑 Stopping the container..."
	docker-compose -p $(PROJECT_NAME) -f $(COMPOSE_FILE) down

destroy:
	@echo "⚠️  Attention! You are about to delete everything related to $(PROJECT_NAME)."
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose -p $(PROJECT_NAME) -f $(COMPOSE_FILE) down --rmi all --volumes --remove-orphans; \
		echo "🧹 Project $(PROJECT_NAME) has been fully removed."; \
	else \
		echo "❌ Nothing has been removed."; \
	fi

logs:
	@echo "📄 Following cron logs..."
	docker exec -it $(PROJECT_NAME) tail -f /var/log/cron.log

batch:
	@echo "📬 Running batch email check..."
	docker exec -it $(PROJECT_NAME) check_batch

check:
	@echo "✅ Checking single email: $(email) $(flag)"
	docker exec -it $(PROJECT_NAME) check_email $(email) $(flag)

update:
	@echo "🔄 Updating disposable domains list..."
	docker exec -it $(PROJECT_NAME) update_domains

set_user_config:
	@if [ -z "$(key)" ]; then \
		echo "❌ Please provide a key=value. Example: make set_user_config key=USE_EHLO=True"; \
	else \
		echo "⚙️  Setting user config: $(key)"; \
		docker exec -it $(PROJECT_NAME) set_user_config $(key); \
	fi

get_user_config:
	@echo "🧾 Displaying current user config..."
	docker exec -it $(PROJECT_NAME) get_user_config
