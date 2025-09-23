"""
PyEnterprise - Página web empresarial desarrollada con Reflex
"""

import reflex as rx
from .styles import *


def index() -> rx.Component:
    """Página principal simple de PyEnterprise."""
    return rx.center(
        rx.vstack(
            # Logo
            rx.image(
                src="/logo.png",
                alt="PyEnterprise Logo",
                width="120px",
                height="120px",
                margin_bottom="2rem",
            ),
            
            # Nombre de la empresa
            rx.heading(
                "PyEnterprise",
                size="9",  # Título grande
                color=COLORS["primary"],
                font_weight="800",
                margin_bottom="1rem",
            ),
            
            # Tagline simple
            rx.text(
                "Soluciones Empresariales con Python",
                font_size="1.5rem",
                color=COLORS["text_light"],
                text_align="center",
                margin_bottom="2rem",
            ),
            
            # Botón simple
            rx.button(
                "Próximamente",
                background_color=COLORS["primary"],
                color="white",
                font_weight="600",
                padding="16px 32px",
                border_radius="10px",
                font_size="1.1rem",
                _hover={
                    "background_color": COLORS["secondary"],
                    "transform": "translateY(-2px)",
                },
                transition="all 0.3s ease",
            ),
            
            align_items="center",
            spacing="4",
            text_align="center",
        ),
        height="100vh",
        width="100%",
        background=f"linear-gradient(135deg, {COLORS['background']} 0%, {COLORS['surface']} 100%)",
    )


# Configuración de la aplicación
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)
app.add_page(index, route="/", title="PyEnterprise - Soluciones Empresariales con Python")

# La aplicación está lista para ejecutarse
