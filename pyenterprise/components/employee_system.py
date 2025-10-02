"""
Sistema completo de empleados para PyLink - Versión Frontend
"""

import reflex as rx
from datetime import datetime
from ..styles import *
from .auth import AuthState

class EmployeeSystemState(rx.State):
    """Estado del sistema de empleados."""
    
    # Control de tiempo
    is_working: bool = False
    current_project: str = ""
    work_start_time: str = ""
    work_description: str = ""
    daily_hours: float = 0.0
    weekly_hours: float = 32.5
    
    # Datos estáticos de proyectos
    projects: list = [
        {
            "id": "PROJ001",
            "name": "E-commerce Tienda Online",
            "client": "TechStore S.A.",
            "progress": 68,
            "deadline": "2024-11-15",
            "status": "En Progreso",
            "assigned": True,
            "priority": "Alta"
        },
        {
            "id": "PROJ002", 
            "name": "App Móvil Delivery",
            "client": "FastFood Corp",
            "progress": 25,
            "deadline": "2024-12-01",
            "status": "Iniciado",
            "assigned": True,
            "priority": "Media"
        },
        {
            "id": "PROJ003",
            "name": "Sistema CRM Empresarial",
            "client": "BusinessHub Ltd",
            "progress": 90,
            "deadline": "2024-10-30", 
            "status": "Finalizando",
            "assigned": False,
            "priority": "Alta"
        }
    ]
    
    # Datos estáticos de tareas
    tasks: list = [
        {
            "id": "T001",
            "title": "Implementar carrito de compras",
            "project": "E-commerce Tienda Online",
            "status": "En Progreso",
            "priority": "Alta",
            "due_date": "2024-10-25",
            "estimated_hours": 8,
            "completed_hours": 5
        },
        {
            "id": "T002",
            "title": "Diseñar mockups de la app",
            "project": "App Móvil Delivery", 
            "status": "Completada",
            "priority": "Media",
            "due_date": "2024-10-20",
            "estimated_hours": 12,
            "completed_hours": 12
        },
        {
            "id": "T003",
            "title": "Optimizar base de datos",
            "project": "E-commerce Tienda Online",
            "status": "Pendiente",
            "priority": "Baja",
            "due_date": "2024-10-28",
            "estimated_hours": 6,
            "completed_hours": 0
        },
        {
            "id": "T004",
            "title": "Integrar sistema de pagos",
            "project": "E-commerce Tienda Online", 
            "status": "En Progreso",
            "priority": "Alta",
            "due_date": "2024-10-30",
            "estimated_hours": 16,
            "completed_hours": 3
        }
    ]
    
    # Historial de horas
    time_entries: list = [
        {"date": "2024-10-21", "project": "E-commerce", "hours": 8.5, "description": "Desarrollo del carrito de compras"},
        {"date": "2024-10-20", "project": "App Móvil", "hours": 7.0, "description": "Diseño de interfaces"},
        {"date": "2024-10-19", "project": "E-commerce", "hours": 8.0, "description": "Integración de API de pagos"},
        {"date": "2024-10-18", "project": "E-commerce", "hours": 9.0, "description": "Testing y corrección de bugs"},
    ]
    
    def start_work_session(self, project_id: str):
        """Iniciar sesión de trabajo."""
        self.is_working = True
        self.current_project = project_id
        self.work_start_time = datetime.now().strftime("%H:%M")
        
    def end_work_session(self):
        """Finalizar sesión de trabajo."""
        if self.is_working:
            self.is_working = False
            self.daily_hours += 2.5  # Simular 2.5 horas trabajadas
            self.weekly_hours += 2.5
            self.current_project = ""
            self.work_start_time = ""
            self.work_description = ""
    
    def set_work_description(self, description: str):
        """Actualizar descripción del trabajo."""
        self.work_description = description


def project_card(project: dict) -> rx.Component:
    """Tarjeta de proyecto individual."""
    status_colors = {
        "En Progreso": "blue",
        "Iniciado": "yellow", 
        "Finalizando": "green",
        "Completado": "emerald"
    }
    
    priority_colors = {
        "Alta": "red",
        "Media": "yellow",
        "Baja": "green"
    }
    
    return rx.card(
        rx.vstack(
            # Header del proyecto
            rx.hstack(
                rx.badge(project["status"], color_scheme=status_colors.get(project["status"], "gray")),
                rx.badge(f"#{project['id']}", variant="outline", size="1"),
                justify="between",
                width="100%",
            ),
            
            rx.heading(project["name"], size="4", margin_bottom="0.5rem"),
            rx.text(f"Cliente: {project['client']}", color=COLORS["text_light"], font_size="0.9rem"),
            rx.text(f"Vence: {project['deadline']}", color=COLORS["text_light"], font_size="0.9rem"),
            
            # Barra de progreso
            rx.vstack(
                rx.hstack(
                    rx.text("Progreso:", font_size="0.9rem", font_weight="500"),
                    rx.text(f"{project['progress']}%", font_weight="600", color=COLORS["primary"]),
                    justify="between",
                    width="100%",
                ),
                rx.progress(value=int(project["progress"]), width="100%", color_scheme="blue"),
                spacing="1",
                width="100%",
            ),
            
            # Acciones del proyecto
            rx.hstack(
                rx.badge(f"Prioridad {project['priority']}", color_scheme=priority_colors.get(project["priority"], "gray"), size="1"),
                rx.cond(
                    project["assigned"],
                    rx.cond(
                        ~EmployeeSystemState.is_working,
                        rx.button(
                            "Iniciar Trabajo",
                            size="2",
                            on_click=lambda pid=project["id"]: EmployeeSystemState.start_work_session(pid),
                            style=button_primary_style,
                        ),
                        rx.text("🟢 Activo", color="green", font_weight="600", font_size="0.9rem")
                    ),
                    rx.text("No asignado", color=COLORS["text_light"], font_size="0.8rem")
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            
            spacing="3",
            align="start",
            width="100%",
        ),
        size="3",
        style={
            **card_style,
            "min_height": "220px",
        },
    )


def task_card(task: dict) -> rx.Component:
    """Tarjeta de tarea individual."""
    status_colors = {
        "Completada": "green",
        "En Progreso": "blue", 
        "Pendiente": "gray"
    }
    
    priority_colors = {
        "Alta": "red",
        "Media": "yellow",
        "Baja": "green"
    }
    
    progress = int((task["completed_hours"] / task["estimated_hours"]) * 100) if task["estimated_hours"] > 0 else 0
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(task["status"], color_scheme=status_colors.get(task["status"], "gray")),
                rx.badge(task["priority"], color_scheme=priority_colors.get(task["priority"], "gray"), size="1"),
                justify="between",
                width="100%",
            ),
            
            rx.text(task["title"], font_weight="600", font_size="1rem"),
            rx.text(f"Proyecto: {task['project']}", color=COLORS["text_light"], font_size="0.8rem"),
            rx.text(f"Vence: {task['due_date']}", color=COLORS["text_light"], font_size="0.8rem"),
            
            # Progreso de horas
            rx.vstack(
                rx.hstack(
                    rx.text("Horas:", font_size="0.8rem"),
                    rx.text(f"{task['completed_hours']}/{task['estimated_hours']}h", font_weight="600", font_size="0.8rem"),
                    justify="between",
                    width="100%",
                ),
                rx.progress(value=progress, width="100%", size="1"),
                spacing="1",
                width="100%",
            ),
            
            spacing="2",
            align="start",
            width="100%",
        ),
        size="2",
        style=card_style,
    )


def time_tracking_panel() -> rx.Component:
    """Panel de control de tiempo."""
    return rx.card(
        rx.vstack(
            rx.heading("Control de Tiempo", size="4"),
            
            # Estadísticas de tiempo
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.text("Hoy", font_weight="600", color=COLORS["text_light"]),
                        rx.text(f"{EmployeeSystemState.daily_hours}h", font_size="1.5rem", font_weight="800", color=COLORS["primary"]),
                        align="center",
                    ),
                    size="2",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Esta Semana", font_weight="600", color=COLORS["text_light"]),
                        rx.text(f"{EmployeeSystemState.weekly_hours}h", font_size="1.5rem", font_weight="800", color=COLORS["success"]),
                        align="center",
                    ),
                    size="2",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Objetivo", font_weight="600", color=COLORS["text_light"]),
                        rx.text("40h", font_size="1.5rem", font_weight="800", color=COLORS["text_light"]),
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
                EmployeeSystemState.is_working,
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.text("🟢", font_size="1.2rem"),
                            rx.text("Sesión Activa", font_weight="600", color="green"),
                            spacing="2",
                        ),
                        rx.text(f"Proyecto: {EmployeeSystemState.current_project}", font_size="0.9rem"),
                        rx.text(f"Inicio: {EmployeeSystemState.work_start_time}", font_size="0.9rem", color=COLORS["text_light"]),
                        
                        rx.input(
                            placeholder="¿En qué estás trabajando?",
                            value=EmployeeSystemState.work_description,
                            on_change=EmployeeSystemState.set_work_description,
                            width="100%",
                        ),
                        
                        rx.button(
                            "Finalizar Sesión",
                            on_click=EmployeeSystemState.end_work_session,
                            color_scheme="red",
                            width="100%",
                        ),
                        
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                    style={"border": "2px solid green", "background": "rgba(0, 255, 0, 0.05)"},
                ),
                rx.text("Selecciona un proyecto para iniciar el seguimiento de tiempo.", text_align="center", color=COLORS["text_light"]),
            ),
            
            spacing="4",
            width="100%",
        ),
        size="3",
    )


def time_history_panel() -> rx.Component:
    """Panel del historial de horas."""
    return rx.card(
        rx.vstack(
            rx.heading("Historial de Horas", size="4"),
            
            # Historial estático
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("2024-10-21", font_weight="600", font_size="0.9rem"),
                        rx.text("E-commerce", color=COLORS["text_light"], font_size="0.8rem"),
                        align="start",
                        spacing="1",
                    ),
                    rx.text("8.5h", font_weight="600", color=COLORS["primary"]),
                    justify="between",
                    align="center",
                    width="100%",
                    padding="0.5rem",
                    border_bottom=f"1px solid {COLORS['border']}",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("2024-10-20", font_weight="600", font_size="0.9rem"),
                        rx.text("App Móvil", color=COLORS["text_light"], font_size="0.8rem"),
                        align="start",
                        spacing="1",
                    ),
                    rx.text("7.0h", font_weight="600", color=COLORS["primary"]),
                    justify="between",
                    align="center",
                    width="100%",
                    padding="0.5rem",
                    border_bottom=f"1px solid {COLORS['border']}",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("2024-10-19", font_weight="600", font_size="0.9rem"),
                        rx.text("E-commerce", color=COLORS["text_light"], font_size="0.8rem"),
                        align="start",
                        spacing="1",
                    ),
                    rx.text("8.0h", font_weight="600", color=COLORS["primary"]),
                    justify="between",
                    align="center",
                    width="100%",
                    padding="0.5rem",
                    border_bottom=f"1px solid {COLORS['border']}",
                ),
                spacing="0",
                width="100%",
            ),
            
            spacing="3",
            width="100%",
        ),
        size="3",
    )


def employee_dashboard() -> rx.Component:
    """Dashboard principal de empleados.""" 
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.heading(f"¡Hola, Juan Pérez!", size="6"),
                    rx.text(f"Desarrollador Frontend • ID: EMP001", color=COLORS["text_light"]),
                    align="start",
                    spacing="1",
                ),
                rx.hstack(
                    rx.button(
                        "Mi Perfil",
                        variant="outline",
                        size="2",
                    ),
                    rx.button(
                        "Cerrar Sesión",
                        on_click=AuthState.logout,
                        variant="outline",
                        color_scheme="red",
                        size="2",
                    ),
                    spacing="3",
                ),
                justify="between",
                align="center",
                width="100%",
                padding="2rem 0 1rem 0",
            ),
            
            # Panel de control de tiempo
            time_tracking_panel(),
            
            # Contenido principal en grid
            rx.grid(
                # Columna izquierda - Proyectos
                rx.vstack(
                    rx.heading("Mis Proyectos", size="5", margin_bottom="1rem"),
                    # Proyectos asignados estáticos
                    project_card({
                        "id": "PROJ001",
                        "name": "E-commerce Tienda Online",
                        "client": "TechStore S.A.",
                        "progress": 68,
                        "deadline": "2024-11-15",
                        "status": "En Progreso",
                        "assigned": True,
                        "priority": "Alta"
                    }),
                    project_card({
                        "id": "PROJ002", 
                        "name": "App Móvil Delivery",
                        "client": "FastFood Corp",
                        "progress": 25,
                        "deadline": "2024-12-01",
                        "status": "Iniciado",
                        "assigned": True,
                        "priority": "Media"
                    }),
                    spacing="0",
                    align="start",
                    width="100%",
                ),
                
                # Columna central - Tareas
                rx.vstack(
                    rx.heading("Mis Tareas", size="5", margin_bottom="1rem"),
                    # Tareas estáticas
                    task_card({
                        "id": "T001",
                        "title": "Implementar carrito de compras",
                        "project": "E-commerce Tienda Online",
                        "status": "En Progreso",
                        "priority": "Alta",
                        "due_date": "2024-10-25",
                        "estimated_hours": 8,
                        "completed_hours": 5
                    }),
                    task_card({
                        "id": "T002",
                        "title": "Diseñar mockups de la app",
                        "project": "App Móvil Delivery", 
                        "status": "Completada",
                        "priority": "Media",
                        "due_date": "2024-10-20",
                        "estimated_hours": 12,
                        "completed_hours": 12
                    }),
                    task_card({
                        "id": "T004",
                        "title": "Integrar sistema de pagos",
                        "project": "E-commerce Tienda Online", 
                        "status": "En Progreso",
                        "priority": "Alta",
                        "due_date": "2024-10-30",
                        "estimated_hours": 16,
                        "completed_hours": 3
                    }),
                    spacing="0",
                    align="start",
                    width="100%",
                ),
                
                # Columna derecha - Historial
                rx.vstack(
                    time_history_panel(),
                    spacing="0",
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
        max_width="1400px",
        padding="2rem",
    )
