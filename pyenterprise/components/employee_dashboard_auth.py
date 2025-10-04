"""
Dashboard avanzado para empleados PyLink con integración completa a Supabase
"""

import reflex as rx
from datetime import datetime, timedelta
from ..styles import *
from ..database import (
    obtener_proyectos_empleado,
    obtener_tareas_empleado,
    registrar_jornada,
    obtener_jornadas_empleado,
    calcular_horas_totales_empleado
)


class EmployeeDashboardState(rx.State):
    """Estado del dashboard de empleados con integración a Supabase."""

    # Estado de sesión de trabajo
    is_working: bool = False
    current_session: dict = {}
    work_description: str = ""
    selected_project: str = ""

    # Datos cargados de la base de datos
    proyectos: list = []
    tareas: list = []
    jornadas: list = []
    horas_hoy: float = 0.0
    horas_semana: float = 0.0

    # Estado de carga
    is_loading: bool = False

    # Información del empleado autenticado
    empleado_id: str = ""
    empleado_nombre: str = ""

    async def on_mount(self):
        """Cargar datos iniciales al montar el componente."""
        await self.cargar_datos()

    def get_empleado_id_from_session(self) -> str:
        """Obtener empleado_id de la sesión de Reflex."""
        try:
            # Acceder al estado de autenticación global
            auth_state = rx.session.get_state(EmployeeAuthState)
            if auth_state and auth_state.employee_id:
                return auth_state.employee_id
        except Exception as e:
            print(f"Error obteniendo empleado_id: {e}")
        return ""

    async def cargar_datos(self):
        """Cargar todos los datos necesarios desde Supabase."""
        self.is_loading = True

        try:
            # Obtener empleado_id de la sesión
            empleado_id = self.get_empleado_id_from_session()

            if empleado_id:
                self.empleado_id = empleado_id

                # Cargar proyectos del empleado
                proyectos_data = obtener_proyectos_empleado(empleado_id)
                self.proyectos = proyectos_data if proyectos_data else []

                # Cargar tareas del empleado
                tareas_data = obtener_tareas_empleado(empleado_id)
                self.tareas = tareas_data if tareas_data else []

                # Cargar jornadas recientes
                jornadas_data = obtener_jornadas_empleado(empleado_id)
                self.jornadas = jornadas_data if jornadas_data else []

                # Calcular horas trabajadas
                fecha_hoy = datetime.now().date()
                fecha_lunes = fecha_hoy - timedelta(days=fecha_hoy.weekday())

                self.horas_hoy = calcular_horas_totales_empleado(
                    empleado_id,
                    fecha_hoy.strftime('%Y-%m-%d'),
                    fecha_hoy.strftime('%Y-%m-%d')
                )

                self.horas_semana = calcular_horas_totales_empleado(
                    empleado_id,
                    fecha_lunes.strftime('%Y-%m-%d'),
                    fecha_hoy.strftime('%Y-%m-%d')
                )
            else:
                print("❌ No se pudo obtener empleado_id - usuario no autenticado")

        except Exception as e:
            print(f"❌ Error cargando datos del dashboard: {e}")

        self.is_loading = False

    def start_work_session(self, proyecto_id: str):
        """Iniciar sesión de trabajo."""
        if not self.is_working:
            self.current_session = {
                "proyecto_id": proyecto_id,
                "start_time": datetime.now().isoformat(),
                "description": ""
            }
            self.is_working = True
            self.selected_project = proyecto_id

    def end_work_session(self):
        """Finalizar sesión de trabajo."""
        if self.is_working and self.current_session:
            start_time = datetime.fromisoformat(self.current_session["start_time"])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 3600  # horas

            # Registrar jornada en la base de datos
            empleado_id = self.get_empleado_id_from_session()

            if empleado_id:
                jornada_data = registrar_jornada(
                    empleado_id=empleado_id,
                    proyecto_id=self.current_session["proyecto_id"],
                    fecha=end_time.strftime('%Y-%m-%d'),
                    hora_inicio=start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    hora_fin=end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    descripcion=self.work_description
                )

                if jornada_data:
                    # Recargar datos después de registrar
                    self.cargar_datos()
                    self.horas_hoy += duration

            # Limpiar sesión
            self.is_working = False
            self.current_session = {}
            self.work_description = ""
            self.selected_project = ""

    def set_work_description(self, description: str):
        """Actualizar descripción de la sesión de trabajo."""
        self.work_description = description
