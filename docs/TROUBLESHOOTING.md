# EEMCARS Troubleshooting Guide

## Common Issues and Solutions

### Database Connection Issues

**Problem:** Backend cannot connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL container is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection string in .env file
cat .env | grep DATABASE_URL
```

---

### Backend Not Starting

**Problem:** Backend container fails to start or crashes

**Solutions:**

1. **Check logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Verify dependencies:**
   ```bash
   docker-compose exec backend pip list
   ```

3. **Check environment variables:**
   ```bash
   docker-compose exec backend env | grep -E 'DATABASE|REDIS|SECRET'
   ```

4. **Rebuild container:**
   ```bash
   docker-compose build backend
   docker-compose up -d backend
   ```

---

### Frontend Build Errors

**Problem:** Frontend fails to build or start

**Solutions:**

1. **Clear node_modules and reinstall:**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Check for missing dependencies:**
   ```bash
   npm install
   ```

3. **Rebuild Docker image:**
   ```bash
   docker-compose build frontend
   ```

---

### Agent Connection Issues

**Problem:** Agents cannot connect to backend

**Solutions:**

1. **Verify backend is accessible:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check agent configuration:**
   - Windows: Verify `$ServerUrl` parameter
   - Linux: Check `EEMCARS_SERVER_URL` environment variable

3. **Check firewall rules:**
   - Ensure port 8000 is accessible
   - Check network connectivity

4. **Verify agent authentication:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/agents/register \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"test-agent","asset_id":"...","agent_version":"1.0.0","platform":"Linux","capabilities":{}}'
   ```

---

### Database Migration Errors

**Problem:** Database schema is out of sync

**Solutions:**

1. **Reset database (DEV ONLY - DESTROYS DATA):**
   ```bash
   docker-compose down -v
   docker-compose up -d postgres
   docker-compose exec postgres psql -U eemcars -d eemcars -f /docker-entrypoint-initdb.d/schema.sql
   ```

2. **Load demo data:**
   ```bash
   docker-compose exec backend python -m app.demo.seed_data
   ```

---

### Redis Connection Errors

**Problem:** Backend cannot connect to Redis

**Solutions:**

1. **Check Redis status:**
   ```bash
   docker-compose exec redis redis-cli ping
   ```

2. **Verify Redis URL:**
   ```bash
   echo $REDIS_URL
   ```

3. **Restart Redis:**
   ```bash
   docker-compose restart redis
   ```

---

### Celery Worker Not Processing Tasks

**Problem:** Background tasks are not being executed

**Solutions:**

1. **Check Celery worker logs:**
   ```bash
   docker-compose logs celery-worker
   ```

2. **Verify Redis connection:**
   ```bash
   docker-compose exec celery-worker python -c "from app.core.celery import celery_app; print(celery_app.control.inspect().active())"
   ```

3. **Restart Celery worker:**
   ```bash
   docker-compose restart celery-worker
   ```

---

### Authentication Errors

**Problem:** Cannot login to the dashboard

**Solutions:**

1. **Verify demo credentials:**
   - Username: `admin`
   - Password: `DemoUser123!`

2. **Check if user exists in database:**
   ```bash
   docker-compose exec postgres psql -U eemcars -d eemcars -c "SELECT username, role FROM users;"
   ```

3. **Recreate demo users:**
   ```bash
   docker-compose exec backend python -m app.demo.seed_data
   ```

---

### Docker Compose Issues

**Problem:** Services fail to start with docker-compose

**Solutions:**

1. **Check Docker daemon:**
   ```bash
   docker info
   ```

2. **Verify docker-compose.yml syntax:**
   ```bash
   docker-compose config
   ```

3. **Check port conflicts:**
   ```bash
   # Check if ports 3000, 5432, 6379, 8000 are in use
   lsof -i :3000
   lsof -i :5432
   lsof -i :6379
   lsof -i :8000
   ```

4. **Clean up and restart:**
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up -d
   ```

---

### Performance Issues

**Problem:** Slow response times or high resource usage

**Solutions:**

1. **Check resource usage:**
   ```bash
   docker stats
   ```

2. **Optimize database:**
   ```bash
   docker-compose exec postgres psql -U eemcars -d eemcars -c "VACUUM ANALYZE;"
   ```

3. **Clear Redis cache:**
   ```bash
   docker-compose exec redis redis-cli FLUSHDB
   ```

4. **Increase Docker resources:**
   - Increase memory limit in Docker settings
   - Allocate more CPU cores

---

### API 500 Errors

**Problem:** Backend API returns 500 Internal Server Error

**Solutions:**

1. **Check backend logs:**
   ```bash
   docker-compose logs backend --tail=100
   ```

2. **Enable debug mode:**
   ```bash
   # In .env file
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

3. **Check database connectivity:**
   ```bash
   docker-compose exec backend python -c "from app.db.database import engine; print(engine)"
   ```

---

### Azure Deployment Issues

**Problem:** Terraform deployment fails

**Solutions:**

1. **Verify Azure credentials:**
   ```bash
   az account show
   az account list-locations -o table | grep australia
   ```

2. **Check resource quotas:**
   ```bash
   az vm list-usage --location australiaeast -o table
   ```

3. **Validate Terraform:**
   ```bash
   cd terraform
   terraform validate
   terraform plan
   ```

4. **Check state file:**
   ```bash
   terraform state list
   ```

---

## Getting Help

If you're still experiencing issues:

1. **Check logs:**
   ```bash
   docker-compose logs --tail=100
   ```

2. **Run health check:**
   ```bash
   ./scripts/check-health.sh
   ```

3. **GitHub Issues:** https://github.com/yourusername/eemcars/issues

4. **Documentation:** Review the [README](../README.md) and [Deployment Guide](DEPLOYMENT.md)

---

## Debugging Tips

### Enable Verbose Logging

```bash
# Backend
export LOG_LEVEL=DEBUG

# Docker Compose
docker-compose logs -f --tail=100
```

### Access Container Shell

```bash
# Backend
docker-compose exec backend /bin/bash

# PostgreSQL
docker-compose exec postgres psql -U eemcars -d eemcars

# Redis
docker-compose exec redis redis-cli
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get controls
curl http://localhost:8000/api/v1/controls/

# Login
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=DemoUser123!"
```

### Monitor Resource Usage

```bash
# Docker stats
docker stats

# System resources
htop

# Network connections
netstat -tulpn | grep -E '3000|5432|6379|8000'
```
