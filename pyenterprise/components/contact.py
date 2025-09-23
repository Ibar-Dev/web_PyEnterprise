"""
Componente Contact Section para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def contact_section() -> rx.Component:
    """Sección de contacto - Por implementar."""
    return rx.box(
        rx.text(
            "Sección Contact - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="2rem",
        ),
        id="contacto",
    )
