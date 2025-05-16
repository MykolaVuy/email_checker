PROJECT_NAME = email_checker
COMPOSE_FILE = docker-compose.yml

.PHONY: help start stop destroy logs batch check update

help:
	@echo ""
	@echo "📘 Available commands:"
	@echo "  make start                           		🟢 Start the Docker container with build"
	@echo "  make stop                            		🛑 Stop the container"
	@echo "  make destroy                         		⚠️  Remove container, images, volumes"
	@echo "  make logs                            		📄 Tail cron logs"
	@echo "  make batch                           		📬 Run batch email check"
	@echo "  make check email=you@domain.com flag=-S|-F	✅ Check one email (optional add flag=-S for short or flag=-F for full)"
	@echo "  make update                          		🔄 Update the list of disposable email domains"
	@echo "  make help                            		ℹ️  Show this help message"


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
	docker exec -it $(PROJECT_NAME) tail -f /var/log/cron.log

batch:
	docker exec -it $(PROJECT_NAME) check_batch

check:
	@echo "✅ Checking single email: $(email) $(flag)"
	docker exec -it $(PROJECT_NAME) check_email $(email) $(flag)

update:
	docker exec -it $(PROJECT_NAME) update_domains
