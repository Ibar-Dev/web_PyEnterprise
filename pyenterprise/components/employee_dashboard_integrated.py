"""
Dashboard integrado con autenticación para empleados PyLink
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
from .employee_auth import EmployeeAuthState


class EmployeeDashboardState(rx.State):
    """Estado del dashboard de empleados."""

    # Estado de sesión de trabajo
    is_working: bool = False
    current_session: dict = {}
    work_description: str = ""

    # Datos cargados de la base de datos (simplificado)
    proyectos: list[dict] = []
    tareas: list[dict] = []
    jornadas: list[dict] = []
    horas_hoy: float = 0.0
    horas_semana: float = 0.0

    # Estado de carga
    is_loading: bool = False

    # Información del empleado
    empleado_id: str = ""
    empleado_nombre: str = ""

    async def on_mount(self):
        """Cargar datos al montar el componente."""
        await self.cargar_datos_desde_auth()

    async def cargar_datos_desde_auth(self):
        """Cargar datos usando información de autenticación."""
        self.is_loading = True

        try:
            # Obtener el estado de autenticación usando el estado padre
            from .employee_auth import EmployeeAuthState
            auth_state = await self.get_state(EmployeeAuthState)

            if auth_state and auth_state.employee_id:
                empleado_id = auth_state.employee_id
                empleado_nombre = auth_state.employee_name

                print(f"✅ Cargando datos para empleado: {empleado_nombre} ({empleado_id})")

                self.empleado_id = empleado_id
                self.empleado_nombre = empleado_nombre

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

                print(f"✅ Datos cargados: {len(self.proyectos)} proyectos, {len(self.tareas)} tareas")

            else:
                print("❌ No se pudo obtener información de autenticación")

        except Exception as e:
            print(f"❌ Error cargando datos del dashboard: {e}")
            import traceback
            traceback.print_exc()

        self.is_loading = False

    def start_work_session(self, proyecto_id: str = ""):
        """Iniciar sesión de trabajo."""
        if not self.is_working:
            # Si hay proyectos, usar el primero; si no hay proyectos, no permitir iniciar
            if proyecto_id:
                proyecto_para_usar = proyecto_id
            elif len(self.proyectos) > 0:
                proyecto_para_usar = self.proyectos[0]["id"]
            else:
                print("❌ No hay proyectos asignados. No se puede iniciar jornada.")
                return
            
            self.current_session = {
                "proyecto_id": proyecto_para_usar,
                "start_time": datetime.now().isoformat(),
                "description": ""
            }
            self.is_working = True
            print(f"✅ Jornada iniciada en proyecto: {proyecto_para_usar}")

    async def end_work_session(self):
        """Finalizar sesión de trabajo."""
        if self.is_working and self.current_session:
            start_time = datetime.fromisoformat(self.current_session["start_time"])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 3600  # horas

            # Usar el empleado_id ya cargado en el estado
            empleado_id = self.empleado_id
            proyecto_id = self.current_session.get("proyecto_id")

            # Validar que tengamos un proyecto válido
            if empleado_id and proyecto_id:
                jornada_data = registrar_jornada(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,
                    fecha=end_time.strftime('%Y-%m-%d'),
                    hora_inicio=start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    hora_fin=end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    descripcion=self.work_description or "Jornada de trabajo"
                )

                if jornada_data:
                    # Recargar datos después de registrar
                    await self.cargar_datos_desde_auth()
                    self.horas_hoy += duration
                    print(f"✅ Jornada registrada: {duration:.2f} horas")
                else:
                    print("❌ Error al registrar jornada")
            else:
                print(f"❌ No se puede registrar jornada: empleado_id={empleado_id}, proyecto_id={proyecto_id}")

            # Limpiar sesión
            self.is_working = False
            self.current_session = {}
            self.work_description = ""

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
                    rx.text(f"Horas trabajadas hoy: {EmployeeDashboardState.horas_hoy:.1f}h",
                           font_weight="600", font_size="1.1rem"),
                    rx.text(f"Horas esta semana: {EmployeeDashboardState.horas_semana:.1f}h",
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
                rx.vstack(
                    rx.text(f"Total: {EmployeeDashboardState.proyectos.length()} proyectos", 
                           font_weight="600", color=COLORS["primary"]),
                    rx.foreach(
                        EmployeeDashboardState.proyectos,
                        lambda p: rx.box(
                            rx.vstack(
                                rx.text(p["nombre"], font_weight="600", font_size="1rem"),
                                rx.text(f"Cliente: {p['cliente']}", 
                                       font_size="0.85rem", color=COLORS["text_light"]),
                                rx.text(f"Estado: {p['estado']}", 
                                       font_size="0.85rem", color=COLORS["success"]),
                                spacing="1",
                            ),
                            padding="0.75rem",
                            border="1px solid",
                            border_color=COLORS["border"],
                            border_radius="6px",
                            margin_bottom="0.5rem",
                            _hover={
                                "border_color": COLORS["primary"],
                                "background": COLORS["surface"]
                            }
                        )
                    ),
                    spacing="2",
                    width="100%",
                )
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
                rx.vstack(
                    rx.text(f"Total: {EmployeeDashboardState.tareas.length()} tareas", 
                           font_weight="600", color=COLORS["warning"]),
                    rx.foreach(
                        EmployeeDashboardState.tareas,
                        lambda t: rx.box(
                            rx.vstack(
                                rx.text(t["titulo"], font_weight="600", font_size="1rem"),
                                rx.hstack(
                                    rx.text(f"Estado: {t['estado']}", 
                                           font_size="0.85rem"),
                                    rx.text(f"Prioridad: {t['prioridad']}", 
                                           font_size="0.85rem", color=COLORS["warning"]),
                                    spacing="3",
                                ),
                                rx.text(f"Vence: {t['fecha_vencimiento']}", 
                                       font_size="0.8rem", color=COLORS["text_light"]),
                                spacing="1",
                            ),
                            padding="0.75rem",
                            border="1px solid",
                            border_color=COLORS["border"],
                            border_radius="6px",
                            margin_bottom="0.5rem",
                            _hover={
                                "border_color": COLORS["warning"],
                                "background": COLORS["surface"]
                            }
                        )
                    ),
                    spacing="2",
                    width="100%",
                )
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        size="3",
        padding="1.5rem",
    )


def employee_dashboard() -> rx.Component:
    """Dashboard principal para empleados."""
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

            # Información del empleado
            rx.card(
                rx.hstack(
                    rx.vstack(
                        rx.text("👤 Empleado:", font_weight="600"),
                        rx.text(EmployeeDashboardState.empleado_nombre, font_size="1.2rem"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("🆔 ID:", font_weight="600"),
                        rx.text(EmployeeDashboardState.empleado_id),
                        spacing="1",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                size="3",
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
                        rx.vstack(
                            rx.text(f"Total: {EmployeeDashboardState.jornadas.length()} jornadas", 
                                   font_weight="600", color=COLORS["info"]),
                            rx.foreach(
                                EmployeeDashboardState.jornadas,
                                lambda j: rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(j["fecha"], font_weight="600"),
                                            rx.text(f"{j['horas_trabajadas']}h", 
                                                   font_weight="600", color=COLORS["success"]),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.text(j['descripcion'], 
                                               font_size="0.85rem", color=COLORS["text_light"]),
                                        spacing="1",
                                    ),
                                    padding="0.75rem",
                                    border="1px solid",
                                    border_color=COLORS["border"],
                                    border_radius="6px",
                                    margin_bottom="0.5rem",
                                )
                            ),
                            spacing="2",
                            width="100%",
                        )
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
