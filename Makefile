# PyEnterprise Test Suite Makefile

.PHONY: help test test-unit test-integration test-e2e test-all test-security test-quality coverage clean install lint format

# Default target
help:
	@echo "PyEnterprise Test Suite"
	@echo "========================"
	@echo ""
	@echo "Available targets:"
	@echo "  help           Show this help message"
	@echo "  install        Install test dependencies"
	@echo "  test           Run unit tests (default)"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration Run integration tests (requires database)"
	@echo "  test-e2e       Run end-to-end tests (requires app running)"
	@echo "  test-all       Run all tests"
	@echo "  test-security  Run security tests"
	@echo "  test-quality   Run code quality checks"
	@echo "  coverage       Generate coverage report"
	@echo "  clean          Clean test artifacts"
	@echo "  lint           Lint code with flake8"
	@echo "  format         Format code with black and isort"
	@echo ""
	@echo "Examples:"
	@echo "  make test                 # Run unit tests"
	@echo "  make test-all             # Run all tests"
	@echo "  make coverage             # Run tests with coverage"
	@echo "  ENVIRONMENT=testing make test-integration  # Run integration tests"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install pytest-cov pytest-playwright bandit safety black isort flake8
	playwright install

# Run unit tests
test: test-unit

test-unit:
	python -m pytest tests/unit/ -v --cov=pyenterprise --cov-report=term-missing --cov-report=html

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	@echo "Note: Make sure database is configured"
	RUN_INTEGRATION_TESTS=true python -m pytest tests/test_*.py -v -m integration

# Run E2E tests
test-e2e:
	@echo "Running end-to-end tests..."
	@echo "Note: Make sure application is running on http://localhost:3000"
	@curl -s http://localhost:3000 > /dev/null || (echo "Application not running. Start with: reflex run" && exit 1)
	RUN_E2E_TESTS=true python -m pytest tests/e2e/ -v -m e2e

# Run all tests
test-all: test-unit test-integration test-e2e
	@echo "All tests completed!"

# Run security tests
test-security:
	@echo "Running security tests..."
	bandit -r pyenterprise/ -f json -o bandit-report.json
	safety check --json --output safety-report.json
	@echo "Security reports generated: bandit-report.json, safety-report.json"

# Run code quality checks
test-quality:
	@echo "Running code quality checks..."
	black --check pyenterprise/ tests/
	isort --check-only pyenterprise/ tests/
	flake8 pyenterprise/ tests/ --max-line-length=100 --ignore=E203,W503
	mypy pyenterprise/ --ignore-missing-imports || true

# Generate coverage report
coverage:
	python -m pytest tests/ -v --cov=pyenterprise --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

# Clean test artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf bandit-report.json safety-report.json
	rm -rf test-results/ test-reports/
	rm -rf playwright-report/ test-results/

# Lint code
lint:
	flake8 pyenterprise/ tests/ --max-line-length=100 --ignore=E203,W503
	bandit -r pyenterprise/

# Format code
format:
	black pyenterprise/ tests/
	isort pyenterprise/ tests/

# Watch mode (requires pytest-watch)
watch:
	pip install pytest-watch
	ptw tests/unit/ -v --runner "python -m pytest"

# Quick test during development
quick:
	python -m pytest tests/unit/ -v -x --tb=short

# Full test suite for CI
ci: install test-unit test-integration test-security test-quality
	@echo "CI test suite completed!"

# Development setup
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything is working."

# Start app for E2E testing
start-app:
	reflex run &
	sleep 10

# Stop app
stop-app:
	pkill -f "reflex run" || true

# Run tests with app management
test-with-app: start-app test-e2e stop-app
	@echo "E2E tests completed!"