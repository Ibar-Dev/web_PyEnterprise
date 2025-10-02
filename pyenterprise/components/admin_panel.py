"""
Panel de administración para PyLink
"""

import reflex as rx
from ..styles import *
from .auth import AuthState
from .employee_dashboard import EmployeeDashboardState

class AdminState(rx.State):
    """Estado del panel de administración."""
    
    # Formularios para crear proyectos
    new_project_name: str = ""
    new_project_client: str = ""
    new_project_deadline: str = ""
    new_project_description: str = ""
    
    # Formularios para crear tareas
    new_task_title: str = ""
    new_task_project: str = ""
    new_task_assignee: str = ""
    new_task_priority: str = "Media"  
    new_task_due_date: str = ""
    new_task_description: str = ""
    
    # Lista de empleados
    employees: list = [
        {"id": "EMP001", "name": "Juan Pérez", "role": "developer", "email": "juan@pylink.com"},
        {"id": "EMP002", "name": "María García", "role": "designer", "email": "maria@pylink.com"},
        {"id": "EMP003", "name": "Carlos López", "role": "developer", "email": "carlos@pylink.com"},
    ]
    
    show_create_project: bool = False
    show_create_task: bool = False
    
    def create_project(self):
        """Crear nuevo proyecto."""
        if self.new_project_name and self.new_project_client and self.new_project_deadline:
            new_project = {
                "id": f"PROJ{len(EmployeeDashboardState.active_projects) + 1:03d}",
                "name": self.new_project_name,
                "client": self.new_project_client,
                "deadline": self.new_project_deadline,
                "progress": 0,
                "assigned_employees": [],
                "status": "Iniciado"
            }
            EmployeeDashboardState.active_projects.append(new_project)
            
            # Limpiar formulario
            self.new_project_name = ""
            self.new_project_client = ""
            self.new_project_deadline = ""
            self.new_project_description = ""
            self.show_create_project = False
    
    def create_task(self):
        """Crear nueva tarea."""
        if self.new_task_title and self.new_task_project and self.new_task_assignee:
            new_task = {
                "id": f"TASK{len(EmployeeDashboardState.tasks) + 1:03d}",
                "title": self.new_task_title,
                "project_id": self.new_task_project,
                "assigned_to": self.new_task_assignee,
                "status": "Pendiente",
                "priority": self.new_task_priority,
                "due_date": self.new_task_due_date
            }
            EmployeeDashboardState.tasks.append(new_task)
            
            # Limpiar formulario
            self.new_task_title = ""
            self.new_task_project = ""
            self.new_task_assignee = ""
            self.new_task_priority = "Media"
            self.new_task_due_date = ""
            self.new_task_description = ""
            self.show_create_task = False
    
    def toggle_create_project(self):
        self.show_create_project = not self.show_create_project
    
    def toggle_create_task(self):
        self.show_create_task = not self.show_create_task


def create_project_form() -> rx.Component:
    """Formulario para crear proyecto."""
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Crear Nuevo Proyecto", size="4"),
                
                rx.input(
                    placeholder="Nombre del proyecto",
                    value=AdminState.new_project_name,
                    on_change=AdminState.set_new_project_name,
                    required=True,
                ),
                
                rx.input(
                    placeholder="Cliente",
                    value=AdminState.new_project_client,
                    on_change=AdminState.set_new_project_client,
                    required=True,
                ),
                
                rx.input(
                    type="date",
                    placeholder="Fecha límite",
                    value=AdminState.new_project_deadline,
                    on_change=AdminState.set_new_project_deadline,
                    required=True,
                ),
                
                rx.text_area(
                    placeholder="Descripción del proyecto",
                    value=AdminState.new_project_description,
                    on_change=AdminState.set_new_project_description,
                    rows="3",
                ),
                
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=AdminState.toggle_create_project,
                        variant="outline",
                    ),
                    rx.button(
                        "Crear Proyecto",
                        on_click=AdminState.create_project,
                        style=button_primary_style,
                    ),
                    spacing="3",
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        size="3",
    )


def create_task_form() -> rx.Component:
    """Formulario para crear tarea."""
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Crear Nueva Tarea", size="4"),
                
                rx.input(
                    placeholder="Título de la tarea",
                    value=AdminState.new_task_title,
                    on_change=AdminState.set_new_task_title,
                    required=True,
                ),
                
                rx.select(
                    [rx.option(p["name"], value=p["id"]) for p in EmployeeDashboardState.active_projects],
                    placeholder="Seleccionar proyecto",
                    value=AdminState.new_task_project,
                    on_change=AdminState.set_new_task_project,
                ),
                
                rx.select(
                    [rx.option(emp["name"], value=emp["id"]) for emp in AdminState.employees],
                    placeholder="Asignar a empleado",
                    value=AdminState.new_task_assignee,
                    on_change=AdminState.set_new_task_assignee,
                ),
                
                rx.select(
                    ["Alta", "Media", "Baja"],
                    placeholder="Prioridad",
                    value=AdminState.new_task_priority,
                    on_change=AdminState.set_new_task_priority,
                ),
                
                rx.input(
                    type="date",
                    placeholder="Fecha de vencimiento",
                    value=AdminState.new_task_due_date,
                    on_change=AdminState.set_new_task_due_date,
                ),
                
                rx.text_area(
                    placeholder="Descripción de la tarea",
                    value=AdminState.new_task_description,
                    on_change=AdminState.set_new_task_description,
                    rows="3",
                ),
                
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=AdminState.toggle_create_task,
                        variant="outline",
                    ),
                    rx.button(
                        "Crear Tarea",
                        on_click=AdminState.create_task,
                        style=button_primary_style,
                    ),
                    spacing="3",
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
        size="3",
    )


def project_management_card(project: dict) -> rx.Component:
    """Tarjeta de gestión de proyecto para admin."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(project["name"], size="4"),
                rx.badge(project["status"], color_scheme="blue"),
                justify="between",
                align="center",
                width="100%",
            ),
            
            rx.text(f"Cliente: {project['client']}", color=COLORS["text_light"]),
            rx.text(f"ID: {project['id']}", font_size="0.8rem", color=COLORS["text_light"]),
            rx.text(f"Progreso: {project['progress']}%", font_weight="600"),
            
            rx.progress(value=project["progress"], width="100%"),
            
            rx.hstack(
                rx.button("Editar", size="2", variant="outline"),
                rx.button("Ver Tareas", size="2"),
                rx.button("Asignar Empleados", size="2", style=button_primary_style),
                spacing="2",
            ),
            
            spacing="3",
            align="start",
            width="100%",
        ),
        size="3",
        style=card_style,
    )


def admin_panel() -> rx.Component:
    """Panel de administración principal."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Panel de Administración", size="6"),
                rx.hstack(
                    rx.badge("Admin", color_scheme="red"),
                    rx.button(
                        "Volver al Dashboard",
                        on_click=lambda: rx.redirect("/empleados/dashboard"),
                        variant="outline",
                    ),
                    rx.button(
                        "Cerrar Sesión",
                        on_click=AuthState.logout,
                        variant="outline",
                        color_scheme="red",
                    ),
                    spacing="3",
                ),
                justify="between",
                align="center",
                width="100%",
                padding="2rem 0",
            ),
            
            # Botones de acción principales
            rx.hstack(
                rx.button(
                    rx.icon("plus", size=16),
                    "Crear Proyecto",
                    on_click=AdminState.toggle_create_project,
                    style=button_primary_style,
                ),
                rx.button(
                    rx.icon("plus", size=16),
                    "Crear Tarea", 
                    on_click=AdminState.toggle_create_task,
                    style=button_secondary_style,
                ),
                spacing="3",
                margin_bottom="2rem",
            ),
            
            # Formularios (se muestran condicionalmente)
            rx.cond(AdminState.show_create_project, create_project_form()),
            rx.cond(AdminState.show_create_task, create_task_form()),
            
            # Pestañas de gestión
            rx.tabs(
                rx.tab_list(
                    rx.tab("Proyectos", value="projects"),
                    rx.tab("Tareas", value="tasks"),
                    rx.tab("Empleados", value="employees"),
                    rx.tab("Reportes", value="reports"),
                ),
                
                rx.tab_panels(
                    # Panel Proyectos
                    rx.tab_panel(
                        rx.vstack(
                            rx.heading("Gestión de Proyectos", size="5", margin_bottom="1rem"),
                            rx.grid(
                                *[project_management_card(p) for p in EmployeeDashboardState.active_projects],
                                columns="2",
                                spacing="4",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="projects",
                    ),
                    
                    # Panel Tareas
                    rx.tab_panel(
                        rx.vstack(
                            rx.heading("Gestión de Tareas", size="5", margin_bottom="1rem"),
                            rx.data_table(
                                data=[
                                    {
                                        "ID": t["id"],
                                        "Título": t["title"],
                                        "Proyecto": t["project_id"],
                                        "Asignado a": next((emp["name"] for emp in AdminState.employees if emp["id"] == t["assigned_to"]), "N/A"),
                                        "Estado": t["status"],
                                        "Prioridad": t["priority"],
                                        "Vencimiento": t["due_date"]
                                    }
                                    for t in EmployeeDashboardState.tasks
                                ],
                                pagination=True,
                                search=True,
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="tasks",
                    ),
                    
                    # Panel Empleados
                    rx.tab_panel(
                        rx.vstack(
                            rx.heading("Gestión de Empleados", size="5", margin_bottom="1rem"),
                            rx.data_table(
                                data=[
                                    {
                                        "ID": emp["id"],
                                        "Nombre": emp["name"],
                                        "Rol": emp["role"],
                                        "Email": emp["email"]
                                    }
                                    for emp in AdminState.employees
                                ],
                                pagination=True,
                                search=True,
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="employees",
                    ),
                    
                    # Panel Reportes
                    rx.tab_panel(
                        rx.vstack(
                            rx.heading("Reportes y Estadísticas", size="5", margin_bottom="1rem"),
                            rx.grid(
                                rx.card(
                                    rx.vstack(
                                        rx.heading("Proyectos Activos", size="4"),
                                        rx.text(f"{len(EmployeeDashboardState.active_projects)}", font_size="2rem", font_weight="800", color=COLORS["primary"]),
                                        align="center",
                                    ),
                                    size="3",
                                ),
                                rx.card(
                                    rx.vstack(
                                        rx.heading("Tareas Pendientes", size="4"),
                                        rx.text(f"{len([t for t in EmployeeDashboardState.tasks if t['status'] == 'Pendiente'])}", font_size="2rem", font_weight="800", color=COLORS["warning"]),
                                        align="center",
                                    ),
                                    size="3",
                                ),
                                rx.card(
                                    rx.vstack(
                                        rx.heading("Empleados Activos", size="4"),
                                        rx.text(f"{len(AdminState.employees)}", font_size="2rem", font_weight="800", color=COLORS["success"]),
                                        align="center",
                                    ),
                                    size="3",
                                ),
                                columns="3",
                                spacing="4",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="reports",
                    ),
                ),
                
                default_value="projects",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="2rem",
    )
