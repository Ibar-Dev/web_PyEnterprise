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



# Configuración de la aplicación
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "/cards.css"  # CSS personalizado para las tarjetas
    ]
)

app.add_page(index, route="/", title="PyLink - Conectando tu negocio con el futuro digital")

# La aplicación está lista para ejecutarse
