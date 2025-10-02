"""
Sistema de autenticación para empleados PyLink
"""

import reflex as rx
from ..styles import *

class AuthState(rx.State):
    """Estado de autenticación."""
    is_authenticated: bool = False
    current_user: dict = {}
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    is_admin: bool = False

    def login(self):
        """Autenticar usuario."""
        # Usuarios de prueba
        users = {
            "admin@pylink.com": {
                "password": "admin123",
                "name": "Administrador",
                "role": "admin",
                "employee_id": "ADMIN001"
            },
            "juan@pylink.com": {
                "password": "emp123", 
                "name": "Juan Pérez",
                "role": "developer",
                "employee_id": "EMP001"
            },
            "maria@pylink.com": {
                "password": "emp123",
                "name": "María García", 
                "role": "designer",
                "employee_id": "EMP002"
            }
        }
        
        if self.login_email in users:
            user = users[self.login_email]
            if user["password"] == self.login_password:
                self.is_authenticated = True
                self.current_user = user
                self.is_admin = user["role"] == "admin"
                self.login_error = ""
                return rx.redirect("/empleados/dashboard")
            else:
                self.login_error = "Contraseña incorrecta"
        else:
            self.login_error = "Usuario no encontrado"
    
    def logout(self):
        """Cerrar sesión."""
        self.is_authenticated = False
        self.current_user = {}
        self.is_admin = False
        self.login_email = ""
        self.login_password = ""
        return rx.redirect("/empleados")

    def set_login_email(self, email: str):
        self.login_email = email
    
    def set_login_password(self, password: str):
        self.login_password = password


def login_form() -> rx.Component:
    """Formulario de login para empleados."""
    return rx.container(
        rx.center(
            rx.card(
                rx.vstack(
                    # Logo y título
                    rx.hstack(
                        rx.image(
                            src="/logo.png",
                            alt="PyLink Logo",
                            width="40px",
                            height="40px",
                        ),
                        rx.heading(
                            "PyLink",
                            size="6",
                            color=COLORS["primary"],
                            font_weight="800",
                        ),
                        align="center",
                        spacing="3",
                        margin_bottom="2rem",
                    ),
                    
                    rx.heading(
                        "Acceso Empleados",
                        size="5",
                        text_align="center",
                        margin_bottom="1rem",
                    ),
                    
                    rx.text(
                        "Ingresa tus credenciales para acceder al sistema",
                        color=COLORS["text_light"],
                        text_align="center",
                        margin_bottom="2rem",
                    ),
                    
                    # Formulario
                    rx.vstack(
                        rx.input(
                            placeholder="Email corporativo",
                            type="email",
                            value=AuthState.login_email,
                            on_change=AuthState.set_login_email,
                            size="3",
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Contraseña",
                            type="password", 
                            value=AuthState.login_password,
                            on_change=AuthState.set_login_password,
                            size="3",
                            width="100%",
                        ),
                        
                        # Mostrar error si existe
                        rx.cond(
                            AuthState.login_error != "",
                            rx.callout(
                                AuthState.login_error,
                                icon="triangle_alert",
                                color_scheme="red",
                                size="2",
                            )
                        ),
                        
                        rx.button(
                            "Iniciar Sesión",
                            on_click=AuthState.login,
                            size="3",
                            width="100%",
                            style=button_primary_style,
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    
                    # Info de usuarios de prueba
                    rx.divider(),
                    rx.callout(
                        rx.vstack(
                            rx.text("👤 Usuarios de prueba:", font_weight="600"),
                            rx.text("• admin@pylink.com / admin123 (Admin)"),
                            rx.text("• juan@pylink.com / emp123 (Desarrollador)"),
                            rx.text("• maria@pylink.com / emp123 (Diseñadora)"),
                            spacing="1",
                        ),
                        icon="info",
                        color_scheme="blue",
                        size="1",
                    ),
                    
                    spacing="4",
                    align="center",
                    width="100%",
                    max_width="400px",
                ),
                size="4",
                style={
                    "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.1)",
                    "border": f"1px solid {COLORS['border']}",
                },
            ),
            min_height="100vh",
            padding="2rem",
        ),
        max_width="500px",
        margin="0 auto",
    )
