"""
Componente Footer para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS


def footer() -> rx.Component:
    """Footer básico - Por implementar."""
    return rx.box(
        rx.text(
            "Footer - Por implementar",
            color=COLORS["text_light"],
            text_align="center",
            padding="2rem",
        ),
        background_color=COLORS["surface"],
        border_top=f"1px solid {COLORS['border']}",
    )
