# EEMCARS Testing Guide

Comprehensive testing guide for EEMCARS backend and frontend.

## Overview

EEMCARS uses a comprehensive testing strategy:
- **Backend:** pytest with async support
- **Frontend:** Jest with React Testing Library
- **Integration:** End-to-end API tests
- **Coverage Target:** 80%+ overall, 90%+ for core modules

## Quick Start

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # macOS
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run tests (interactive)
npm test

# Run tests with coverage
npm run test:coverage

# Run tests for CI (non-interactive)
npm run test:ci
```

## Backend Testing

### Test Structure

```
backend/tests/
├── conftest.py                 # Pytest configuration and fixtures
├── test_auth.py               # Authentication tests
├── test_scoring.py            # Scoring engine tests
├── test_api_controls.py       # Controls API tests
├── test_api_assets.py         # Assets API tests
├── test_api_evidence.py       # Evidence API tests
├── test_api_assessments.py    # Assessments API tests
├── test_api_remediation.py    # Remediation API tests
├── test_drift_detection.py    # Drift detection tests
├── test_celery_tasks.py       # Celery task tests
└── README.md                  # Testing documentation
```

### Writing Backend Tests

#### Example: API Endpoint Test
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
class TestControlsAPI:
    """Test controls API endpoints."""

    def test_list_controls(self, auth_client: TestClient):
        """Test listing all controls."""
        response = auth_client.get("/api/v1/controls")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_control_as_admin(self, admin_client: TestClient):
        """Test creating a control as admin."""
        control_data = {
            "control_id": "E8-TEST-L1-REQ1",
            "pillar": "application_control",
            "name": "Test Control",
            "description": "Test description",
            "maturity_level": 1,
        }
        response = admin_client.post("/api/v1/controls", json=control_data)
        assert response.status_code == 201
```

#### Example: Scoring Engine Test
```python
import pytest
from app.scoring.engine import ScoringEngine

@pytest.mark.asyncio
class TestScoringEngine:
    """Test the Essential Eight scoring engine."""

    async def test_score_control_compliant(
        self,
        scoring_engine: ScoringEngine,
        test_control,
        test_asset,
        db
    ):
        """Test scoring a compliant control."""
        # Create compliant evidence
        evidence = Evidence(
            control_id=test_control.id,
            asset_id=test_asset.id,
            data={"applocker_enabled": True},
            validation_status="validated",
        )
        db.add(evidence)
        await db.commit()

        # Score
        result = await scoring_engine.score_control(
            control_id=test_control.control_id,
            asset_id=test_asset.id,
        )

        assert result["achieved_level"] >= 2
```

### Running Backend Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_auth.py

# Specific test
pytest tests/test_auth.py::TestAuth::test_login_success

# With coverage
pytest --cov=app --cov-report=html

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "login"

# Run only async tests
pytest -m asyncio
```

### Backend Test Fixtures

Available fixtures (see `conftest.py`):

- `db`: Database session (fresh for each test)
- `test_user`: Standard user (SecOps role)
- `admin_user`: Admin user
- `auditor_user`: Auditor user
- `test_token`: JWT token for test_user
- `admin_token`: JWT token for admin_user
- `client`: Unauthenticated test client
- `auth_client`: Authenticated test client (test_user)
- `admin_client`: Authenticated admin test client

## Frontend Testing

### Test Structure

```
frontend/src/
├── components/
│   ├── StatCard.js
│   └── __tests__/
│       └── StatCard.test.js
├── pages/
│   ├── Dashboard.js
│   └── __tests__/
│       └── Dashboard.test.js
└── setupTests.js
```

### Writing Frontend Tests

#### Example: Component Test
```javascript
import React from 'react';
import { render, screen } from '@testing-library/react';
import StatCard from '../StatCard';

describe('StatCard Component', () => {
  test('renders title and value', () => {
    render(<StatCard title="Total Assets" value="500" />);

    expect(screen.getByText('Total Assets')).toBeInTheDocument();
    expect(screen.getByText('500')).toBeInTheDocument();
  });

  test('renders with color prop', () => {
    const { container } = render(
      <StatCard title="Test" value="123" color="primary" />
    );

    expect(container.firstChild).toBeInTheDocument();
  });
});
```

#### Example: Page Test with API Mocking
```javascript
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import Dashboard from '../Dashboard';

jest.mock('axios');

const mockData = {
  total_assets: 500,
  compliant_assets: 275,
  // ...
};

describe('Dashboard Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders dashboard with data', async () => {
    axios.get.mockResolvedValue({ data: mockData });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('500')).toBeInTheDocument();
    });
  });
});
```

### Running Frontend Tests

```bash
# Interactive mode (watches for changes)
npm test

# Run all tests once
npm test -- --watchAll=false

# With coverage
npm run test:coverage

# CI mode (non-interactive, with coverage)
npm run test:ci

# Update snapshots
npm test -- -u

# Run specific test file
npm test -- Dashboard.test.js

# Run tests matching pattern
npm test -- --testNamePattern="renders"
```

### Test Coverage

Frontend coverage is configured in `package.json`:

```json
{
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.{js,jsx}",
      "!src/index.js",
      "!src/reportWebVitals.js",
      "!src/**/*.test.{js,jsx}",
      "!src/**/__tests__/**"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 70,
        "functions": 70,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Integration Testing

### API Integration Tests

Test complete workflows:

```python
@pytest.mark.asyncio
async def test_assessment_workflow(auth_client, db):
    """Test complete assessment workflow."""
    # 1. Create asset
    asset_response = auth_client.post("/api/v1/assets", json={...})
    asset_id = asset_response.json()["id"]

    # 2. Upload evidence
    evidence_response = auth_client.post("/api/v1/evidence", json={...})
    assert evidence_response.status_code == 201

    # 3. Run assessment
    assessment_response = auth_client.post(
        "/api/v1/assessments/run",
        json={"asset_id": asset_id}
    )
    assert assessment_response.status_code == 202

    # 4. Wait for completion (in real test, use polling or fixtures)
    # ...

    # 5. Check results
    results = auth_client.get(f"/api/v1/assessments/{assessment_id}")
    assert results.status_code == 200
```

## Test Coverage Goals

### Backend Coverage

| Module | Target | Current |
|--------|--------|---------|
| Core (auth, security) | 90% | TBD |
| Scoring engine | 90% | TBD |
| API endpoints | 85% | TBD |
| Database models | 80% | TBD |
| Celery tasks | 75% | TBD |
| **Overall** | **80%** | **TBD** |

### Frontend Coverage

| Category | Target | Current |
|----------|--------|---------|
| Components | 80% | TBD |
| Pages | 75% | TBD |
| Services/API clients | 85% | TBD |
| Utilities | 90% | TBD |
| **Overall** | **80%** | **TBD** |

## Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- Pull requests
- Pushes to main/develop
- Nightly builds

Example workflow (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements-dev.txt
      - run: cd backend && pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:ci
      - uses: codecov/codecov-action@v3
```

## Best Practices

### General

1. **Test Behavior, Not Implementation:** Test what the code does, not how it does it
2. **Arrange-Act-Assert:** Structure tests clearly
3. **Descriptive Test Names:** Use descriptive names that explain what's being tested
4. **Independent Tests:** Each test should be independent
5. **Fast Tests:** Keep tests fast (<1s per test ideally)
6. **Mock External Dependencies:** Don't depend on external APIs or services

### Backend

1. **Use Fixtures:** Leverage pytest fixtures for setup/teardown
2. **Test Database Isolation:** Each test gets a fresh database
3. **Async Tests:** Use `@pytest.mark.asyncio` for async code
4. **Test RBAC:** Verify role-based access control
5. **Test Validation:** Test both valid and invalid input
6. **Test Edge Cases:** Cover boundary conditions

### Frontend

1. **Test User Interactions:** Simulate user behavior
2. **Mock API Calls:** Always mock axios/fetch
3. **Test Accessibility:** Use queries like `getByRole`, `getByLabelText`
4. **Avoid Implementation Details:** Don't test internal state
5. **Test Error States:** Verify error handling and display
6. **Use Testing Library Queries:** Prefer `getByRole` over `getByTestId`

## Debugging Tests

### Backend

```bash
# Drop into debugger on failure
pytest --pdb

# Show logs
pytest --log-cli-level=DEBUG

# Show print statements
pytest -s

# Run single test with verbose output
pytest -svv tests/test_auth.py::TestAuth::test_login_success
```

### Frontend

```bash
# Debug in browser (adds `debug()` calls)
npm test -- --debug

# Show console logs
npm test -- --verbose
```

## Common Issues

### Backend

**Issue:** Tests hang on database operations
```bash
# Check for missing await in async tests
# Verify test database exists and is accessible
```

**Issue:** Fixtures not found
```bash
# Ensure conftest.py is in tests directory
# Check fixture scope (session/module/function)
```

### Frontend

**Issue:** "Not wrapped in act(...)" warning
```javascript
// Use waitFor for async updates
await waitFor(() => {
  expect(screen.getByText('...')).toBeInTheDocument();
});
```

**Issue:** Mock not working
```javascript
// Clear mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Resources

### Documentation
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)

### Best Practices
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [Pytest Good Practices](https://docs.pytest.org/en/latest/explanation/goodpractices.html)
- [React Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

## Contributing

When adding new features:

1. **Write tests first** (TDD) or alongside code
2. **Ensure all tests pass** before creating PR
3. **Maintain coverage** above thresholds
4. **Update test documentation** if adding new patterns
5. **Review test failures** in CI before merging

## Getting Help

- **Backend Tests:** See `backend/tests/README.md`
- **Questions:** Ask in #engineering Slack channel
- **CI Issues:** Contact DevOps team
- **Coverage Reports:** View in GitHub PR checks
