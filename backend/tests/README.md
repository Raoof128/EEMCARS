# EEMCARS Backend Tests

Comprehensive test suite for the EEMCARS backend API.

## Test Structure

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── test_auth.py               # Authentication tests
├── test_scoring.py            # Scoring engine tests
├── test_api_controls.py       # Controls API tests
├── test_api_assets.py         # Assets API tests (to be added)
├── test_api_evidence.py       # Evidence API tests (to be added)
├── test_api_assessments.py    # Assessments API tests (to be added)
├── test_api_remediation.py    # Remediation API tests (to be added)
├── test_drift_detection.py    # Drift detection tests (to be added)
├── test_celery_tasks.py       # Celery task tests (to be added)
└── README.md                  # This file
```

## Running Tests

### Run All Tests
```bash
# From backend directory
pytest

# With coverage
pytest --cov=app --cov-report=html --cov-report=term

# With verbose output
pytest -v

# With output (print statements visible)
pytest -s
```

### Run Specific Tests
```bash
# Run specific file
pytest tests/test_auth.py

# Run specific test class
pytest tests/test_auth.py::TestAuth

# Run specific test
pytest tests/test_auth.py::TestAuth::test_login_success

# Run tests matching pattern
pytest -k "login"
```

### Run Tests by Marker
```bash
# Run async tests only
pytest -m asyncio

# Run integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Database

Tests use a separate test database:
- **Database:** `eemcars_test`
- **URL:** `postgresql+asyncpg://test:test@localhost:5432/eemcars_test`

### Setup Test Database
```bash
# Create test database
psql -U postgres -c "CREATE DATABASE eemcars_test;"
psql -U postgres -c "CREATE USER test WITH PASSWORD 'test';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE eemcars_test TO test;"
```

## Test Fixtures

### Database Fixtures
- `db`: Fresh database session for each test
- `test_user`: Standard test user (SecOps role)
- `admin_user`: Admin test user
- `auditor_user`: Auditor test user

### Authentication Fixtures
- `test_token`: JWT token for test_user
- `admin_token`: JWT token for admin_user
- `auditor_token`: JWT token for auditor_user

### Client Fixtures
- `client`: Unauthenticated test client
- `auth_client`: Authenticated test client (test_user)
- `admin_client`: Authenticated admin test client

### Example Usage
```python
def test_example(auth_client: TestClient):
    """Test with authenticated client."""
    response = auth_client.get("/api/v1/controls")
    assert response.status_code == 200
```

## Writing Tests

### Test File Structure
```python
"""
Tests for [module name].
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
class TestModuleName:
    """Test [module name]."""

    def test_feature_success(self, auth_client: TestClient):
        """Test successful [feature]."""
        response = auth_client.get("/api/v1/endpoint")
        assert response.status_code == 200
        # More assertions...

    def test_feature_failure(self, auth_client: TestClient):
        """Test [feature] failure case."""
        response = auth_client.post("/api/v1/endpoint", json={})
        assert response.status_code == 400
        # More assertions...
```

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `TestClassName`
- Test methods: `test_feature_scenario`

### Examples
- `test_login_success`: Feature is "login", scenario is "success"
- `test_create_control_duplicate`: Feature is "create_control", scenario is "duplicate"
- `test_score_control_no_evidence`: Feature is "score_control", scenario is "no_evidence"

## Test Coverage

### Target Coverage
- **Overall:** 80%+
- **Core modules (scoring, auth):** 90%+
- **API endpoints:** 85%+

### Generate Coverage Report
```bash
# HTML report (detailed, recommended)
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Terminal report
pytest --cov=app --cov-report=term

# Coverage report missing lines
pytest --cov=app --cov-report=term-missing
```

### Coverage Exceptions
Some code may be excluded from coverage requirements:
- Abstract base classes
- Defensive error handling (should never happen)
- Development/debug code
- External integrations (mocked in tests)

## Test Categories

### Unit Tests
Test individual functions/methods in isolation.
```python
def test_password_hashing():
    """Test password hashing function."""
    from app.core.security import get_password_hash, verify_password

    password = "testpassword123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)
```

### Integration Tests
Test API endpoints and database interactions.
```python
def test_create_and_retrieve_control(auth_client: TestClient):
    """Test creating and retrieving a control."""
    # Create
    response = auth_client.post("/api/v1/controls", json={...})
    assert response.status_code == 201
    control_id = response.json()["control_id"]

    # Retrieve
    response = auth_client.get(f"/api/v1/controls/{control_id}")
    assert response.status_code == 200
```

### E2E Tests
Test complete workflows across multiple endpoints.
```python
async def test_assessment_workflow(auth_client: TestClient, db: AsyncSession):
    """Test complete assessment workflow."""
    # 1. Create assets
    # 2. Upload evidence
    # 3. Run assessment
    # 4. Check results
    # 5. Verify drift detection
```

## Mocking

### Mock External Services
```python
from unittest.mock import patch, MagicMock

@patch('app.integrations.defender.DefenderClient')
def test_evidence_collection(mock_defender, auth_client):
    """Test evidence collection from Defender."""
    mock_defender.return_value.get_devices.return_value = [...]

    response = auth_client.post("/api/v1/evidence/collect")
    assert response.status_code == 202
```

### Mock Celery Tasks
```python
@patch('app.tasks.assessment.run_assessment.delay')
def test_trigger_assessment(mock_task, auth_client):
    """Test triggering assessment task."""
    response = auth_client.post("/api/v1/assessments/run")
    assert mock_task.called
```

## Common Patterns

### Test Authentication Required
```python
def test_endpoint_requires_auth(client: TestClient):
    """Test endpoint requires authentication."""
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
```

### Test RBAC
```python
def test_admin_only_endpoint(auth_client: TestClient):
    """Test endpoint requires admin role."""
    response = auth_client.post("/api/v1/admin/action")
    assert response.status_code == 403  # SecOps user forbidden

def test_admin_endpoint_as_admin(admin_client: TestClient):
    """Test endpoint allows admin role."""
    response = admin_client.post("/api/v1/admin/action")
    assert response.status_code == 200  # Admin allowed
```

### Test Validation
```python
def test_create_with_invalid_data(auth_client: TestClient):
    """Test validation errors."""
    response = auth_client.post("/api/v1/controls", json={
        "control_id": "",  # Invalid: empty
        "pillar": "invalid_pillar",  # Invalid: not in enum
    })
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("control_id" in e["loc"] for e in errors)
    assert any("pillar" in e["loc"] for e in errors)
```

### Test Pagination
```python
def test_list_with_pagination(auth_client: TestClient):
    """Test list endpoint pagination."""
    response = auth_client.get("/api/v1/controls?skip=10&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
```

## Debugging Tests

### Run with PDB
```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on error
pytest --pdb-trace
```

### Print Debugging
```bash
# Show print statements
pytest -s

# Show print statements and verbose output
pytest -sv
```

### Show Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Pushes to main/develop
- Nightly builds

### CI Requirements
- All tests must pass
- Coverage must be ≥80%
- No linting errors
- No security vulnerabilities

### GitHub Actions Workflow
See `.github/workflows/test.yml`

## Performance Testing

### Load Testing (Locust)
```bash
# Install
pip install locust

# Run load test
cd tests/load
locust -f locustfile.py
```

### Benchmark Tests
```python
import pytest

@pytest.mark.benchmark
def test_scoring_performance(benchmark, scoring_engine):
    """Benchmark scoring performance."""
    result = benchmark(scoring_engine.score_control, "E8-AC-L2-REQ1", "asset-1")
    assert result is not None
```

## Security Testing

### Test SQL Injection
```python
def test_sql_injection_prevention(auth_client: TestClient):
    """Test SQL injection is prevented."""
    response = auth_client.get("/api/v1/controls?pillar='; DROP TABLE controls; --")
    assert response.status_code in [200, 400]  # Should not execute SQL
    # Verify database still intact
```

### Test XSS
```python
def test_xss_prevention(auth_client: TestClient):
    """Test XSS is prevented."""
    response = auth_client.post("/api/v1/controls", json={
        "control_id": "TEST",
        "name": "<script>alert('XSS')</script>",
    })
    # Verify response escapes HTML
```

## Troubleshooting

### Tests Hang
- Check for missing `await` in async tests
- Check for infinite loops
- Use `pytest --timeout=10` to fail hanging tests

### Database Errors
- Ensure test database exists
- Check database permissions
- Verify database is not locked
- Clear test database: `psql -U postgres -c "DROP DATABASE eemcars_test; CREATE DATABASE eemcars_test;"`

### Import Errors
- Ensure `PYTHONPATH` includes backend directory
- Check `__init__.py` files exist
- Verify dependencies installed: `pip install -r requirements-dev.txt`

### Fixture Errors
- Check fixture scope (session/module/function)
- Verify fixture dependencies
- Use `pytest --fixtures` to list available fixtures

## Best Practices

1. **Test Isolation:** Each test should be independent
2. **Descriptive Names:** Test names should describe what they test
3. **Arrange-Act-Assert:** Structure tests clearly
4. **One Assert Per Test:** Test one thing at a time (guideline, not rule)
5. **Fast Tests:** Keep tests fast (<1s per test ideally)
6. **Meaningful Assertions:** Assert what matters, not implementation details
7. **Test Edge Cases:** Happy path + error cases + edge cases
8. **Mock External Services:** Don't depend on external APIs
9. **Clean Up:** Use fixtures for setup/teardown
10. **Document Complex Tests:** Add docstrings and comments

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Library Best Practices](https://testing-library.com/docs/guiding-principles/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
