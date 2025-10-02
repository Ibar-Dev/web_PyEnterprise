"""
PyLink - Página web empresarial desarrollada con Reflex
Empresa de desarrollo de software con enfoque moderno y tecnológico
"""

import reflex as rx
from .styles import *
from .components.navbar import navbar
from .components.hero import hero_section
from .components.about import about_section
from .components.team import team_section
from .components.contact import contact_section
from .components.footer import footer
from .components.employee_auth import employee_login_page, EmployeeAuthState




def index() -> rx.Component:
    """Página principal llamativa de PyLink."""
    return rx.box(
        navbar(),
        hero_section(), 
        about_section(),
        team_section(),
        contact_section(),
        footer(),
        width="100%",
        margin="0",
        padding="0",
        # Efectos de background
        background=f"""
            linear-gradient(135deg, {COLORS['background']} 0%, {COLORS['surface']} 100%),
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%)
        """,
        background_attachment="fixed",
    )


def empleados_login() -> rx.Component:
    """Página de login para empleados."""
    return employee_login_page()


def empleados_dashboard() -> rx.Component:
    """Dashboard de empleados - requiere autenticación."""
    return rx.cond(
        EmployeeAuthState.is_authenticated,
        rx.box(
            rx.heading("Dashboard - En desarrollo", size="5"),
            rx.text(EmployeeAuthState.employee_name),
            rx.text(EmployeeAuthState.employee_role),
            rx.text(EmployeeAuthState.employee_id),
            rx.button(
                "Cerrar Sesión",
                on_click=EmployeeAuthState.logout,
                background="red",
                color="white",
            ),
            padding="2rem",
        ),
        rx.box(
            rx.heading("Acceso Denegado"),
            rx.text("Por favor inicia sesión"),
        )
    )



# Configuración de la aplicación
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "/cards.css"  # CSS personalizado para las tarjetas
    ]
)

# Rutas de la aplicación
app.add_page(index, route="/", title="PyLink - Conectando tu negocio con el futuro digital")
app.add_page(empleados_login, route="/empleados", title="PyLink - Login Empleados")
app.add_page(empleados_dashboard, route="/empleados/dashboard", title="PyLink - Dashboard")

# La aplicación está lista para ejecutarse
