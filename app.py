"""
PyEnterprise - Aplicación Principal
Página web empresarial desarrollada con Reflex
"""

import reflex as rx
from pyenterprise.components.navbar import navbar
from pyenterprise.components.hero import hero_section
from pyenterprise.components.about import about_section
from pyenterprise.components.services import services_section
from pyenterprise.components.contact import contact_section
from pyenterprise.components.footer import footer
from pyenterprise.components.employee_auth import employee_login_page
from pyenterprise.components.employee_dashboard_integrated import employee_dashboard
from pyenterprise.components.admin_panel_profesional import admin_panel
from shared.styles import base_style
from shared.constants import ROUTES


def index() -> rx.Component:
    """Página principal de PyEnterprise."""
    return rx.box(
        navbar(),
        hero_section(),
        about_section(),
        services_section(),
        contact_section(),
        footer(),
        width="100%",
        margin="0",
        padding="0",
    )


def empleados() -> rx.Component:
    """Página de login para empleados."""
    return rx.box(
        employee_login_page(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


def empleado_dashboard() -> rx.Component:
    """Dashboard del empleado."""
    return rx.box(
        navbar(),
        employee_dashboard(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


def admin() -> rx.Component:
    """Panel de administración."""
    return rx.box(
        navbar(),
        admin_panel(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


def servicios() -> rx.Component:
    """Página de servicios."""
    return rx.box(
        navbar(),
        services_section(),
        footer(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


def about() -> rx.Component:
    """Página sobre nosotros."""
    return rx.box(
        navbar(),
        about_section(),
        footer(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


def contacto() -> rx.Component:
    """Página de contacto."""
    return rx.box(
        navbar(),
        contact_section(),
        footer(),
        width="100%",
        min_height="100vh",
        style=base_style,
    )


# Configuración de la aplicación
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Añadir páginas
app.add_page(index, route=ROUTES["home"], title="PyEnterprise - Soluciones Empresariales con Python")
app.add_page(empleados, route=ROUTES["empleados"], title="Portal de Empleados - PyEnterprise")
app.add_page(empleado_dashboard, route=ROUTES["empleado_dashboard"], title="Dashboard Empleado - PyEnterprise")
app.add_page(admin, route=ROUTES["admin"], title="Panel de Administración - PyEnterprise")
app.add_page(servicios, route=ROUTES["services"], title="Servicios - PyEnterprise")
app.add_page(about, route=ROUTES["about"], title="Sobre Nosotros - PyEnterprise")
app.add_page(contacto, route=ROUTES["contact"], title="Contacto - PyEnterprise")

print("PyEnterprise aplicación configurada con ruteo completo")
print("Rutas disponibles:")
for route_name, route_path in ROUTES.items():
    print(f"   - {route_name}: {route_path}")

# La aplicación está lista para ejecutarse
