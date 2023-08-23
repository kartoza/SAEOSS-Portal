export COMPOSE_FILE=docker/docker-compose.yml
export COMPOSE_PROJECT_NAME=saeoss
DATE := $(shell date "+%Y_%m_%d_%H_%M_%S")
OPTS :=

db-backup: ## Create database backup
	docker-compose exec ckan-db su - postgres -c "pg_dumpall" | gzip -9 > latest-$(DATE).sql.gz