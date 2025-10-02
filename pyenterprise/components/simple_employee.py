"""
Sistema de empleados simplificado para PyLink
"""

import reflex as rx
from ..styles import *
from .auth import AuthState

class SimpleEmployeeState(rx.State):
    """Estado simplificado para empleados."""
    is_working: bool = False
    work_hours: float = 0.0

    def toggle_work(self):
        """Alternar estado de trabajo."""
        self.is_working = not self.is_working
        if not self.is_working:
            self.work_hours += 1.0  # Agregar una hora de trabajo


def simple_employee_dashboard() -> rx.Component:
    """Dashboard simplificado para empleados."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Dashboard Empleados", size="6"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    variant="outline",
                    color_scheme="red",
                ),
                justify="between",
                width="100%",
                padding="2rem 0",
            ),
            
            # Panel de tiempo
            rx.card(
                rx.vstack(
                    rx.heading("Control de Tiempo", size="4"),
                    rx.text(f"Horas trabajadas: {SimpleEmployeeState.work_hours}h", font_weight="600"),
                    
                    rx.cond(
                        SimpleEmployeeState.is_working,
                        rx.vstack(
                            rx.text("🟢 Trabajando", color="green", font_size="1.2rem"),
                            rx.button(
                                "Finalizar Jornada",
                                on_click=SimpleEmployeeState.toggle_work,
                                color_scheme="red",
                            ),
                            spacing="2",
                        ),
                        rx.button(
                            "Iniciar Jornada",
                            on_click=SimpleEmployeeState.toggle_work,
                            style=button_primary_style,
                        ),
                    ),
                    
                    spacing="3",
                    align="center",
                ),
                size="3",
            ),
            
            # Proyectos
            rx.card(
                rx.vstack(
                    rx.heading("Proyectos Activos", size="4"),
                    rx.text("📊 E-commerce Tienda Online - En Progreso (65%)"),
                    rx.text("📱 App Móvil Delivery - Iniciado (30%)"),
                    rx.text("💼 Sistema CRM Empresarial - Finalizando (85%)"),
                    spacing="2",
                    align="start",
                ),
                size="3",
            ),
            
            # Tareas
            rx.card(
                rx.vstack(
                    rx.heading("Mis Tareas", size="4"),
                    rx.text("✅ Diseñar interfaz de usuario - Completada"),
                    rx.text("🔧 Implementar carrito de compras - En Progreso"),
                    rx.text("⏳ Configurar base de datos - Pendiente"),
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


def simple_admin_panel() -> rx.Component:
    """Panel de administración simplificado."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Panel de Administración", size="6"),
                rx.hstack(
                    rx.badge("Admin", color_scheme="red"),
                    rx.button(
                        "Dashboard",
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
                width="100%",
                padding="2rem 0",
            ),
            
            # Estadísticas
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Proyectos", size="4"),
                        rx.text("3", font_size="2rem", font_weight="800", color=COLORS["primary"]),
                        rx.text("Activos", color=COLORS["text_light"]),
                        align="center",
                    ),
                    size="3",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Empleados", size="4"),
                        rx.text("3", font_size="2rem", font_weight="800", color=COLORS["success"]),
                        rx.text("Registrados", color=COLORS["text_light"]),
                        align="center",
                    ),
                    size="3",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Tareas", size="4"),
                        rx.text("5", font_size="2rem", font_weight="800", color=COLORS["warning"]),
                        rx.text("Pendientes", color=COLORS["text_light"]),
                        align="center",
                    ),
                    size="3",
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
            
            # Información del sistema
            rx.card(
                rx.vstack(
                    rx.heading("Sistema de Gestión", size="4"),
                    rx.text("✅ Sistema de autenticación funcionando"),
                    rx.text("✅ Control de tiempo implementado"),
                    rx.text("✅ Dashboard para empleados activo"),
                    rx.text("⚙️ Próximamente: Creación de proyectos"),
                    rx.text("⚙️ Próximamente: Asignación de tareas"),
                    spacing="2",
                    align="start",
                ),
                size="3",
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="1000px",
        padding="2rem",
    )
