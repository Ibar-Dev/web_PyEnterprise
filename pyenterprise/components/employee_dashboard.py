"""
Dashboard principal para empleados PyLink
"""

import reflex as rx
from datetime import datetime, timedelta
from ..styles import *
from .auth import AuthState

class EmployeeDashboardState(rx.State):
    """Estado del dashboard de empleados."""
    active_projects: list = [
        {
            "id": "PROJ001",
            "name": "E-commerce Tienda Online",
            "client": "TechStore S.A.",
            "deadline": "2024-11-15",
            "progress": 65,
            "assigned_employees": ["EMP001", "EMP002"],
            "status": "En Progreso"
        },
        {
            "id": "PROJ002", 
            "name": "App Móvil Delivery",
            "client": "FastFood Corp",
            "deadline": "2024-12-01",
            "progress": 30,
            "assigned_employees": ["EMP001"],
            "status": "Iniciado"
        },
        {
            "id": "PROJ003",
            "name": "Sistema CRM Empresarial", 
            "client": "BusinessHub Ltd",
            "deadline": "2024-10-30",
            "progress": 85,
            "assigned_employees": ["EMP002"],
            "status": "Por Finalizar"
        }
    ]
    
    current_session: dict = {}
    is_working: bool = False
    work_description: str = ""
    selected_project: str = ""
    work_hours_today: float = 0.0
    
    tasks: list = [
        {
            "id": "TASK001",
            "title": "Implementar carrito de compras",
            "project_id": "PROJ001",
            "assigned_to": "EMP001",
            "status": "En Progreso",
            "priority": "Alta",
            "due_date": "2024-10-25"
        },
        {
            "id": "TASK002",
            "title": "Diseñar interfaz de usuario",
            "project_id": "PROJ001", 
            "assigned_to": "EMP002",
            "status": "Completada",
            "priority": "Media",
            "due_date": "2024-10-20"
        },
        {
            "id": "TASK003",
            "title": "Configurar base de datos",
            "project_id": "PROJ002",
            "assigned_to": "EMP001", 
            "status": "Pendiente",
            "priority": "Alta",
            "due_date": "2024-10-28"
        }
    ]

    def start_work_session(self, project_id: str):
        """Iniciar sesión de trabajo."""
        if not self.is_working:
            self.current_session = {
                "project_id": project_id,
                "start_time": datetime.now().isoformat(),
                "description": ""
            }
            self.is_working = True
            self.selected_project = project_id

    def end_work_session(self):
        """Finalizar sesión de trabajo."""
        if self.is_working and self.current_session:
            start_time = datetime.fromisoformat(self.current_session["start_time"])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 3600  # horas
            
            # Guardar sesión (aquí iría la lógica de BD)
            session_record = {
                "project_id": self.current_session["project_id"],
                "start_time": start_time,
                "end_time": end_time,
                "duration": round(duration, 2),
                "description": self.work_description,
                "employee_id": AuthState.current_user.get("employee_id", "")
            }
            
            self.work_hours_today += duration
            self.is_working = False
            self.current_session = {}
            self.work_description = ""
            self.selected_project = ""

    def set_work_description(self, description: str):
        self.work_description = description

    @rx.var
    def my_projects(self) -> list:
        """Obtener proyectos asignados al usuario actual.""" 
        return self.active_projects  # Por ahora mostramos todos los proyectos

    @rx.var
    def my_tasks(self) -> list:
        """Obtener tareas asignadas al usuario actual."""
        return self.tasks  # Por ahora mostramos todas las tareas


def project_card(project: dict) -> rx.Component:
    """Tarjeta de proyecto."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    project["status"],
                    color_scheme="blue" if project["status"] == "En Progreso" else "green" if project["status"] == "Por Finalizar" else "gray",
                ),
                rx.text(f"#{project['id']}", font_size="0.8rem", color=COLORS["text_light"]),
                justify="between",
                width="100%",
            ),
            
            rx.heading(project["name"], size="4", margin_bottom="0.5rem"),
            rx.text(f"Cliente: {project['client']}", color=COLORS["text_light"]),
            rx.text(f"Fecha límite: {project['deadline']}", color=COLORS["text_light"]),
            
            # Barra de progreso
            rx.vstack(
                rx.hstack(
                    rx.text("Progreso:", font_size="0.9rem"),
                    rx.text(f"{project['progress']}%", font_weight="600"),
                    justify="between",
                    width="100%",
                ),
                rx.progress(value=project["progress"], width="100%"),
                spacing="1",
                width="100%",
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    "Ver Detalles",
                    size="2",
                    variant="outline",
                ),
                rx.cond(
                    ~EmployeeDashboardState.is_working,
                    rx.button(
                        "Iniciar Trabajo",
                        size="2",
                        on_click=lambda: EmployeeDashboardState.start_work_session(project["id"]),
                        style=button_primary_style,
                    ),
                    rx.text("🟢 Sesión activa", color="green", font_weight="600")
                ),
                justify="between",
                width="100%",
            ),
            
            spacing="3",
            align="start",
            width="100%",
        ),
        size="3",
        style=card_style,
    )


def task_item(task: dict) -> rx.Component:
    """Item de tarea."""
    priority_colors = {
        "Alta": "red",
        "Media": "yellow", 
        "Baja": "green"
    }
    
    status_colors = {
        "Completada": "green",
        "En Progreso": "blue",
        "Pendiente": "gray"
    }
    
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text(task["title"], font_weight="600"),
                    rx.badge(task["priority"], color_scheme=priority_colors.get(task["priority"], "gray"), size="1"),
                    spacing="2",
                ),
                rx.text(f"Proyecto: #{task['project_id']}", font_size="0.8rem", color=COLORS["text_light"]),
                rx.text(f"Vence: {task['due_date']}", font_size="0.8rem", color=COLORS["text_light"]),
                align="start",
                flex="1",
            ),
            rx.badge(
                task["status"],
                color_scheme=status_colors.get(task["status"], "gray"),
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        size="2",
        margin_bottom="0.5rem",
    )


def work_session_panel() -> rx.Component:
    """Panel de sesión de trabajo activa - simplificado.""" 
    return rx.cond(
        EmployeeDashboardState.is_working,
        rx.card(
            rx.vstack(
                rx.text("🟢 Sesión de Trabajo Activa", color="green", font_weight="600", font_size="1.2rem"),
                rx.text("Proyecto en progreso..."),
                rx.button(
                    "Finalizar Sesión",
                    on_click=EmployeeDashboardState.end_work_session,
                    color_scheme="red",
                ),
                spacing="3",
                align="center",
            ),
            style={"border": "2px solid green"},
        )
    )


def employee_dashboard() -> rx.Component:
    """Dashboard principal para empleados."""
    return rx.container(
        rx.vstack(
            # Header simple
            rx.hstack(
                rx.heading("Dashboard de Empleados", size="6"),
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
            
            # Panel de control de tiempo
            rx.card(
                rx.vstack(
                    rx.heading("Control de Tiempo", size="4"),
                    rx.text("Sistema de seguimiento de horas simplificado"),
                    
                    rx.cond(
                        ~EmployeeDashboardState.is_working,
                        rx.button(
                            "Iniciar Jornada",
                            on_click=lambda: EmployeeDashboardState.start_work_session("PROJ001"),
                            style=button_primary_style,
                        ),
                        rx.vstack(
                            rx.text("🟢 Sesión Activa", color="green", font_weight="600"),
                            rx.button(
                                "Finalizar Jornada",
                                on_click=EmployeeDashboardState.end_work_session,
                                color_scheme="red",
                            ),
                            spacing="2",
                        )
                    ),
                    
                    spacing="3",
                    align="center",
                ),
                size="3",
            ),
            
            # Proyectos estáticos por ahora
            rx.card(
                rx.vstack(
                    rx.heading("Proyectos Disponibles", size="4"),
                    rx.text("• E-commerce Tienda Online - En Progreso"),
                    rx.text("• App Móvil Delivery - Iniciado"), 
                    rx.text("• Sistema CRM Empresarial - Por Finalizar"),
                    spacing="2",
                    align="start",
                ),
                size="3",
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="800px",
        padding="2rem",
    )
