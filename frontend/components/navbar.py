"""
Componente Navbar para PyEnterprise
"""

import reflex as rx
from shared.styles import navbar_style, container_style, COLORS


def navbar() -> rx.Component:
    """Navbar principal con logo y menú de navegación."""
    return rx.box(
        rx.container(
            rx.hstack(
                # Logo y nombre de la empresa
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        alt="PyEnterprise Logo",
                        width="40px",
                        height="40px",
                    ),
                    rx.heading(
                        "PyEnterprise",
                        size="lg",
                        color=COLORS["primary"],
                        font_weight="700",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                
                # Menú de navegación
                rx.hstack(
                    rx.link(
                        "Inicio",
                        href="#inicio",
                        color=COLORS["text"],
                        font_weight="500",
                        _hover={
                            "color": COLORS["primary"],
                            "text_decoration": "none",
                        },
                    ),
                    rx.link(
                        "Nosotros",
                        href="#nosotros",
                        color=COLORS["text"],
                        font_weight="500",
                        _hover={
                            "color": COLORS["primary"],
                            "text_decoration": "none",
                        },
                    ),
                    rx.link(
                        "Servicios",
                        href="#servicios",
                        color=COLORS["text"],
                        font_weight="500",
                        _hover={
                            "color": COLORS["primary"],
                            "text_decoration": "none",
                        },
                    ),
                    rx.link(
                        "Contacto",
                        href="#contacto",
                        color=COLORS["text"],
                        font_weight="500",
                        _hover={
                            "color": COLORS["primary"],
                            "text_decoration": "none",
                        },
                    ),
                    spacing="8",
                    display=["none", "none", "flex", "flex"],  # Oculto en móvil
                ),
                
                # Botón CTA
                rx.button(
                    "Contáctanos",
                    background_color=COLORS["primary"],
                    color="white",
                    border_radius="8px",
                    padding="10px 20px",
                    font_weight="600",
                    _hover={
                        "background_color": COLORS["secondary"],
                        "transform": "translateY(-2px)",
                    },
                    transition="all 0.3s ease",
                ),
                
                # Menú hamburguesa para móvil
                rx.button(
                    rx.icon(tag="hamburger"),
                    display=["block", "block", "none", "none"],  # Solo visible en móvil
                    background="transparent",
                    border="none",
                    color=COLORS["primary"],
                    font_size="24px",
                    cursor="pointer",
                ),
                
                justify_content="space-between",
                align_items="center",
                width="100%",
            ),
            **container_style,
        ),
        **navbar_style,
    )
