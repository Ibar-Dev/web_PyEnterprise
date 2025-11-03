# Testing Guide for PyEnterprise

This document provides comprehensive information about the testing infrastructure and how to run tests for the PyEnterprise project.

## 🧪 Test Suite Overview

The PyEnterprise project includes a comprehensive testing suite with:

- **Unit Tests**: Fast, isolated tests for individual functions and classes
- **Integration Tests**: Tests that require database connections or external services
- **End-to-End (E2E) Tests**: Full workflow tests using Playwright
- **Security Tests**: Vulnerability scanning with Bandit and Safety
- **Code Quality**: Linting and formatting checks

## 📁 Test Structure

```
tests/
├── unit/                          # Unit tests
│   ├── test_auth.py               # Authentication unit tests
│   ├── test_database_operations.py # Database operation tests
│   ├── test_security.py           # Security function tests
│   ├── test_models.py             # Data model tests
│   ├── test_rate_limiter.py       # Rate limiting tests
│   └── test_admin_panel.py        # Admin panel component tests
├── e2e/                           # End-to-end tests
│   ├── conftest.py                # E2E test configuration
│   ├── test_authentication.py     # Authentication flows
│   └── test_critical_flows.py     # Critical business workflows
├── test_backend_completo.py       # Backend integration tests
├── test_login.py                  # Simple login tests
├── test_supabase.py               # Database connectivity tests
└── test_sistema_completo.py       # Full system tests
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **PostgreSQL/Supabase** for integration tests (optional)
3. **Reflex application** running for E2E tests

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install test-specific dependencies
pip install pytest-cov pytest-playwright bandit safety

# Install Playwright browsers for E2E tests
playwright install
```

### Running Tests

#### Unit Tests (Default)
```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Using the test script
python scripts/run_tests.py --unit-only

# Using Make
make test
```

#### All Tests
```bash
# Using the test script
python scripts/run_tests.py --all

# Using Make
make test-all

# Individual test types
python scripts/run_tests.py --integration
python scripts/run_tests.py --e2e
```

#### With Coverage
```bash
# Generate coverage report
python -m pytest --cov=pyenterprise --cov-report=html tests/

# Using Make
make coverage
```

## 🏗️ Test Configuration

### Environment Variables

- `ENVIRONMENT`: Set to "testing" for test runs
- `RUN_INTEGRATION_TESTS`: Set to "true" to run integration tests
- `RUN_E2E_TESTS`: Set to "true" to run E2E tests
- `TEST_BASE_URL`: Base URL for E2E tests (default: http://localhost:3000)
- `SUPABASE_URL`: Supabase URL for integration tests
- `SUPABASE_KEY`: Supabase key for integration tests

### Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.e2e`: End-to-end tests
- `@pytest.mark.security`: Security-related tests
- `@pytest.mark.auth`: Authentication tests
- `@pytest.mark.slow`: Slow-running tests

### Configuration Files

- `pytest.ini`: Main pytest configuration
- `conftest.py`: Global test fixtures and configuration
- `tests/e2e/conftest.py`: E2E-specific configuration

## 📊 Test Categories

### Unit Tests

**Location**: `tests/unit/`

**Purpose**: Test individual functions and classes in isolation

**Examples**:
- Authentication logic validation
- Database operation testing with mocked dependencies
- Security function validation
- Model validation testing
- Rate limiting functionality

**Running**:
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific unit test file
pytest tests/unit/test_auth.py -v

# Run with coverage
pytest tests/unit/ --cov=pyenterprise --cov-report=html
```

### Integration Tests

**Location**: `tests/test_*.py`

**Purpose**: Test integration between components with real database connections

**Examples**:
- Complete authentication flow with Supabase
- Database CRUD operations
- Full backend workflow testing

**Running**:
```bash
# Set environment variable
export RUN_INTEGRATION_TESTS=true

# Run integration tests
pytest tests/test_backend_completo.py -v -m integration

# Using test script
python scripts/run_tests.py --integration
```

### End-to-End Tests

**Location**: `tests/e2e/`

**Purpose**: Test complete user workflows in a browser

**Prerequisites**:
1. Application must be running: `reflex run`
2. Playwright browsers installed: `playwright install`

**Examples**:
- User login and logout flows
- Contact form submission
- Employee time tracking
- Project and task management
- Navigation and responsive design

**Running**:
```bash
# Start the application
reflex run &

# Run E2E tests
pytest tests/e2e/ -v -m e2e

# Using test script
python scripts/run_tests.py --e2e
```

## 🔒 Security Testing

### Static Analysis

```bash
# Run security vulnerability scanning
make test-security

# Or manually:
bandit -r pyenterprise/
safety check
```

### Security Tests Coverage

- Input sanitization
- SQL injection prevention
- XSS prevention
- CSRF token validation
- Authentication security
- Password hashing

## 📈 Code Quality

### Linting and Formatting

```bash
# Check code quality
make test-quality

# Lint code
make lint

# Format code
make format
```

### Tools Used

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **Bandit**: Security scanning
- **Safety**: Dependency vulnerability scanning

## 🔄 Continuous Integration

The project includes GitHub Actions workflows for automated testing:

### Workflow Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Jobs

1. **unit-tests**: Run unit tests across multiple Python versions
2. **integration-tests**: Run integration tests with database
3. **e2e-tests**: Run E2E tests with running application
4. **security-tests**: Run security vulnerability scans
5. **code-quality**: Run linting and formatting checks
6. **test-summary**: Generate summary of all test results

### Coverage Reporting

Coverage reports are automatically uploaded to Codecov for visualization and tracking.

## 🛠️ Writing New Tests

### Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.unit
class TestNewFeature:
    def test_functionality_success(self):
        """Test successful case"""
        # Arrange
        # Act
        # Assert
        pass

    def test_error_handling(self):
        """Test error cases"""
        # Test error conditions
        pass

    @patch('module.dependency')
    def test_with_mock(self, mock_dependency):
        """Test with mocked dependencies"""
        # Configure mock
        # Test function
        pass
```

### E2E Test Template

```python
import pytest
from playwright.async_api import Page, expect

@pytest.mark.e2e
class TestNewWorkflow:
    async def test_workflow_complete(self, page: Page):
        """Test complete user workflow"""
        # Navigate to page
        # Perform actions
        # Verify results
        pass
```

### Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Mock external dependencies** in unit tests
4. **Test both success and failure cases**
5. **Use fixtures** for common test data and setup
6. **Add appropriate markers** to categorize tests
7. **Keep tests independent** and isolated

## 📋 Test Data Management

### Fixtures

Common test data is provided through fixtures in `conftest.py`:

- `mock_employee_data`: Sample employee information
- `mock_project_data`: Sample project information
- `mock_task_data`: Sample task information
- `test_user_data`: Login credentials for tests

### Mock Services

Tests use mocked services to avoid dependencies:

- **Supabase client**: Mocked database operations
- **Reflex components**: Mocked UI components
- **Authentication**: Mocked auth state

## 🔍 Debugging Tests

### Running Individual Tests

```bash
# Run specific test
pytest tests/unit/test_auth.py::TestAuth::test_login_success -v

# Run with debugging
pytest tests/unit/test_auth.py -v -s --pdb

# Stop on first failure
pytest tests/ -x
```

### Test Output

- `-v`: Verbose output
- `-s`: Show print statements
- `--tb=short`: Short traceback format
- `--tb=long`: Long traceback format

### Common Issues

1. **Import errors**: Ensure you're in the project root
2. **Database connection**: Set `RUN_INTEGRATION_TESTS=false` to skip integration tests
3. **E2E failures**: Ensure the application is running on port 3000
4. **Playwright issues**: Run `playwright install` to install browsers

## 📞 Getting Help

For questions about testing:

1. Check this document first
2. Look at existing test files for examples
3. Run `pytest --help` for pytest options
4. Check the [pytest documentation](https://docs.pytest.org/)
5. Check the [Playwright documentation](https://playwright.dev/)

## 🚀 Contributing

When contributing new features:

1. **Write tests first** (TDD approach when possible)
2. **Ensure all tests pass** before submitting PR
3. **Add appropriate test markers**
4. **Update documentation** if needed
5. **Maintain test coverage** above 80%

Remember: Tests are code too! Keep them clean, readable, and maintainable.