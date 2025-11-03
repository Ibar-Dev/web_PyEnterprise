"""
Unit tests for database operations in pyenterprise.database.supabase_client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pyenterprise.database.supabase_client import (
    login_empleado,
    crear_empleado,
    hash_password,
    verify_password,
    registrar_jornada,
    obtener_proyecto_por_id,
    crear_proyecto,
    crear_tarea,
    asignar_empleado_proyecto,
    eliminar_proyecto
)

@pytest.mark.unit
@pytest.mark.database
class TestDatabaseOperations:
    """Test database operations with mocked Supabase client"""

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_login_empleado_success(self, mock_supabase):
        """Test successful employee login"""
        # Mock the database response
        mock_response = Mock()
        mock_response.data = [{
            'id': 'test-uuid',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'test@pylink.com',
            'password': 'hashed_password',
            'rol': 'desarrollador',
            'activo': True
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        # Mock password verification
        with patch('pyenterprise.database.supabase_client.verify_password', return_value=True):
            result = login_empleado("test@pylink.com", "password123")

        assert result is not None
        assert result['email'] == "test@pylink.com"
        assert result['rol'] == "desarrollador"
        assert result['activo'] is True

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_login_empleado_invalid_credentials(self, mock_supabase):
        """Test login with invalid credentials"""
        # Mock empty response
        mock_response = Mock()
        mock_response.data = []
        mock_response.count = 0
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        result = login_empleado("invalid@test.com", "wrongpassword")

        assert result is None

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_login_empleado_inactive_user(self, mock_supabase):
        """Test login with inactive user"""
        # Mock inactive user response
        mock_response = Mock()
        mock_response.data = [{
            'id': 'test-uuid',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'test@pylink.com',
            'password': 'hashed_password',
            'rol': 'desarrollador',
            'activo': False
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        result = login_empleado("test@pylink.com", "password123")

        assert result is None

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_login_empleado_wrong_password(self, mock_supabase):
        """Test login with wrong password"""
        # Mock the database response
        mock_response = Mock()
        mock_response.data = [{
            'id': 'test-uuid',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'test@pylink.com',
            'password': 'hashed_password',
            'rol': 'desarrollador',
            'activo': True
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        # Mock password verification failure
        with patch('pyenterprise.database.supabase_client.verify_password', return_value=False):
            result = login_empleado("test@pylink.com", "wrongpassword")

        assert result is None

    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password123"
        hashed = hash_password(password)

        assert hashed != password
        assert hashed.startswith('$2b$')  # bcrypt hash prefix
        assert len(hashed) == 60  # bcrypt hash length

    def test_verify_password_success(self):
        """Test successful password verification"""
        password = "test_password123"
        hashed = hash_password(password)

        result = verify_password(password, hashed)

        assert result is True

    def test_verify_password_failure(self):
        """Test failed password verification"""
        password = "test_password123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        result = verify_password(wrong_password, hashed)

        assert result is False

    @patch('pyenterprise.database.supabase_client.supabase')
    @patch('pyenterprise.database.supabase_client.hash_password')
    def test_crear_empleado_success(self, mock_hash_password, mock_supabase):
        """Test successful employee creation"""
        # Mock password hashing
        mock_hash_password.return_value = "hashed_password"

        # Mock database response
        mock_response = Mock()
        mock_response.data = [{
            'id': 'new-uuid',
            'nombre': 'New',
            'apellidos': 'Employee',
            'email': 'new@pylink.com',
            'rol': 'desarrollador',
            'activo': True
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = crear_empleado(
            nombre="New",
            apellidos="Employee",
            email="new@pylink.com",
            password="password123",
            rol="desarrollador"
        )

        assert result is not None
        assert result['email'] == "new@pylink.com"
        mock_hash_password.assert_called_once_with("password123")

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_registrar_jornada_success(self, mock_supabase):
        """Test successful work session registration"""
        # Mock database response
        mock_response = Mock()
        mock_response.data = [{
            'id': 'jornada-uuid',
            'empleado_id': 'test-uuid',
            'proyecto_id': 'project-uuid',
            'fecha': '2024-01-01',
            'hora_inicio': '09:00',
            'hora_fin': '17:00',
            'total_horas': 8.0
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = registrar_jornada(
            empleado_id='test-uuid',
            proyecto_id='project-uuid',
            fecha='2024-01-01',
            hora_inicio='09:00',
            hora_fin='17:00'
        )

        assert result is not None
        assert result['empleado_id'] == 'test-uuid'
        assert result['total_horas'] == 8.0

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_obtener_proyecto_por_id_success(self, mock_supabase):
        """Test successful project retrieval by ID"""
        mock_response = Mock()
        mock_response.data = [{
            'id': 'project-uuid',
            'nombre': 'Test Project',
            'descripcion': 'Test Description',
            'estado': 'activo'
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        result = obtener_proyecto_por_id('project-uuid')

        assert result is not None
        assert result['id'] == 'project-uuid'
        assert result['nombre'] == 'Test Project'

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_obtener_proyecto_por_id_not_found(self, mock_supabase):
        """Test project retrieval when not found"""
        mock_response = Mock()
        mock_response.data = []
        mock_response.count = 0
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        result = obtener_proyecto_por_id('nonexistent-uuid')

        assert result is None

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_crear_proyecto_success(self, mock_supabase):
        """Test successful project creation"""
        mock_response = Mock()
        mock_response.data = [{
            'id': 'new-project-uuid',
            'nombre': 'New Project',
            'cliente': 'Test Client',
            'presupuesto': 50000.0,
            'estado': 'activo'
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = crear_proyecto(
            nombre="New Project",
            descripcion="Project description",
            cliente="Test Client",
            presupuesto=50000.0
        )

        assert result is not None
        assert result['nombre'] == "New Project"
        assert result['presupuesto'] == 50000.0

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_crear_tarea_success(self, mock_supabase):
        """Test successful task creation"""
        mock_response = Mock()
        mock_response.data = [{
            'id': 'new-task-uuid',
            'titulo': 'New Task',
            'descripcion': 'Task description',
            'proyecto_id': 'project-uuid',
            'empleado_id': 'employee-uuid',
            'prioridad': 'alta',
            'estado': 'pendiente'
        }]
        mock_response.count = 1
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = crear_tarea(
            titulo="New Task",
            descripcion="Task description",
            proyecto_id='project-uuid',
            empleado_id='employee-uuid',
            prioridad='alta'
        )

        assert result is not None
        assert result['titulo'] == "New Task"
        assert result['prioridad'] == "alta"

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_asignar_empleado_proyecto_success(self, mock_supabase):
        """Test successful employee-project assignment"""
        mock_response = Mock()
        mock_response.data = [{'id': 'assignment-uuid'}]
        mock_response.count = 1
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = asignar_empleado_proyecto(
            empleado_id='employee-uuid',
            proyecto_id='project-uuid',
            rol='desarrollador'
        )

        assert result is True

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_eliminar_proyecto_success(self, mock_supabase):
        """Test successful project deletion"""
        mock_response = Mock()
        mock_response.data = []
        mock_response.count = 0
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response

        result = eliminar_proyecto('project-uuid')

        assert result is True

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_eliminar_proyecto_not_found(self, mock_supabase):
        """Test project deletion when not found"""
        mock_response = Mock()
        mock_response.data = []
        mock_response.count = 0
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response

        result = eliminar_proyecto('nonexistent-uuid')

        assert result is True  # Still returns True as deletion is idempotent

    @patch('pyenterprise.database.supabase_client.supabase')
    def test_database_error_handling(self, mock_supabase):
        """Test database error handling"""
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

        result = login_empleado("test@pylink.com", "password123")

        assert result is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])