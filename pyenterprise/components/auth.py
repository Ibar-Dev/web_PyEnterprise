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
    """Formulario de login moderno estilo landing."""
    return rx.box(
        rx.center(
            rx.box(
                rx.vstack(
                    # Logo y título - estilo landing
                    rx.vstack(
                        rx.box(
                            rx.image(
                                src="/logopylink.png",
                                alt="PyLink Logo",
                                width="70px",
                                height="70px",
                            ),
                            border_radius="50%",
                            padding="8px",
                            background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                            box_shadow="0 0 40px rgba(94, 234, 212, 0.6), 0 0 60px rgba(59, 130, 246, 0.4)",
                            transition="all 0.4s ease",
                            _hover={
                                "transform": "scale(1.05)",
                                "box_shadow": "0 0 50px rgba(94, 234, 212, 0.8), 0 0 80px rgba(59, 130, 246, 0.6)",
                            },
                        ),
                        rx.heading(
                            "PyLink",
                            size="8",
                            font_weight="900",
                            background="linear-gradient(45deg, #5EEAD4, #3B82F6, #00d4ff)",
                            background_clip="text",
                            _webkit_background_clip="text",
                            _webkit_text_fill_color="transparent",
                            text_shadow="0 0 30px rgba(94, 234, 212, 0.5)",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    
                    rx.heading(
                        "Acceso Empleados",
                        size="7",
                        text_align="center",
                        color="white",
                        font_weight="700",
                        margin_top="2rem",
                    ),
                    
                    rx.text(
                        "Ingresa tus credenciales corporativas",
                        color="rgba(255, 255, 255, 0.7)",
                        text_align="center",
                        font_size="1.1rem",
                        margin_bottom="2rem",
                    ),
                    
                    # Formulario moderno
                    rx.vstack(
                        rx.vstack(
                            rx.text("Correo Electrónico:", color="rgba(255, 255, 255, 0.9)", font_weight="600", font_size="0.9rem"),
                            rx.input(
                                placeholder="tu.email@pylink.com",
                                type="email",
                                value=AuthState.login_email,
                                on_change=AuthState.set_login_email,
                                size="3",
                                width="100%",
                                background="rgba(255, 255, 255, 0.1)",
                                border="1px solid rgba(94, 234, 212, 0.3)",
                                color="white",
                                _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                _focus={
                                    "border_color": "#5EEAD4",
                                    "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.2)",
                                    "background": "rgba(255, 255, 255, 0.15)",
                                },
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Contraseña:", color="rgba(255, 255, 255, 0.9)", font_weight="600", font_size="0.9rem"),
                            rx.input(
                                placeholder="••••••",
                                type="password", 
                                value=AuthState.login_password,
                                on_change=AuthState.set_login_password,
                                size="3",
                                width="100%",
                                background="rgba(255, 255, 255, 0.1)",
                                border="1px solid rgba(94, 234, 212, 0.3)",
                                color="white",
                                _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                _focus={
                                    "border_color": "#5EEAD4",
                                    "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.2)",
                                    "background": "rgba(255, 255, 255, 0.15)",
                                },
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        
                        # Mostrar error si existe
                        rx.cond(
                            AuthState.login_error != "",
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="triangle_alert", color="#EF4444"),
                                    rx.text(AuthState.login_error, color="white", font_weight="600"),
                                    spacing="2",
                                ),
                                padding="1rem",
                                border_radius="12px",
                                background="rgba(239, 68, 68, 0.2)",
                                border="1px solid rgba(239, 68, 68, 0.4)",
                                width="100%",
                            )
                        ),
                        
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="log_in", size=20),
                                rx.text("Iniciar Sesión", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=AuthState.login,
                            size="3",
                            width="100%",
                            background="linear-gradient(45deg, #5EEAD4, #3B82F6)",
                            color="white",
                            border="none",
                            border_radius="12px",
                            padding="1.2rem",
                            font_size="1.1rem",
                            box_shadow="0 10px 30px rgba(94, 234, 212, 0.4)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 15px 40px rgba(94, 234, 212, 0.6)",
                            },
                        ),
                        
                        spacing="5",
                        width="100%",
                    ),
                    
                    # Info de usuarios de prueba - estilo moderno
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="info", color="#5EEAD4"),
                                rx.text("Credenciales de Prueba:", font_weight="700", color="white"),
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(tag="user", size=16, color="rgba(255, 255, 255, 0.7)"),
                                    rx.text("Usuario: ", color="rgba(255, 255, 255, 0.7)", font_weight="600"),
                                    rx.text("juan@pylink.com / emp123", color="white"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon(tag="shield", size=16, color="#F59E0B"),
                                    rx.text("Admin: ", color="rgba(255, 255, 255, 0.7)", font_weight="600"),
                                    rx.text("admin@pylink.com / admin123", color="white"),
                                    spacing="2",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            spacing="3",
                            align="start",
                        ),
                        padding="1.5rem",
                        border_radius="16px",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        width="100%",
                        margin_top="1rem",
                    ),
                    
                    spacing="5",
                    align="center",
                    width="100%",
                    max_width="450px",
                ),
                padding="3rem 2.5rem",
                border_radius="24px",
                background="rgba(26, 26, 46, 0.8)",
                backdrop_filter="blur(20px)",
                box_shadow="0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(94, 234, 212, 0.1)",
                border="1px solid rgba(94, 234, 212, 0.2)",
            ),
            min_height="100vh",
            padding="2rem",
        ),
        
        # Fondo igual al landing
        background="""
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)
        """,
        min_height="100vh",
    )
