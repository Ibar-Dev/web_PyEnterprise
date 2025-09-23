"""
Componente Navbar para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def navbar() -> rx.Component:
    """Navbar básico - Por implementar."""
    return rx.box(
        rx.text(
            "Navbar - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="1rem",
        ),
        background_color=COLORS["surface"],
        border_bottom=f"1px solid {COLORS['border']}",
    )
