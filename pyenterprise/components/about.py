"""
Componente About Section para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def about_section() -> rx.Component:
    """Sección sobre nosotros - Por implementar."""
    return rx.box(
        rx.text(
            "Sección About - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="2rem",
        ),
        id="nosotros",
    )
