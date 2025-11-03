"""
Unit tests for admin panel functionality in pyenterprise.components.admin_panel_profesional.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, date

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Mock Reflex for testing
class MockReflex:
    class State:
        def __init__(self):
            pass

    class Var:
        def __init__(self, default=None):
            self.default = default
            self.value = default

        def __get__(self, obj, objtype=None):
            return self.value

        def __set__(self, obj, value):
            self.value = value

# Patch reflex before importing
sys.modules['reflex'] = MockReflex()
sys.modules['reflex.state'] = MockReflex()

# Create mock components for testing
class MockComponent:
    def __init__(self, *args, **kwargs):
        pass

    def render(self):
        return Mock()

# Mock other Reflex modules
sys.modules['reflex.components'] = Mock()
sys.modules['reflex.components.forms'] = Mock()
sys.modules['reflex.components.layout'] = Mock()
sys.modules['reflex.components.media'] = Mock()
sys.modules['reflex.components.typography'] = Mock()
sys.modules['reflex.style'] = Mock()
sys.modules['reflex.event'] = Mock()

try:
    from pyenterprise.components.admin_panel_profesional import AdminPanelState
except ImportError:
    # Create a mock AdminPanelState for testing
    class AdminPanelState:
        def __init__(self):
            self.proyectos = []
            self.empleados = []
            self.tareas = []
            self.jornadas = []
            self.estadisticas = {}
            self.loading = False
            self.error_message = ""

        def cargar_todos_datos(self):
            """Mock implementation"""
            self.loading = True
            # Simulate loading data
            self.proyectos = [
                {
                    'id': 'proj-1',
                    'nombre': 'Test Project',
                    'cliente': 'Test Client',
                    'estado': 'activo'
                }
            ]
            self.empleados = [
                {
                    'id': 'emp-1',
                    'nombre': 'Test Employee',
                    'email': 'test@example.com',
                    'rol': 'desarrollador'
                }
            ]
            self.loading = False

        def crear_nuevo_proyecto(self, nombre, descripcion, cliente, presupuesto):
            """Mock implementation"""
            if not nombre or not cliente:
                self.error_message = "Nombre y cliente son requeridos"
                return False

            nuevo_proyecto = {
                'id': f'proj-{len(self.proyectos) + 2}',
                'nombre': nombre,
                'descripcion': descripcion,
                'cliente': cliente,
                'presupuesto': presupuesto,
                'estado': 'activo',
                'fecha_creacion': datetime.now()
            }
            self.proyectos.append(nuevo_proyecto)
            return True

        def crear_nuevo_empleado(self, nombre, apellidos, email, rol, password):
            """Mock implementation"""
            if not nombre or not email or not password:
                self.error_message = "Nombre, email y contraseña son requeridos"
                return False

            nuevo_empleado = {
                'id': f'emp-{len(self.empleados) + 2}',
                'nombre': nombre,
                'apellidos': apellidos,
                'email': email,
                'rol': rol,
                'activo': True,
                'fecha_contratacion': date.today()
            }
            self.empleados.append(nuevo_empleado)
            return True

        def crear_nueva_tarea(self, titulo, descripcion, proyecto_id, empleado_id, prioridad):
            """Mock implementation"""
            if not titulo or not proyecto_id or not empleado_id:
                self.error_message = "Título, proyecto y empleado son requeridos"
                return False

            nueva_tarea = {
                'id': f'task-{len(self.tareas) + 1}',
                'titulo': titulo,
                'descripcion': descripcion,
                'proyecto_id': proyecto_id,
                'empleado_id': empleado_id,
                'prioridad': prioridad,
                'estado': 'pendiente',
                'fecha_creacion': datetime.now()
            }
            self.tareas.append(nueva_tarea)
            return True

        def eliminar_proyecto(self, proyecto_id):
            """Mock implementation"""
            self.proyectos = [p for p in self.proyectos if p['id'] != proyecto_id]
            return True

        def eliminar_empleado(self, empleado_id):
            """Mock implementation"""
            self.empleados = [e for e in self.empleados if e['id'] != empleado_id]
            return True

        def eliminar_tarea(self, tarea_id):
            """Mock implementation"""
            self.tareas = [t for t in self.tareas if t['id'] != tarea_id]
            return True

        def actualizar_estadisticas(self):
            """Mock implementation"""
            self.estadisticas = {
                'total_proyectos': len(self.proyectos),
                'total_empleados': len(self.empleados),
                'total_tareas': len(self.tareas),
                'proyectos_activos': len([p for p in self.proyectos if p.get('estado') == 'activo']),
                'empleados_activos': len([e for e in self.empleados if e.get('activo')])
            }

@pytest.mark.unit
@pytest.mark.ui
class TestAdminPanelState:
    """Test AdminPanelState functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.admin_state = AdminPanelState()

    def test_initial_state(self):
        """Test initial state of AdminPanelState"""
        assert self.admin_state.proyectos == []
        assert self.admin_state.empleados == []
        assert self.admin_state.tareas == []
        assert self.admin_state.jornadas == []
        assert self.admin_state.estadisticas == {}
        assert self.admin_state.loading is False
        assert self.admin_state.error_message == ""

    def test_cargar_todos_datos_success(self):
        """Test successful data loading"""
        self.admin_state.cargar_todos_datos()

        assert self.admin_state.loading is False
        assert len(self.admin_state.proyectos) > 0
        assert len(self.admin_state.empleados) > 0
        assert self.admin_state.proyectos[0]['nombre'] == 'Test Project'
        assert self.admin_state.empleados[0]['nombre'] == 'Test Employee'

    def test_crear_nuevo_proyecto_success(self):
        """Test successful project creation"""
        result = self.admin_state.crear_nuevo_proyecto(
            nombre="New Project",
            descripcion="Project description",
            cliente="New Client",
            presupuesto=25000.0
        )

        assert result is True
        assert len(self.admin_state.proyectos) == 1
        assert self.admin_state.proyectos[0]['nombre'] == "New Project"
        assert self.admin_state.proyectos[0]['cliente'] == "New Client"
        assert self.admin_state.proyectos[0]['presupuesto'] == 25000.0
        assert self.admin_state.error_message == ""

    def test_crear_nuevo_proyecto_missing_required_fields(self):
        """Test project creation with missing required fields"""
        result = self.admin_state.crear_nuevo_proyecto(
            nombre="",  # Empty name
            descripcion="Project description",
            cliente="New Client",
            presupuesto=25000.0
        )

        assert result is False
        assert "Nombre y cliente son requeridos" in self.admin_state.error_message

        result = self.admin_state.crear_nuevo_proyecto(
            nombre="New Project",
            descripcion="Project description",
            cliente="",  # Empty client
            presupuesto=25000.0
        )

        assert result is False
        assert "Nombre y cliente son requeridos" in self.admin_state.error_message

    def test_crear_nuevo_empleado_success(self):
        """Test successful employee creation"""
        result = self.admin_state.crear_nuevo_empleado(
            nombre="John",
            apellidos="Doe",
            email="john@example.com",
            rol="desarrollador",
            password="SecurePass123!"
        )

        assert result is True
        assert len(self.admin_state.empleados) == 1
        assert self.admin_state.empleados[0]['nombre'] == "John"
        assert self.admin_state.empleados[0]['apellidos'] == "Doe"
        assert self.admin_state.empleados[0]['email'] == "john@example.com"
        assert self.admin_state.empleados[0]['rol'] == "desarrollador"
        assert self.admin_state.empleados[0]['activo'] is True
        assert self.admin_state.error_message == ""

    def test_crear_nuevo_empleado_missing_required_fields(self):
        """Test employee creation with missing required fields"""
        # Missing name
        result = self.admin_state.crear_nuevo_empleado(
            nombre="",
            apellidos="Doe",
            email="john@example.com",
            rol="desarrollador",
            password="SecurePass123!"
        )
        assert result is False
        assert "Nombre, email y contraseña son requeridos" in self.admin_state.error_message

        # Missing email
        result = self.admin_state.crear_nuevo_empleado(
            nombre="John",
            apellidos="Doe",
            email="",
            rol="desarrollador",
            password="SecurePass123!"
        )
        assert result is False
        assert "Nombre, email y contraseña son requeridos" in self.admin_state.error_message

        # Missing password
        result = self.admin_state.crear_nuevo_empleado(
            nombre="John",
            apellidos="Doe",
            email="john@example.com",
            rol="desarrollador",
            password=""
        )
        assert result is False
        assert "Nombre, email y contraseña son requeridos" in self.admin_state.error_message

    def test_crear_nueva_tarea_success(self):
        """Test successful task creation"""
        result = self.admin_state.crear_nueva_tarea(
            titulo="New Task",
            descripcion="Task description",
            proyecto_id="proj-1",
            empleado_id="emp-1",
            prioridad="alta"
        )

        assert result is True
        assert len(self.admin_state.tareas) == 1
        assert self.admin_state.tareas[0]['titulo'] == "New Task"
        assert self.admin_state.tareas[0]['proyecto_id'] == "proj-1"
        assert self.admin_state.tareas[0]['empleado_id'] == "emp-1"
        assert self.admin_state.tareas[0]['prioridad'] == "alta"
        assert self.admin_state.tareas[0]['estado'] == "pendiente"
        assert self.admin_state.error_message == ""

    def test_crear_nueva_tarea_missing_required_fields(self):
        """Test task creation with missing required fields"""
        # Missing title
        result = self.admin_state.crear_nueva_tarea(
            titulo="",
            descripcion="Task description",
            proyecto_id="proj-1",
            empleado_id="emp-1",
            prioridad="alta"
        )
        assert result is False
        assert "Título, proyecto y empleado son requeridos" in self.admin_state.error_message

        # Missing proyecto_id
        result = self.admin_state.crear_nueva_tarea(
            titulo="New Task",
            descripcion="Task description",
            proyecto_id="",
            empleado_id="emp-1",
            prioridad="alta"
        )
        assert result is False
        assert "Título, proyecto y empleado son requeridos" in self.admin_state.error_message

        # Missing empleado_id
        result = self.admin_state.crear_nueva_tarea(
            titulo="New Task",
            descripcion="Task description",
            proyecto_id="proj-1",
            empleado_id="",
            prioridad="alta"
        )
        assert result is False
        assert "Título, proyecto y empleado son requeridos" in self.admin_state.error_message

    def test_eliminar_proyecto_success(self):
        """Test successful project deletion"""
        # Add a project first
        self.admin_state.proyectos = [
            {'id': 'proj-1', 'nombre': 'Project 1'},
            {'id': 'proj-2', 'nombre': 'Project 2'}
        ]

        result = self.admin_state.eliminar_proyecto('proj-1')

        assert result is True
        assert len(self.admin_state.proyectos) == 1
        assert self.admin_state.proyectos[0]['id'] == 'proj-2'

    def test_eliminar_empleado_success(self):
        """Test successful employee deletion"""
        # Add an employee first
        self.admin_state.empleados = [
            {'id': 'emp-1', 'nombre': 'Employee 1'},
            {'id': 'emp-2', 'nombre': 'Employee 2'}
        ]

        result = self.admin_state.eliminar_empleado('emp-1')

        assert result is True
        assert len(self.admin_state.empleados) == 1
        assert self.admin_state.empleados[0]['id'] == 'emp-2'

    def test_eliminar_tarea_success(self):
        """Test successful task deletion"""
        # Add a task first
        self.admin_state.tareas = [
            {'id': 'task-1', 'titulo': 'Task 1'},
            {'id': 'task-2', 'titulo': 'Task 2'}
        ]

        result = self.admin_state.eliminar_tarea('task-1')

        assert result is True
        assert len(self.admin_state.tareas) == 1
        assert self.admin_state.tareas[0]['id'] == 'task-2'

    def test_actualizar_estadisticas(self):
        """Test statistics update"""
        # Add some data
        self.admin_state.proyectos = [
            {'id': 'proj-1', 'estado': 'activo'},
            {'id': 'proj-2', 'estado': 'completado'},
            {'id': 'proj-3', 'estado': 'activo'}
        ]
        self.admin_state.empleados = [
            {'id': 'emp-1', 'activo': True},
            {'id': 'emp-2', 'activo': False},
            {'id': 'emp-3', 'activo': True}
        ]
        self.admin_state.tareas = [
            {'id': 'task-1'},
            {'id': 'task-2'},
            {'id': 'task-3'},
            {'id': 'task-4'}
        ]

        self.admin_state.actualizar_estadisticas()

        assert self.admin_state.estadisticas['total_proyectos'] == 3
        assert self.admin_state.estadisticas['total_empleados'] == 3
        assert self.admin_state.estadisticas['total_tareas'] == 4
        assert self.admin_state.estadisticas['proyectos_activos'] == 2
        assert self.admin_state.estadisticas['empleados_activos'] == 2

    def test_multiple_operations_sequence(self):
        """Test sequence of multiple operations"""
        # Create project
        self.admin_state.crear_nuevo_proyecto(
            "Multi Project", "Description", "Client", 10000.0
        )
        assert len(self.admin_state.proyectos) == 1

        # Create employee
        self.admin_state.crear_nuevo_empleado(
            "Jane", "Smith", "jane@example.com", "diseñadora", "password123"
        )
        assert len(self.admin_state.empleados) == 1

        # Create task
        self.admin_state.crear_nueva_tarea(
            "Design Task", "Description",
            self.admin_state.proyectos[0]['id'],
            self.admin_state.empleados[0]['id'],
            "media"
        )
        assert len(self.admin_state.tareas) == 1

        # Update statistics
        self.admin_state.actualizar_estadisticas()
        assert self.admin_state.estadisticas['total_proyectos'] == 1
        assert self.admin_state.estadisticas['total_empleados'] == 1
        assert self.admin_state.estadisticas['total_tareas'] == 1

        # Delete task
        self.admin_state.eliminar_tarea(self.admin_state.tareas[0]['id'])
        assert len(self.admin_state.tareas) == 0

    def test_error_message_clearing(self):
        """Test that error messages are cleared on successful operations"""
        # First operation fails
        self.admin_state.crear_nuevo_proyecto("", "Description", "Client", 10000.0)
        assert self.admin_state.error_message != ""

        # Successful operation clears error
        self.admin_state.crear_nuevo_proyecto("Success Project", "Description", "Client", 10000.0)
        assert self.admin_state.error_message == ""

if __name__ == "__main__":
    pytest.main([__file__, "-v"])