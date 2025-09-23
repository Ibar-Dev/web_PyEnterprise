"""
Componente Hero Section para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def hero_section() -> rx.Component:
    """Sección hero - Por implementar."""
    return rx.box(
        rx.text(
            "Sección Hero - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="2rem",
        ),
        id="inicio",
    )
