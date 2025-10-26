.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: sync
sync: ## Install production dependencies
	uv sync

.PHONY: run-dev
run-dev: ## Run development server with hot reload
	uv run uvicorn src.prospect-acquisition-agent.main:app --reload

.PHONY: test-unit
test-unit: ## Run unit tests only
	uv run pytest tests/unit/

.PHONY: test-integration
test-integration: ## Run integration tests only
	uv run pytest tests/integration/

.PHONY: test
test: ## Run all tests (unit + integration)
	uv run pytest

.PHONY: lint
lint: ## Run ruff linter
	uv run ruff check .

.PHONY: format
format: ## Format code with ruff
	uv run ruff format .

.PHONY: format-check
format-check: ## Check code formatting
	uv run ruff format --check .
