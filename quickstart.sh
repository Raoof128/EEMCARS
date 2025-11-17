#!/bin/bash
# EEMCARS Quick Start Script

set -e

echo "================================================================"
echo "  EEMCARS - Essential Eight Assessment Platform"
echo "  Quick Start Installation"
echo "================================================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Build and start services
echo ""
echo "Building Docker images... (this may take a few minutes)"
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 15

# Check if services are healthy
echo ""
echo "Checking service health..."

# Check PostgreSQL
echo -n "  PostgreSQL: "
if docker-compose exec -T postgres pg_isready -U eemcars > /dev/null 2>&1; then
    echo "✓"
else
    echo "✗ (may need more time)"
fi

# Check Redis
echo -n "  Redis: "
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✓"
else
    echo "✗ (may need more time)"
fi

# Check Backend
echo -n "  Backend API: "
retries=0
max_retries=30
while [ $retries -lt $max_retries ]; do
    if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓"
        break
    fi
    retries=$((retries + 1))
    sleep 1
done

if [ $retries -eq $max_retries ]; then
    echo "✗ (timeout)"
fi

# Seed demo data
echo ""
echo "Loading demo data..."
docker-compose exec -T backend python -m app.demo.seed_data || echo "⚠ Demo data seeding failed (database may not be ready yet)"

echo ""
echo "================================================================"
echo "  Installation Complete!"
echo "================================================================"
echo ""
echo "Access the platform:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/api/docs"
echo ""
echo "Demo Credentials:"
echo "  Username: admin"
echo "  Password: DemoUser123!"
echo ""
echo "Useful Commands:"
echo "  docker-compose logs -f          # View logs"
echo "  docker-compose stop             # Stop services"
echo "  docker-compose down             # Stop and remove containers"
echo "  make help                       # See all available commands"
echo ""
echo "================================================================"
