"""
Sistema de autenticación para empleados de PyLink
Solo login - Sin registro (las credenciales las asigna el admin)
"""

import reflex as rx
from ..styles import *

# Datos de empleados de prueba (en producción vendrían de base de datos)
EMPLEADOS_DB = {
    "juan@pylink.com": {
        "password": "emp123",
        "nombre": "Juan Pérez",
        "rol": "Desarrollador Frontend",
        "id": "EMP001"
    },
    "maria@pylink.com": {
        "password": "emp123",
        "nombre": "María García",
        "rol": "Diseñadora UX/UI",
        "id": "EMP002"
    },
    "admin@pylink.com": {
        "password": "admin123",
        "nombre": "Administrador",
        "rol": "Administrador del Sistema",
        "id": "ADMIN001"
    }
}


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
        """Procesar login de empleado."""
        # Validar que los campos no estén vacíos
        if not self.email or not self.password:
            self.error_message = "Por favor, ingresa email y contraseña"
            self.show_error = True
            return
        
        # Verificar credenciales
        if self.email in EMPLEADOS_DB:
            empleado = EMPLEADOS_DB[self.email]
            if empleado["password"] == self.password:
                # Login exitoso
                self.is_authenticated = True
                self.employee_name = empleado["nombre"]
                self.employee_role = empleado["rol"]
                self.employee_id = empleado["id"]
                self.is_admin = (self.email == "admin@pylink.com")
                
                # Limpiar campos
                self.password = ""
                self.error_message = ""
                self.show_error = False
                
                # Redirigir al dashboard
                return rx.redirect("/empleados/dashboard")
            else:
                self.error_message = "Contraseña incorrecta"
                self.show_error = True
        else:
            self.error_message = "Email no registrado. Contacta al administrador."
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
    """Página de login para empleados - versión minimalista."""
    return rx.fragment(
        rx.heading("PyLink - Login Empleados"),
        rx.text("Correo Electrónico:"),
        rx.input(
            placeholder="tu.email@pylink.com",
            value=EmployeeAuthState.email,
            on_change=EmployeeAuthState.set_email,
        ),
        rx.text("Contraseña:"),
        rx.input(
            placeholder="contraseña",
            type="password",
            value=EmployeeAuthState.password,
            on_change=EmployeeAuthState.set_password,
        ),
        rx.text(EmployeeAuthState.error_message, color="red"),
        rx.button(
            "Iniciar Sesión",
            on_click=EmployeeAuthState.login,
        ),
        rx.text("Usuarios: juan@pylink.com / emp123"),
        rx.text("Admin: admin@pylink.com / admin123"),
    )
