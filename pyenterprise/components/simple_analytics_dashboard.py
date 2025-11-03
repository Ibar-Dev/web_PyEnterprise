"""
Dashboard simplificado con analíticas básicas
"""

import reflex as rx
from ..styles import COLORS
from .employee_auth import EmployeeAuthState
from .analytics_dashboard import AnalyticsState, employee_analytics_dashboard


def simple_employee_dashboard() -> rx.Component:
    """Dashboard simplificado con pestañas"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Dashboard de Empleados", font_size="2rem", color="white", font_weight="700"),
                rx.button(
                    "Cerrar Sesión",
                    background_color=COLORS["error"],
                    color="white",
                    on_click=EmployeeAuthState.logout,
                    size="2"
                ),
                justify="space-between",
                width="100%",
                margin_bottom="2rem",
            ),

            # Tab navigation
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Principal", value="main"),
                    rx.tabs.trigger("Analíticas", value="analytics"),
                    padding="0",
                    border_bottom=f"1px solid {COLORS['border']}",
                    margin_bottom="2rem",
                ),

                rx.tabs.content(
                    value="main",
                    rx.grid(
                        # Time control card
                        rx.card(
                            rx.vstack(
                                rx.heading("Control de Tiempo", size="4"),
                                rx.text("Gestiona tus jornadas de trabajo"),
                                rx.button("Iniciar Jornada", color_scheme="green", size="2"),
                                spacing="3",
                                padding="20px",
                                align_items="center"
                            ),
                            width="100%"
                        ),

                        # Projects card
                        rx.card(
                            rx.vstack(
                                rx.heading("Mis Proyectos", size="4"),
                                rx.text("Proyectos asignados a ti"),
                                rx.button("Ver Proyectos", color_scheme="blue", size="2"),
                                spacing="3",
                                padding="20px",
                                align_items="center"
                            ),
                            width="100%"
                        ),

                        # Tasks card
                        rx.card(
                            rx.vstack(
                                rx.heading("Mis Tareas", size="4"),
                                rx.text("Tareas pendientes y en progreso"),
                                rx.button("Ver Tareas", color_scheme="purple", size="2"),
                                spacing="3",
                                padding="20px",
                                align_items="center"
                            ),
                            width="100%"
                        ),
                        columns="3",
                        spacing="4",
                        width="100%"
                    )
                ),

                rx.tabs.content(
                    value="analytics",
                    employee_analytics_dashboard()
                ),

                value="main",
                width="100%"
            ),

            spacing="6",
            width="100%",
            max_width="1200px",
            padding="2rem",
        ),

        # Background
        background=f"""
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)
        """,
        min_height="100vh",
        on_mount=AnalyticsState.load_employee_analytics,
    )