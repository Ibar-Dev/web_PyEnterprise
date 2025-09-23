"""
Componente Services Section para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def services_section() -> rx.Component:
    """Sección de servicios - Por implementar."""
    return rx.box(
        rx.text(
            "Sección Services - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="2rem",
        ),
        id="servicios",
    )
