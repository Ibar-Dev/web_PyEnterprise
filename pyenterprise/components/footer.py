"""
Componente Footer moderno para PyLink
"""

import reflex as rx
from ..styles import COLORS


def footer() -> rx.Component:
    """Footer moderno con efectos glassmorphism."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Logo y descripción
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        alt="PyLink Logo",
                        width="32px",
                        height="32px",
                    ),
                    rx.heading(
                        "PyLink",
                        size="5",
                        color="white",
                        font_weight="800",
                    ),
                    align_items="center",
                    spacing="2",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Conectando tu negocio con el futuro digital",
                    color="rgba(255, 255, 255, 0.7)",
                    text_align="center",
                    margin_bottom="2rem",
                ),
                
                # Enlaces rápidos
                rx.hstack(
                    rx.link("Inicio", href="#home", color="rgba(255, 255, 255, 0.8)", _hover={"color": COLORS["primary"]}),
                    rx.link("Nosotros", href="#about", color="rgba(255, 255, 255, 0.8)", _hover={"color": COLORS["primary"]}),
                    rx.link("Equipo", href="#team", color="rgba(255, 255, 255, 0.8)", _hover={"color": COLORS["primary"]}),
                    rx.link("Empleados", href="/empleados", color="rgba(255, 255, 255, 0.8)", _hover={"color": COLORS["primary"]}),
                    spacing="6",
                    justify_content="center",
                    margin_bottom="2rem",
                ),
                
                # Copyright
                rx.text(
                    f"© 2025 PyLink. Construyendo el futuro, un proyecto a la vez.",
                    color="rgba(255, 255, 255, 0.5)",
                    font_size="0.9rem",
                    text_align="center",
                ),
                
                align_items="center",
                spacing="4",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="3rem 2rem",
        ),
        background="rgba(30, 41, 59, 0.95)",
        backdrop_filter="blur(10px)",
        border_top="1px solid rgba(255, 255, 255, 0.1)",
    )
