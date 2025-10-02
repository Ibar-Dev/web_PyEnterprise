"""
Sistema de empleados ultra-simple para PyLink
"""

import reflex as rx
from ..styles import *

class UltraSimpleState(rx.State):
    """Estado ultra-simple."""
    is_logged_in: bool = False
    username: str = ""
    password: str = ""
    error_message: str = ""

    def login(self):
        """Login básico."""
        if self.username == "juan@pylink.com" and self.password == "emp123":
            self.is_logged_in = True
            self.error_message = ""
        else:
            self.error_message = "Credenciales incorrectas"

    def logout(self):
        """Logout."""
        self.is_logged_in = False
        self.username = ""
        self.password = ""
        self.error_message = ""

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password


def ultra_simple_login() -> rx.Component:
    """Login ultra-simple."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Sistema de Empleados PyLink", size="5"),
                rx.text("Acceso para empleados", color=COLORS["text_light"]),
                
                rx.input(
                    placeholder="Email",
                    value=UltraSimpleState.username,
                    on_change=UltraSimpleState.set_username,
                    width="100%",
                ),
                
                rx.input(
                    placeholder="Contraseña",
                    type="password",
                    value=UltraSimpleState.password,
                    on_change=UltraSimpleState.set_password,
                    width="100%",
                ),
                
                rx.cond(
                    UltraSimpleState.error_message != "",
                    rx.text(UltraSimpleState.error_message, color="red"),
                ),
                
                rx.button(
                    "Iniciar Sesión",
                    on_click=UltraSimpleState.login,
                    width="100%",
                    style=button_primary_style,
                ),
                
                rx.text("Usuario de prueba: juan@pylink.com / emp123", 
                       font_size="0.8rem", 
                       color=COLORS["text_light"]),
                
                spacing="4",
                align="center",
                width="100%",
            ),
            size="4",
            max_width="400px",
        ),
        min_height="100vh",
    )


def ultra_simple_dashboard() -> rx.Component:
    """Dashboard ultra-simple."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Dashboard - Juan Pérez", size="5"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=UltraSimpleState.logout,
                    color_scheme="red",
                    variant="outline",
                ),
                justify="between",
                width="100%",
                padding="1rem 0",
            ),
            
            # Control de tiempo
            rx.card(
                rx.vstack(
                    rx.heading("⏰ Control de Tiempo", size="4"),
                    rx.text("Horas trabajadas hoy: 7.5 horas", font_weight="600"),
                    rx.text("Horas esta semana: 37.5 horas"),
                    rx.button("🟢 Iniciar Jornada", style=button_primary_style),
                    spacing="3",
                    align="center",
                ),
                width="100%",
            ),
            
            # Grid de información
            rx.grid(
                # Proyectos
                rx.card(
                    rx.vstack(
                        rx.heading("📊 Mis Proyectos", size="4"),
                        rx.vstack(
                            rx.text("🛒 E-commerce Tienda Online", font_weight="600"),
                            rx.text("Cliente: TechStore S.A."),
                            rx.text("Progreso: 68% ▓▓▓▓▓▓▓░░░"),
                            rx.text("Estado: En Progreso", color="blue"),
                            
                            rx.divider(),
                            
                            rx.text("📱 App Móvil Delivery", font_weight="600"),
                            rx.text("Cliente: FastFood Corp"),
                            rx.text("Progreso: 25% ▓▓▓░░░░░░░"),
                            rx.text("Estado: Iniciado", color="orange"),
                            
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                ),
                
                # Tareas
                rx.card(
                    rx.vstack(
                        rx.heading("✅ Mis Tareas", size="4"),
                        rx.vstack(
                            rx.hstack(
                                rx.text("🔧", font_size="1.2rem"),
                                rx.vstack(
                                    rx.text("Implementar carrito de compras", font_weight="600"),
                                    rx.text("Prioridad: Alta • En Progreso", color="red", font_size="0.9rem"),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            
                            rx.hstack(
                                rx.text("✅", font_size="1.2rem"),
                                rx.vstack(
                                    rx.text("Diseñar mockups de la app", font_weight="600"),
                                    rx.text("Prioridad: Media • Completada", color="green", font_size="0.9rem"),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            
                            rx.hstack(
                                rx.text("⏳", font_size="1.2rem"),
                                rx.vstack(
                                    rx.text("Integrar sistema de pagos", font_weight="600"),
                                    rx.text("Prioridad: Alta • Pendiente", color="gray", font_size="0.9rem"),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                ),
                
                columns="2",
                spacing="4",
                width="100%",
            ),
            
            # Historial de horas
            rx.card(
                rx.vstack(
                    rx.heading("📈 Historial de Horas", size="4"),
                    rx.grid(
                        rx.text("📅 2024-10-21: 8.5h • E-commerce"),
                        rx.text("📅 2024-10-20: 7.0h • App Móvil"),
                        rx.text("📅 2024-10-19: 8.0h • E-commerce"),  
                        rx.text("📅 2024-10-18: 9.0h • Testing"),
                        columns="2",
                        spacing="2",
                        width="100%",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="1000px",
        padding="2rem",
    )
