"""
Dashboard principal para empleados PyLink con integración a Supabase
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

    async def on_mount(self):
        """Cargar datos iniciales al montar el componente."""
        await self.cargar_datos()

    async def cargar_datos(self):
        """Cargar todos los datos necesarios desde Supabase."""
        self.is_loading = True

        # TODO: Obtener empleado_id del estado de autenticación
        empleado_id = "empleado_id_aqui"

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
            empleado_id = "empleado_id_aqui"  # TODO: Obtener del estado de autenticación

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


def time_control_card() -> rx.Component:
    """Tarjeta de control de tiempo."""
    return rx.card(
        rx.vstack(
            rx.heading("⏰ Control de Tiempo", size="5"),
            rx.text("Gestión de jornadas laborales"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.vstack(
                    rx.text(f"Horas trabajadas hoy: {EmployeeDashboardState.horas_hoy}h",
                           font_weight="600", font_size="1.1rem"),
                    rx.text(f"Horas esta semana: {EmployeeDashboardState.horas_semana}h",
                           font_size="0.9rem", color=COLORS["text_light"]),
                    spacing="2",
                )
            ),

            rx.cond(
                ~EmployeeDashboardState.is_working,
                rx.button(
                    "🟢 Iniciar Jornada",
                    on_click=lambda: EmployeeDashboardState.start_work_session("default"),
                    background=COLORS["success"],
                    color="white",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("🟢 Sesión Activa", color="green", font_weight="600"),
                    rx.input(
                        placeholder="¿Qué estás haciendo?",
                        value=EmployeeDashboardState.work_description,
                        on_change=EmployeeDashboardState.set_work_description,
                    ),
                    rx.button(
                        "🔴 Finalizar Jornada",
                        on_click=EmployeeDashboardState.end_work_session,
                        color_scheme="red",
                        width="100%",
                    ),
                    spacing="3",
                )
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        size="3",
        padding="1.5rem",
    )


def projects_card() -> rx.Component:
    """Tarjeta de proyectos asignados."""
    return rx.card(
        rx.vstack(
            rx.heading("📊 Mis Proyectos", size="5"),
            rx.text("Proyectos donde colaboras"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.text("Proyectos cargados desde Supabase aparecerían aquí")
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        size="3",
        padding="1.5rem",
    )


def tasks_card() -> rx.Component:
    """Tarjeta de tareas asignadas."""
    return rx.card(
        rx.vstack(
            rx.heading("✅ Mis Tareas", size="5"),
            rx.text("Tareas pendientes y en progreso"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.text("Tareas cargadas desde Supabase aparecerían aquí")
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        size="3",
        padding="1.5rem",
    )


def employee_dashboard() -> rx.Component:
    """Dashboard principal para empleados con integración completa."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Dashboard de Empleados", size="7"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=lambda: rx.redirect("/empleados"),
                    variant="outline",
                    color_scheme="red",
                ),
                justify="between",
                align="center",
                width="100%",
                padding="2rem 0",
            ),

            # Grid de tarjetas principales
            rx.grid(
                time_control_card(),
                projects_card(),
                tasks_card(),
                columns="3",
                spacing="6",
                width="100%",
            ),

            # Historial reciente de jornadas
            rx.card(
                rx.vstack(
                    rx.heading("📈 Historial de Jornadas", size="5"),
                    rx.text("Últimas jornadas registradas"),

                    rx.cond(
                        EmployeeDashboardState.is_loading,
                        rx.spinner(),
                        rx.text("Jornadas cargadas desde Supabase aparecerían aquí")
                    ),

                    spacing="4",
                    align="stretch",
                    width="100%",
                ),
                size="3",
                padding="1.5rem",
            ),

            spacing="8",
            width="100%",
            max_width="1200px",
        ),
        padding="2rem",
        on_mount=EmployeeDashboardState.on_mount,
    )
