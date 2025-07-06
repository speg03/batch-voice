# Makefile for batch-voice project

.PHONY: help setup up down logs clean install test lint

# Default target
help:
	@echo "Available commands:"
	@echo "  setup     - Setup LocalStack resources"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs"
	@echo "  clean     - Clean up volumes and containers"
	@echo "  install   - Install dependencies"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"

# Setup LocalStack resources
setup:
	@echo "Setting up LocalStack resources..."
	docker-compose up -d localstack
	@sleep 10
	./scripts/setup-localstack.sh

# Start all services
up:
	docker-compose up -d
	@echo "Services started. Access:"
	@echo "  - LocalStack: http://localhost:4566"
	@echo "  - API: http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"

# Start infrastructure only
up-infra:
	docker-compose up -d localstack

# Start with full application
up-full:
	docker-compose --profile full up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up
clean:
	docker-compose down -v
	docker-compose rm -f
	docker volume prune -f

# Install dependencies (placeholder)
install:
	@echo "Installing dependencies..."
	@echo "Run 'make install-backend' and 'make install-frontend' when ready"

# Install backend dependencies
install-backend:
	cd backend && pip install -r requirements.txt

# Install frontend dependencies
install-frontend:
	cd frontend && npm install

# Run tests (placeholder)
test:
	@echo "Running tests..."
	@echo "Implement test commands for backend and frontend"

# Run linting (placeholder)
lint:
	@echo "Running linting..."
	@echo "Implement lint commands for backend and frontend"

# Development commands
dev-api:
	docker-compose up -d localstack
	@echo "Infrastructure started. Run your API locally with:"
	@echo "cd backend && uvicorn main:app --reload"

dev-frontend:
	@echo "Run your frontend locally with:"
	@echo "cd frontend && npm run dev"

# Database operations
db-migrate:
	@echo "Running database migrations..."
	@echo "Implement migration commands"

# LocalStack operations
localstack-status:
	@echo "LocalStack status:"
	curl -s http://localhost:4566/health | jq .

localstack-reset:
	docker-compose restart localstack
	@sleep 10
	./scripts/setup-localstack.sh