"""
PyEnterprise - Aplicación Principal
Página web empresarial desarrollada con Reflex
"""

import reflex as rx
from frontend.components.navbar import navbar
from frontend.components.hero import hero_section
from frontend.components.about import about_section
from frontend.components.services import services_section
from frontend.components.contact import contact_section
from frontend.components.footer import footer
from shared.styles import base_style


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


# Configuración de la aplicación
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Añadir páginas
app.add_page(index, route="/", title="PyEnterprise - Soluciones Empresariales con Python")

# La aplicación está lista para ejecutarse
