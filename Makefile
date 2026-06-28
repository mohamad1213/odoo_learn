WEB_DB_NAME := odoo_development

DOCKER := docker
DOCKER_COMPOSE := $(DOCKER) compose

CONTAINER_ODOO := odoo
CONTAINER_DB := odoo-postgres

.PHONY: help start stop restart console psql logs

help:
	@echo "Available targets"
	@echo "  start        Start the compose stack"
	@echo "  stop         Stop the compose stack"
	@echo "  restart      Restart the compose stack"
	@echo "  console      Odoo interactive shell"
	@echo "  psql         PostgreSQL interactive shell"
	@echo "  logs odoo    Logs the Odoo container"
	@echo "  logs db      Logs the PostgreSQL container"
	@echo "  addons <addon_name>  restart odoo with the specified addon enabled"

start:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

console:
	$(DOCKER) exec -it $(CONTAINER_ODOO) \
		odoo shell \
		--db_host=$(CONTAINER_DB) \
		-d $(WEB_DB_NAME)

psql:
	$(DOCKER) exec -it $(CONTAINER_DB) \
		psql -U $(CONTAINER_ODOO) -d $(WEB_DB_NAME)


define log_target
	@if [ "$(TARGET)" = "odoo" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_ODOO); \
	elif [ "$(TARGET)" = "db" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_DB); \
	else \
		echo  "invalid logs target: $(TARGET) Use 'make logs odoo' or 'make logs db'."; \
	fi
endef

logs:
	$(call log_target, $(word 2, $(MAKECMDGOALS)))

define upgrade_addons
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO) -u $(1)
endef

addon: restart
	@sleep 5
	@$(call upgrade_addons, $(word 2, $(MAKECMDGOALS)))

.PHONY:  start stop restart console psql logs odoo db