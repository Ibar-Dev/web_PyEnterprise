"""
Sistema de autenticación para empleados de PyLink
Solo login - Sin registro (las credenciales las asigna el admin)
"""

import reflex as rx
from ..styles import *
from ..database import login_empleado


class EmployeeAuthState(rx.State):
    """Estado de autenticación para empleados."""
    
    # Campos del formulario
    email: str = ""
    password: str = ""
    
    # Estado de autenticación
    is_authenticated: bool = False
    is_admin: bool = False
    
    # Datos del empleado autenticado
    employee_name: str = ""
    employee_role: str = ""
    employee_id: str = ""
    
    # Mensajes de error
    error_message: str = ""
    show_error: bool = False
    
    def set_email(self, email: str):
        """Actualizar email."""
        self.email = email.lower().strip()
        self.show_error = False
    
    def set_password(self, password: str):
        """Actualizar contraseña."""
        self.password = password
        self.show_error = False
    
    def login(self):
        """Procesar login de empleado usando Supabase."""
        # Validar que los campos no estén vacíos
        if not self.email or not self.password:
            self.error_message = "Por favor, ingresa email y contraseña"
            self.show_error = True
            return
        
        # Intentar autenticar con Supabase
        empleado = login_empleado(self.email, self.password)
        
        if empleado:
            # Login exitoso
            self.is_authenticated = True
            self.employee_name = f"{empleado['nombre']} {empleado.get('apellidos', '')}"
            self.employee_role = empleado['rol']
            self.employee_id = empleado['id']
            self.is_admin = (empleado['rol'] == 'admin')
            
            # Limpiar campos
            self.password = ""
            self.error_message = ""
            self.show_error = False
            
            # Redirigir según el rol
            if empleado['rol'] == 'admin':
                print(f"✅ Admin detectado: {empleado['nombre']}, redirigiendo a /admin")
                return rx.redirect("/admin")
            else:
                print(f"✅ Empleado detectado: {empleado['nombre']}, redirigiendo a /empleados/dashboard")
                return rx.redirect("/empleados/dashboard")
        else:
            self.error_message = "Email o contraseña incorrectos"
            self.show_error = True
    
    def logout(self):
        """Cerrar sesión."""
        self.is_authenticated = False
        self.is_admin = False
        self.employee_name = ""
        self.employee_role = ""
        self.employee_id = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.show_error = False
        return rx.redirect("/empleados")


def employee_login_page() -> rx.Component:
    """Página de login para empleados - estilo landing oscuro."""
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
                    
                    # Formulario moderno oscuro
                    rx.vstack(
                        rx.vstack(
                            rx.text("Correo Electrónico:", color="rgba(255, 255, 255, 0.9)", font_weight="600", font_size="0.9rem"),
                            rx.input(
                                placeholder="tu.email@pylink.com",
                                type="email",
                                value=EmployeeAuthState.email,
                                on_change=EmployeeAuthState.set_email,
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
                                value=EmployeeAuthState.password,
                                on_change=EmployeeAuthState.set_password,
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
                            EmployeeAuthState.show_error,
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="triangle_alert", color="#EF4444"),
                                    rx.text(EmployeeAuthState.error_message, color="white", font_weight="600"),
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
                            on_click=EmployeeAuthState.login,
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
        width="100%",
        min_height="100vh",
    )
