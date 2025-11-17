#!/bin/bash
# Health check script for all services

set -e

echo "=== EEMCARS Health Check ==="

# Check PostgreSQL
echo -n "PostgreSQL: "
if docker-compose exec postgres pg_isready -U eemcars > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Not responding"
fi

# Check Redis
echo -n "Redis: "
if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Not responding"
fi

# Check Backend
echo -n "Backend API: "
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Not responding"
fi

# Check Frontend
echo -n "Frontend: "
if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Healthy"
else
    echo "✗ Not responding"
fi

echo ""
echo "Health check complete!"
