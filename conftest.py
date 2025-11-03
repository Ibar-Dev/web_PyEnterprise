"""
pytest configuration and fixtures for the PyEnterprise test suite
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Mock environment variables for testing
@pytest.fixture(scope="session", autouse=True)
def mock_env_vars():
    """Set up test environment variables"""
    os.environ["SUPABASE_URL"] = "https://test.supabase.co"
    os.environ["SUPABASE_KEY"] = "test-key"
    os.environ["ENVIRONMENT"] = "testing"

    yield

    # Clean up
    for key in ["SUPABASE_URL", "SUPABASE_KEY", "ENVIRONMENT"]:
        if key in os.environ:
            del os.environ[key]

@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing"""
    mock_client = Mock()

    # Mock table method chain
    mock_table = Mock()
    mock_client.table.return_value = mock_table

    # Mock common operations
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.order.return_value = mock_table
    mock_table.execute.return_value = Mock(data=[], count=0)

    return mock_client

@pytest.fixture
def mock_employee_data():
    """Sample employee data for testing"""
    return {
        "id": "test-uuid-123",
        "nombre": "Test",
        "apellidos": "Employee",
        "email": "test@pylink.com",
        "password": "hashed_password",
        "rol": "desarrollador",
        "activo": True,
        "fecha_contratacion": "2024-01-01",
        "telefono": "123456789",
        "departamento": "IT"
    }

@pytest.fixture
def mock_project_data():
    """Sample project data for testing"""
    return {
        "id": "test-project-uuid",
        "nombre": "Test Project",
        "descripcion": "Test project description",
        "cliente": "Test Client",
        "presupuesto": 10000.0,
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-12-31",
        "estado": "activo"
    }

@pytest.fixture
def mock_task_data():
    """Sample task data for testing"""
    return {
        "id": "test-task-uuid",
        "titulo": "Test Task",
        "descripcion": "Test task description",
        "proyecto_id": "test-project-uuid",
        "empleado_id": "test-uuid-123",
        "prioridad": "alta",
        "estado": "pendiente",
        "fecha_limite": "2024-06-30"
    }

@pytest.fixture
def mock_auth_state():
    """Mock authentication state"""
    state = Mock()
    state.is_authenticated = True
    state.user_data = {
        "id": "test-uuid-123",
        "nombre": "Test",
        "apellidos": "Employee",
        "email": "test@pylink.com",
        "rol": "desarrollador"
    }
    return state

@pytest.fixture
def temp_database():
    """Create a temporary database for testing"""
    # This would set up a test database if needed
    # For now, we'll use mocked responses
    yield

@pytest.fixture
def mock_reflex_state():
    """Mock Reflex state for testing components"""
    from reflex.state import BaseState

    class MockState(BaseState):
        pass

    return MockState()

# Skip integration tests if database is not available
def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip integration tests if needed"""
    skip_integration = pytest.mark.skip(reason="Database not available for integration tests")

    # Check if we should run integration tests
    run_integration = os.getenv("RUN_INTEGRATION_TESTS", "false").lower() == "true"

    if not run_integration:
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)