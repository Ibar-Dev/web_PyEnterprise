"""
Dashboard básico para empleados PyLink
Evita errores de UUID hasta tener autenticación completa
"""

import reflex as rx
from ..styles import *


class EmployeeDashboardState(rx.State):
    """Estado básico del dashboard de empleados."""

    # Estado simple
    is_loading: bool = False

    def start_work_session(self, proyecto_id: str):
        """Iniciar sesión de trabajo."""
        pass

    def end_work_session(self):
        """Finalizar sesión de trabajo."""
        pass

    def set_work_description(self, description: str):
        """Actualizar descripción de la sesión de trabajo."""
        pass


def time_control_card() -> rx.Component:
    """Tarjeta de control de tiempo."""
    return rx.card(
        rx.vstack(
            rx.heading("⏰ Control de Tiempo", size="5"),
            rx.text("Gestión de jornadas laborales"),

            rx.text("Horas trabajadas hoy: 0.0h",
                   font_weight="600", font_size="1.1rem"),
            rx.text("Horas esta semana: 0.0h",
                   font_size="0.9rem", color=COLORS["text_light"]),

            rx.button(
                "🟢 Iniciar Jornada",
                on_click=lambda: EmployeeDashboardState.start_work_session("default"),
                background=COLORS["success"],
                color="white",
                width="100%",
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

            rx.text("Los proyectos aparecerán aquí una vez que inicies sesión correctamente"),

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

            rx.text("Las tareas aparecerán aquí una vez que inicies sesión correctamente"),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        size="3",
        padding="1.5rem",
    )


def employee_dashboard() -> rx.Component:
    """Dashboard básico para empleados."""
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

            # Información adicional
            rx.card(
                rx.vstack(
                    rx.heading("📋 Información", size="5"),
                    rx.text("Para ver tus proyectos, tareas y horas trabajadas:"),
                    rx.text("1. Inicia sesión con tu cuenta corporativa", font_weight="600"),
                    rx.text("2. El sistema cargará automáticamente tus datos", font_weight="600"),
                    rx.text("3. Podrás registrar jornadas laborales", font_weight="600"),

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
    )
