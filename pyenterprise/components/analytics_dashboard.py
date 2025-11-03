"""
Dashboard de analíticas para empleados y administradores
"""

import reflex as rx
from datetime import datetime, timedelta
from ..styles import COLORS
from ..database import (
    obtener_jornadas_empleado,
    obtener_tareas_empleado,
    obtener_todos_proyectos,
    obtener_todos_empleados,
    obtener_todas_tareas,
    obtener_todas_jornadas
)
from .employee_auth import EmployeeAuthState
from shared.analytics import (
    AnalyticsService,
    TimeStats,
    ProjectStats,
    TaskStats,
    EmployeeStats
)


class AnalyticsState(rx.State):
    """Estado para las analíticas"""

    # Datos cargados
    loading: bool = False
    error_message: str = ""

    # Estadísticas del empleado actual
    time_stats: TimeStats = TimeStats(0, 0, 0, 0)
    task_stats: TaskStats = TaskStats(0, 0, 0, 0, 0)

    # Estadísticas generales (para admin)
    project_stats: ProjectStats = ProjectStats(0, 0, 0, 0, 0)
    employee_stats: EmployeeStats = EmployeeStats(0, 0, 0, 0)

    # Datos de tendencias
    weekly_trend: list[dict] = []
    project_progress: list[dict] = []

    # Reporte de productividad
    productivity_report: dict = {}

    def load_employee_analytics(self):
        """Cargar analíticas del empleado actual"""
        self.loading = True
        self.error_message = ""

        try:
            if not EmployeeAuthState.employee_id:
                self.error_message = "No hay sesión activa"
                self.loading = False
                return

            # Cargar datos del empleado
            jornadas = obtener_jornadas_empleado(EmployeeAuthState.employee_id)
            tareas = obtener_tareas_empleado(EmployeeAuthState.employee_id)

            # Calcular estadísticas
            self.time_stats = AnalyticsService.calculate_time_stats(jornadas)
            self.task_stats = AnalyticsService.calculate_task_stats(tareas)
            self.weekly_trend = AnalyticsService.get_weekly_trend(jornadas)
            self.productivity_report = AnalyticsService.generate_productivity_report(jornadas, tareas)

        except Exception as e:
            self.error_message = f"Error cargando analíticas: {str(e)}"

        self.loading = False

    def load_admin_analytics(self):
        """Cargar analíticas de administrador"""
        self.loading = True
        self.error_message = ""

        try:
            # Cargar todos los datos
            proyectos = obtener_todos_proyectos()
            empleados = obtener_todos_empleados()
            tareas = obtener_todas_tareas()
            jornadas = obtener_todas_jornadas()

            # Calcular estadísticas
            self.project_stats = AnalyticsService.calculate_project_stats(proyectos)
            self.employee_stats = AnalyticsService.calculate_employee_stats(empleados, jornadas)
            self.project_progress = AnalyticsService.get_project_progress(proyectos, tareas)

        except Exception as e:
            self.error_message = f"Error cargando analíticas de admin: {str(e)}"

        self.loading = False


def stat_card(title: str, value: str, subtitle: str, icon: str, color: str = "primary") -> rx.Component:
    """Tarjeta de estadística"""
    return rx.card(
        rx.hstack(
            rx.box(
                rx.html(f'<i class="{icon}"></i>'),
                background_color=f"rgba({COLORS[color].lstrip('#')}, 0.1)",
                color=COLORS[color],
                padding="12px",
                border_radius="12px",
                font_size="24px",
                display="flex",
                align_items="center",
                justify_content="center",
                width="48px",
                height="48px"
            ),
            rx.vstack(
                rx.heading(title, size="4", color=COLORS["text_light"]),
                rx.text(value, font_size="2rem", font_weight="700", color=COLORS["text"]),
                rx.text(subtitle, font_size="0.875rem", color=COLORS["text_light"]),
                spacing="1",
                align_items="start",
            ),
            spacing="4",
            align_items="center",
            width="100%",
        ),
        padding="20px",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.05)",
        border=f"1px solid {COLORS['border']}",
        border_radius="12px",
        width="100%",
        transition="all 0.3s ease",
        _hover={
            "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.1)",
            "transform": "translateY(-4px)",
        }
    )


def progress_card(project: dict) -> rx.Component:
    """Tarjeta de progreso de proyecto"""
    progress_color = COLORS["success"] if project['progress_percentage'] >= 75 else \
                    COLORS["warning"] if project['progress_percentage'] >= 50 else \
                    COLORS["primary"]

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(project['project_name'], size="5", font_weight="600"),
                rx.badge(
                    project['status'].title(),
                    color_scheme="green" if project['status'] == 'activo' else "blue",
                    radius="full"
                ),
                justify="space-between",
                width="100%"
            ),
            rx.text(
                f"{project['completed_tasks']} de {project['total_tasks']} tareas completadas",
                font_size="0.875rem",
                color=COLORS["text_light"]
            ),
            rx.progress(
                value=project['progress_percentage'],
                width="100%",
                color_scheme="green" if project['progress_percentage'] >= 75 else "yellow",
                height="8px",
                border_radius="4px"
            ),
            rx.hstack(
                rx.text(f"{project['progress_percentage']}%", font_weight="600"),
                rx.text(f"€{project['budget']:,.0f}", color=COLORS["text_light"]),
                justify="space-between",
                width="100%"
            ),
            spacing="3",
            width="100%",
            align_items="start"
        ),
        padding="16px",
        border=f"1px solid {COLORS['border']}",
        border_radius="12px",
        width="100%",
        transition="all 0.3s ease",
        _hover={
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            "transform": "translateY(-2px)",
        }
    )


def weekly_trend_chart(trend_data: list[dict]) -> rx.Component:
    """Gráfico de tendencia semanal"""
    max_hours = max([d['hours'] for d in trend_data]) if trend_data else 1

    return rx.card(
        rx.vstack(
            rx.heading("Tendencia Semanal", size="5", font_weight="600"),
            rx.vstack(
                *[rx.hstack(
                    rx.text(week['week'], font_weight="500", width="100px"),
                    rx.box(
                        rx.box(
                            background_color=COLORS["primary"],
                            height="24px",
                            border_radius="4px",
                            width=f"{(week['hours'] / max_hours) * 100}%",
                            transition="all 0.3s ease"
                        ),
                        background_color=COLORS["surface"],
                        height="24px",
                        border_radius="4px",
                        flex="1",
                        overflow="hidden"
                    ),
                    rx.text(f"{week['hours']}h", font_weight="600", width="60px", text_align="right"),
                    align_items="center",
                    spacing="3",
                    width="100%"
                ) for week in trend_data],
                spacing="2",
                width="100%"
            ),
            spacing="4",
            width="100%",
            align_items="start"
        ),
        padding="20px",
        border=f"1px solid {COLORS['border']}",
        border_radius="12px",
        width="100%"
    )


def employee_analytics_dashboard() -> rx.Component:
    """Dashboard de analíticas para empleados"""
    return rx.vstack(
        rx.heading("Mis Analíticas", size="6", font_weight="700", margin_bottom="1rem"),

        # Loading state
        rx.cond(
            AnalyticsState.loading,
            rx.center(
                rx.spinner(size="3"),
                padding="2rem"
            )
        ),

        # Error state
        rx.cond(
            AnalyticsState.error_message != "",
            rx.callout(
                AnalyticsState.error_message,
                icon="alert_triangle",
                color_scheme="red"
            )
        ),

        # Main analytics content
        rx.cond(
            ~AnalyticsState.loading,
            rx.vstack(
                # Stats cards
                rx.grid(
                    stat_card(
                        "Horas Totales",
                        f"{AnalyticsState.time_stats.total_hours}h",
                        f"{AnalyticsState.time_stats.days_worked} días trabajados",
                        "clock",
                        "primary"
                    ),
                    stat_card(
                        "Tareas Completadas",
                        f"{AnalyticsState.task_stats.completed_tasks}",
                        f"de {AnalyticsState.task_stats.total_tasks} totales",
                        "check_circle",
                        "success"
                    ),
                    stat_card(
                        "Productividad",
                        f"{AnalyticsState.productivity_report.get('tasks_per_hour', 0):.2f}",
                        f"tareas/hora - {AnalyticsState.productivity_report.get('efficiency_rating', 'Normal')}",
                        "trending_up",
                        "info"
                    ),
                    stat_card(
                        "Horas Extra",
                        f"{AnalyticsState.time_stats.overtime_hours}h",
                        "este mes",
                        "clock",
                        "warning"
                    ),
                    columns="4",
                    spacing="4",
                    width="100%"
                ),

                # Charts and trends
                rx.grid(
                    weekly_trend_chart(AnalyticsState.weekly_trend),

                    # Productivity score
                    rx.card(
                        rx.vstack(
                            rx.heading("Score de Productividad", size="5", font_weight="600"),
                            rx.center(
                                rx.vstack(
                                    rx.text(
                                        f"{AnalyticsState.productivity_report.get('productivity_score', 0)}",
                                        font_size="3rem",
                                        font_weight="700",
                                        color=COLORS["primary"]
                                    ),
                                    rx.text(
                                        AnalyticsState.productivity_report.get('efficiency_rating', 'Normal'),
                                        font_size="1.25rem",
                                        font_weight="500",
                                        color=COLORS["text"]
                                    ),
                                    spacing="1"
                                )
                            ),
                            spacing="4",
                            width="100%",
                            align_items="center"
                        ),
                        padding="20px",
                        border=f"1px solid {COLORS['border']}",
                        border_radius="12px",
                        width="100%"
                    ),
                    columns="2",
                    spacing="4",
                    width="100%"
                ),

                spacing="6",
                width="100%",
                align_items="start"
            )
        ),

        width="100%",
        align_items="center",
        padding="2rem"
    )


def admin_analytics_dashboard() -> rx.Component:
    """Dashboard de analíticas para administradores"""
    return rx.vstack(
        rx.heading("Analíticas del Sistema", size="6", font_weight="700", margin_bottom="1rem"),

        # Loading state
        rx.cond(
            AnalyticsState.loading,
            rx.center(
                rx.spinner(size="3"),
                padding="2rem"
            )
        ),

        # Main analytics content
        rx.cond(
            ~AnalyticsState.loading,
            rx.vstack(
                # Overview stats
                rx.grid(
                    stat_card(
                        "Proyectos Activos",
                        f"{AnalyticsState.project_stats.active_projects}",
                        f"de {AnalyticsState.project_stats.total_projects} totales",
                        "briefcase",
                        "primary"
                    ),
                    stat_card(
                        "Empleados Activos",
                        f"{AnalyticsState.employee_stats.active_employees}",
                        f"{AnalyticsState.employee_stats.new_employees_this_month} nuevos este mes",
                        "users",
                        "success"
                    ),
                    stat_card(
                        "Presupuesto Total",
                        f"€{AnalyticsState.project_stats.total_budget:,.0f}",
                        f"€{AnalyticsService.project_stats.average_project_value:,.0f} promedio por proyecto",
                        "dollar_sign",
                        "info"
                    ),
                    stat_card(
                        "Horas Promedio",
                        f"{AnalyticsState.employee_stats.average_hours_per_employee:.1f}h",
                        "por empleado activo",
                        "clock",
                        "warning"
                    ),
                    columns="4",
                    spacing="4",
                    width="100%"
                ),

                # Project progress
                rx.card(
                    rx.vstack(
                        rx.heading("Progreso de Proyectos", size="5", font_weight="600"),
                        rx.vstack(
                            *[progress_card(project) for project in AnalyticsState.project_progress[:5]],
                            spacing="3",
                            width="100%"
                        ),
                        spacing="4",
                        width="100%",
                        align_items="start"
                    ),
                    padding="24px",
                    border=f"1px solid {COLORS['border']}",
                    border_radius="12px",
                    width="100%"
                ),

                spacing="6",
                width="100%",
                align_items="start"
            )
        ),

        width="100%",
        align_items="center",
        padding="2rem"
    )