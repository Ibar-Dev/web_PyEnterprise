"""
Dashboard de empleados mejorado con analíticas integradas
"""

import reflex as rx
from datetime import datetime
from ..styles import COLORS
from ..database import (
    obtener_proyectos_empleado,
    obtener_tareas_empleado,
    obtener_jornadas_empleado,
    registrar_jornada,
    actualizar_estado_tarea
)
from .employee_auth import EmployeeAuthState
from .employee_dashboard_integrated import EmployeeDashboardState
from .analytics_dashboard import (
    AnalyticsState,
    employee_analytics_dashboard
)


class EnhancedEmployeeDashboardState(EmployeeDashboardState):
    """Estado mejorado del dashboard con analíticas"""

    # Analytics state
    analytics_state: AnalyticsState = AnalyticsState()

    # UI state
    active_tab: str = "dashboard"  # dashboard, analytics

    def toggle_tab(self, tab: str):
        """Cambiar entre tabs del dashboard"""
        self.active_tab = tab
        if tab == "analytics":
            self.analytics_state.load_employee_analytics()

    def on_mount(self):
        """Cargar datos al montar el componente"""
        # Cargar datos del dashboard original
        self.cargar_datos_empleado()

        # Cargar analíticas
        self.analytics_state.load_employee_analytics()


def enhanced_employee_dashboard() -> rx.Component:
    """Dashboard de empleados mejorado con analíticas"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Dashboard de Empleados", font_size="2.5rem", color="white", font_weight="700"),
                rx.hstack(
                    rx.badge(
                        EmployeeAuthState.employee_role.title(),
                        color_scheme="blue",
                        radius="full"
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("log_out", size=16),
                            rx.text("Cerrar Sesión", font_weight="600"),
                            spacing="2"
                        ),
                        background="rgba(239, 68, 68, 0.2)",
                        border="1px solid rgba(239, 68, 68, 0.4)",
                        color="#EF4444",
                        size="2",
                        _hover={"background": "rgba(239, 68, 68, 0.3)"},
                        on_click=EmployeeAuthState.logout,
                    ),
                    spacing="3",
                    align_items="center"
                ),
                justify="space-between",
                align_items="center",
                width="100%",
                margin_bottom="2rem",
            ),

            # Employee info
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text("Empleado:", font_weight="500", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),
                        rx.text(EmployeeAuthState.employee_name, font_size="1.3rem", color="white", font_weight="600"),
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.text(f"Último acceso: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                           font_size="0.875rem", color="rgba(255, 255, 255, 0.6)"),
                    align_items="center",
                    width="100%",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(94, 234, 212, 0.2)",
                backdrop_filter="blur(10px)",
                margin_bottom="2rem",
            ),

            # Tab navigation
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        "Dashboard Principal",
                        value="dashboard",
                        padding="12px 24px",
                        font_weight="500",
                        _selected={"background_color": "rgba(94, 234, 212, 0.1)", "border_bottom": "2px solid #5EEAD4"}
                    ),
                    rx.tabs.trigger(
                        "Mis Analíticas",
                        value="analytics",
                        padding="12px 24px",
                        font_weight="500",
                        _selected={"background_color": "rgba(94, 234, 212, 0.1)", "border_bottom": "2px solid #5EEAD4"}
                    ),
                    rx.tabs.trigger(
                        "Reportes",
                        value="reports",
                        padding="12px 24px",
                        font_weight="500",
                        _selected={"background_color": "rgba(94, 234, 212, 0.1)", "border_bottom": "2px solid #5EEAD4"}
                    ),
                    padding="0",
                    border_bottom=f"1px solid {COLORS['border']}",
                    margin_bottom="2rem",
                ),

                rx.tabs.content(
                    value="dashboard",
                    # Dashboard principal original (simplificado)
                    rx.grid(
                        # Time control card
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("clock", size=24, color=COLORS["primary"]),
                                    rx.heading("Control de Tiempo", size="5", font_weight="600"),
                                    align_items="center",
                                    spacing="3"
                                ),
                                rx.cond(
                                    EnhancedEmployeeDashboardState.is_working,
                                    rx.vstack(
                                        rx.text("Trabajando actualmente", color=COLORS["success"], font_weight="500"),
                                        rx.text(f"Inicio: {EnhancedEmployeeDashboardState.current_session.get('hora_inicio', 'N/A')}",
                                               font_size="0.875rem", color=COLORS["text_light"]),
                                        rx.button(
                                            "Finalizar Jornada",
                                            background_color=COLORS["error"],
                                            color="white",
                                            size="3",
                                            on_click=EnhancedEmployeeDashboardState.end_work_session
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.vstack(
                                        rx.text("No estás trabajando", color=COLORS["text_light"]),
                                        rx.button(
                                            "Iniciar Jornada",
                                            background_color=COLORS["success"],
                                            color="white",
                                            size="3",
                                            on_click=EnhancedEmployeeDashboardState.start_work_session
                                        ),
                                        spacing="3",
                                        align="center"
                                    )
                                ),
                                spacing="4",
                                padding="24px",
                                align_items="center",
                                width="100%"
                            ),
                            width="100%"
                        ),

                        # Quick stats
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("briefcase", size=24, color=COLORS["primary"]),
                                    rx.heading("Mis Proyectos", size="5", font_weight="600"),
                                    align_items="center",
                                    spacing="3"
                                ),
                                rx.text(
                                    f"{len(EnhancedEmployeeDashboardState.proyectos)} proyectos activos",
                                    font_size="1.5rem",
                                    font_weight="700",
                                    color=COLORS["primary"],
                                    text_align="center"
                                ),
                                rx.text(
                                    "Ver todos los proyectos",
                                    color=COLORS["primary"],
                                    cursor="pointer",
                                    _hover={"text_decoration": "underline"}
                                ),
                                spacing="3",
                                padding="24px",
                                align_items="center",
                                width="100%"
                            ),
                            width="100%"
                        ),

                        # Tasks overview
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("check_square", size=24, color=COLORS["primary"]),
                                    rx.heading("Mis Tareas", size="5", font_weight="600"),
                                    align_items="center",
                                    spacing="3"
                                ),
                                rx.text(
                                    f"{len([t for t in EnhancedEmployeeDashboardState.tareas if t.get('estado') == 'pendiente'])} tareas pendientes",
                                    font_size="1.5rem",
                                    font_weight="700",
                                    color=COLORS["warning"],
                                    text_align="center"
                                ),
                                rx.text(
                                    "Ver todas las tareas",
                                    color=COLORS["primary"],
                                    cursor="pointer",
                                    _hover={"text_decoration": "underline"}
                                ),
                                spacing="3",
                                padding="24px",
                                align_items="center",
                                width="100%"
                            ),
                            width="100%"
                        ),
                        columns="3",
                        spacing="6",
                        width="100%"
                    )
                ),

                rx.tabs.content(
                    value="analytics",
                    employee_analytics_dashboard()
                ),

                rx.tabs.content(
                    value="reports",
                    rx.card(
                        rx.vstack(
                            rx.heading("Reportes Disponibles", size="5", font_weight="600"),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("file_text", size=20, color=COLORS["primary"]),
                                    rx.vstack(
                                        rx.heading("Reporte Semanal", size="4", font_weight="500"),
                                        rx.text("Resumen de tu actividad de la última semana", font_size="0.875rem"),
                                        spacing="1"
                                    ),
                                    rx.button("Descargar", size="2", color_scheme="blue"),
                                    justify="space-between",
                                    align_items="center",
                                    width="100%",
                                    padding="16px",
                                    border=f"1px solid {COLORS['border']}",
                                    border_radius="8px",
                                    _hover={"background_color": COLORS["surface"]}
                                ),
                                rx.hstack(
                                    rx.icon("bar_chart", size=20, color=COLORS["primary"]),
                                    rx.vstack(
                                        rx.heading("Reporte de Productividad", size="4", font_weight="500"),
                                        rx.text("Análisis detallado de tu rendimiento", font_size="0.875rem"),
                                        spacing="1"
                                    ),
                                    rx.button("Ver", size="2", color_scheme="green"),
                                    justify="space-between",
                                    align_items="center",
                                    width="100%",
                                    padding="16px",
                                    border=f"1px solid {COLORS['border']}",
                                    border_radius="8px",
                                    _hover={"background_color": COLORS["surface"]}
                                ),
                                spacing="3",
                                width="100%"
                            ),
                            spacing="4",
                            width="100%",
                            align="start"
                        ),
                        padding="24px",
                        width="100%"
                    )
                ),

                value=EnhancedEmployeeDashboardState.active_tab,
                on_change=lambda tab: EnhancedEmployeeDashboardState.toggle_tab(tab),
                width="100%"
            ),

            spacing="6",
            width="100%",
            max_width="1400px",
        ),

        # Background
        background=f"""
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)
        """,
        min_height="100vh",
        padding="3rem",
        on_mount=EnhancedEmployeeDashboardState.on_mount,
    )