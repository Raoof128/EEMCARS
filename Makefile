.PHONY: help install dev start stop test clean lint format docker-build docker-up docker-down seed

help:
	@echo "EEMCARS - Essential Eight Assessment Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make dev            - Start development servers"
	@echo "  make start          - Start production services with Docker"
	@echo "  make stop           - Stop all services"
	@echo "  make test           - Run all tests"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code"
	@echo "  make clean          - Clean temporary files"
	@echo "  make seed           - Seed database with demo data"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Start Docker Compose services"
	@echo "  make docker-down    - Stop Docker Compose services"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Done!"

dev:
	@echo "Starting development servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	docker-compose up postgres redis -d
	@echo "Waiting for database to be ready..."
	sleep 5
	cd backend && uvicorn app.main:app --reload &
	cd frontend && npm start

start:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs"

stop:
	docker-compose down
	@echo "Services stopped!"

test:
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test -- --watchAll=false

lint:
	@echo "Linting backend..."
	cd backend && flake8 app
	@echo "Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "Formatting backend code..."
	cd backend && black app
	@echo "Formatting frontend code..."
	cd frontend && npm run format

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Done!"

seed:
	@echo "Seeding database with demo data..."
	docker-compose exec backend python -m app.demo.seed_data
	@echo "Demo data loaded!"
	@echo "Login with: admin / DemoUser123!"

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker Compose services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	sleep 10
	@echo "Services are up!"
	@echo "Run 'make seed' to load demo data"

docker-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down
	@echo "Services stopped!"

.DEFAULT_GOAL := help
