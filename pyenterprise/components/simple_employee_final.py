"""
Sistema de empleados simplificado y estable para PyLink
"""

import reflex as rx
from ..styles import *
from .auth import AuthState

class SimpleEmployeeState(rx.State):
    """Estado simplificado para empleados."""
    is_working: bool = False
    current_project: str = ""
    daily_hours: float = 7.5
    weekly_hours: float = 37.5

    def start_work(self, project: str):
        """Iniciar trabajo en un proyecto."""
        self.is_working = True
        self.current_project = project

    def stop_work(self):
        """Finalizar trabajo."""
        self.is_working = False
        self.current_project = ""
        self.daily_hours += 1.0
        self.weekly_hours += 1.0


def project_simple_card(title: str, client: str, progress: int, status: str) -> rx.Component:
    """Tarjeta simple de proyecto."""
    status_color = "blue" if status == "En Progreso" else "green" if status == "Finalizando" else "yellow"
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(status, color_scheme=status_color),
                rx.text(f"{progress}%", font_weight="600", color=COLORS["primary"]),
                justify="between",
                width="100%",
            ),
            rx.heading(title, size="4"),
            rx.text(f"Cliente: {client}", color=COLORS["text_light"]),
            rx.progress(value=progress, width="100%"),
            
            rx.cond(
                ~SimpleEmployeeState.is_working,
                rx.button(
                    "Iniciar Trabajo",
                    on_click=lambda: SimpleEmployeeState.start_work(title),
                    style=button_primary_style,
                    size="2",
                ),
                rx.text("🟢 Activo", color="green", font_weight="600")
            ),
            
            spacing="3",
            align="start",
            width="100%",
        ),
        size="3",
        style=card_style,
    )


def task_simple_card(title: str, project: str, status: str, priority: str) -> rx.Component:
    """Tarjeta simple de tarea."""
    status_color = "green" if status == "Completada" else "blue" if status == "En Progreso" else "gray"
    priority_color = "red" if priority == "Alta" else "yellow" if priority == "Media" else "green"
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(status, color_scheme=status_color),
                rx.badge(priority, color_scheme=priority_color, size="1"),
                justify="between",
                width="100%",
            ),
            rx.text(title, font_weight="600"),
            rx.text(f"Proyecto: {project}", color=COLORS["text_light"], font_size="0.9rem"),
            spacing="2",
            align="start",
            width="100%",
        ),
        size="2",
    )


def employee_dashboard_simple() -> rx.Component:
    """Dashboard simplificado de empleados."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.heading("¡Hola, Juan Pérez!", size="6"),
                    rx.text("Desarrollador Frontend • ID: EMP001", color=COLORS["text_light"]),
                    align="start",
                    spacing="1",
                ),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    variant="outline",
                    color_scheme="red",
                ),
                justify="between",
                align="center",
                width="100%",
                padding="2rem 0",
            ),
            
            # Panel de tiempo
            rx.card(
                rx.vstack(
                    rx.heading("Control de Tiempo", size="4"),
                    
                    rx.grid(
                        rx.card(
                            rx.vstack(
                                rx.text("Horas Hoy", font_weight="600"),
                                rx.text(f"{SimpleEmployeeState.daily_hours}h", font_size="1.5rem", color=COLORS["primary"]),
                                align="center",
                            ),
                            size="2",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Esta Semana", font_weight="600"),
                                rx.text(f"{SimpleEmployeeState.weekly_hours}h", font_size="1.5rem", color=COLORS["success"]),
                                align="center",
                            ),
                            size="2",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Objetivo", font_weight="600"),
                                rx.text("40h", font_size="1.5rem", color=COLORS["text_light"]),
                                align="center",
                            ),
                            size="2",
                        ),
                        columns="3",
                        spacing="3",
                        width="100%",
                    ),
                    
                    # Panel de sesión activa
                    rx.cond(
                        SimpleEmployeeState.is_working,
                        rx.card(
                            rx.vstack(
                                rx.text("🟢 Sesión Activa", color="green", font_weight="600", font_size="1.2rem"),
                                rx.text(f"Trabajando en: {SimpleEmployeeState.current_project}"),
                                rx.button(
                                    "Finalizar Sesión",
                                    on_click=SimpleEmployeeState.stop_work,
                                    color_scheme="red",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            style={"border": "2px solid green"},
                        ),
                        rx.text("Selecciona un proyecto para iniciar el seguimiento", text_align="center", color=COLORS["text_light"])
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                size="3",
            ),
            
            # Contenido principal
            rx.grid(
                # Proyectos
                rx.vstack(
                    rx.heading("Mis Proyectos", size="5"),
                    project_simple_card("E-commerce Tienda Online", "TechStore S.A.", 68, "En Progreso"),
                    project_simple_card("App Móvil Delivery", "FastFood Corp", 25, "En Progreso"), 
                    project_simple_card("Sistema CRM", "BusinessHub Ltd", 90, "Finalizando"),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                
                # Tareas
                rx.vstack(
                    rx.heading("Mis Tareas", size="5"),
                    task_simple_card("Implementar carrito de compras", "E-commerce", "En Progreso", "Alta"),
                    task_simple_card("Diseñar mockups de la app", "App Móvil", "Completada", "Media"),
                    task_simple_card("Optimizar base de datos", "E-commerce", "Pendiente", "Baja"),
                    task_simple_card("Integrar sistema de pagos", "E-commerce", "En Progreso", "Alta"),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                
                # Historial
                rx.vstack(
                    rx.heading("Historial de Horas", size="5"),
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.text("2024-10-21", font_weight="600"),
                                rx.text("8.5h", color=COLORS["primary"]),
                                justify="between",
                                width="100%",
                            ),
                            rx.text("E-commerce - Desarrollo del carrito", color=COLORS["text_light"], font_size="0.9rem"),
                            
                            rx.divider(),
                            
                            rx.hstack(
                                rx.text("2024-10-20", font_weight="600"),
                                rx.text("7.0h", color=COLORS["primary"]),
                                justify="between",
                                width="100%",
                            ),
                            rx.text("App Móvil - Diseño de interfaces", color=COLORS["text_light"], font_size="0.9rem"),
                            
                            rx.divider(),
                            
                            rx.hstack(
                                rx.text("2024-10-19", font_weight="600"),
                                rx.text("8.0h", color=COLORS["primary"]),
                                justify="between",
                                width="100%",
                            ),
                            rx.text("E-commerce - API de pagos", color=COLORS["text_light"], font_size="0.9rem"),
                            
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        size="3",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                
                columns="3",
                spacing="6",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="2rem",
    )
