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
    """Página de login para empleados con diseño moderno."""
    return rx.box(
        rx.center(
            rx.card(
                rx.vstack(
                    # Logo y título con efectos
                    rx.hstack(
                        rx.box(
                            rx.image(
                                src="/logopylink.png",
                                alt="PyLink Logo",
                                width="60px",
                                height="60px",
                            ),
                            border_radius="50%",
                            padding="6px",
                            background="linear-gradient(135deg, rgba(94, 234, 212, 0.3), rgba(59, 130, 246, 0.3))",
                            box_shadow="0 0 25px rgba(94, 234, 212, 0.6), 0 0 45px rgba(59, 130, 246, 0.4)",
                            transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        ),
                        rx.heading(
                            "PyLink",
                            size="8",
                            color=COLORS["primary"],
                            font_weight="800",
                            background=f"linear-gradient(45deg, #5EEAD4, {COLORS['primary']}, #00d4ff)",
                            background_clip="text",
                            _webkit_background_clip="text",
                            _webkit_text_fill_color="transparent",
                        ),
                        align="center",
                        spacing="4",
                        justify="center",
                        margin_bottom="2rem",
                    ),
                    
                    rx.heading(
                        "Acceso Empleados",
                        size="6",
                        text_align="center",
                        margin_bottom="2rem",
                        color=COLORS["text"],
                    ),
                    
                    # Formulario
                    rx.vstack(
                        rx.text("Correo Electrónico:", font_weight="600", color=COLORS["text"]),
                        rx.input(
                            placeholder="tu.email@pylink.com",
                            value=EmployeeAuthState.email,
                            on_change=EmployeeAuthState.set_email,
                            width="100%",
                            size="3",
                            border_color=COLORS["primary"],
                        ),
                        rx.text("Contraseña:", font_weight="600", color=COLORS["text"], margin_top="1rem"),
                        rx.input(
                            placeholder="••••••••",
                            type="password",
                            value=EmployeeAuthState.password,
                            on_change=EmployeeAuthState.set_password,
                            width="100%",
                            size="3",
                            border_color=COLORS["primary"],
                        ),
                        rx.cond(
                            EmployeeAuthState.show_error,
                            rx.text(
                                EmployeeAuthState.error_message, 
                                color="red",
                                font_weight="500",
                                margin_top="0.5rem"
                            ),
                        ),
                        rx.button(
                            "Iniciar Sesión",
                            on_click=EmployeeAuthState.login,
                            width="100%",
                            size="3",
                            margin_top="1.5rem",
                            background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                            color="white",
                            font_weight="600",
                            border_radius="12px",
                            box_shadow="0 4px 15px rgba(59, 130, 246, 0.3)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 20px rgba(59, 130, 246, 0.5)",
                            },
                            transition="all 0.3s ease",
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    
                    # Credenciales de prueba
                    rx.divider(margin_top="2rem", margin_bottom="1rem"),
                    rx.vstack(
                        rx.text("Credenciales de Prueba:", font_weight="600", font_size="0.9rem", color=COLORS["text"]),
                        rx.text("👤 Usuario: juan@pylink.com / emp123", font_size="0.85rem", color=COLORS["text_light"]),
                        rx.text("👑 Admin: admin@pylink.com / admin123", font_size="0.85rem", color=COLORS["text_light"]),
                        spacing="1",
                        align_items="center",
                    ),
                    
                    spacing="4",
                    align_items="stretch",
                    width="100%",
                ),
                padding="3rem",
                width="450px",
                box_shadow="0 10px 40px rgba(0, 0, 0, 0.1)",
            ),
            min_height="100vh",
            padding="2rem",
            background=f"""
                linear-gradient(135deg, {COLORS['background']} 0%, {COLORS['surface']} 100%),
                radial-gradient(circle at 20% 80%, rgba(94, 234, 212, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 50%)
            """,
        ),
        width="100%",
    )
