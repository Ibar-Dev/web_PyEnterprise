"""
Componente Hero Section para PyEnterprise
"""

import reflex as rx
from shared.styles import hero_style, container_style, button_primary_style, button_secondary_style, COLORS


def hero_section() -> rx.Component:
    """Sección hero principal con título, descripción y CTAs."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal
                rx.heading(
                    "Soluciones Empresariales ",
                    rx.text(
                        "con Python",
                        color="#60a5fa",  # Azul más claro para contraste
                        as_="span",
                    ),
                    size="2xl",
                    font_weight="800",
                    text_align="center",
                    line_height="1.1",
                    margin_bottom="1.5rem",
                ),
                
                # Subtítulo/descripción
                rx.text(
                    "Transformamos tu negocio con tecnología Python avanzada. "
                    "Desarrollo web, automatización, análisis de datos y soluciones "
                    "personalizadas para impulsar tu empresa al siguiente nivel.",
                    font_size="1.25rem",
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    max_width="600px",
                    margin_bottom="2.5rem",
                    line_height="1.6",
                ),
                
                # Botones de acción
                rx.hstack(
                    rx.button(
                        "Comenzar Proyecto",
                        background_color="white",
                        color=COLORS["primary"],
                        font_weight="600",
                        padding="16px 32px",
                        border_radius="10px",
                        font_size="1.1rem",
                        _hover={
                            "transform": "translateY(-3px)",
                            "box_shadow": "0 10px 25px rgba(255, 255, 255, 0.3)",
                        },
                        transition="all 0.3s ease",
                    ),
                    rx.button(
                        rx.icon(tag="play", margin_right="8px"),
                        "Ver Demo",
                        background_color="transparent",
                        color="white",
                        border="2px solid rgba(255, 255, 255, 0.8)",
                        font_weight="600",
                        padding="16px 32px",
                        border_radius="10px",
                        font_size="1.1rem",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.1)",
                            "border_color": "white",
                            "transform": "translateY(-3px)",
                        },
                        transition="all 0.3s ease",
                    ),
                    spacing="4",
                    wrap="wrap",
                    justify_content="center",
                ),
                
                # Estadísticas o badges
                rx.hstack(
                    rx.vstack(
                        rx.text("100+", font_size="2rem", font_weight="700"),
                        rx.text("Proyectos", font_size="0.9rem", opacity="0.8"),
                        align_items="center",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("50+", font_size="2rem", font_weight="700"),
                        rx.text("Clientes", font_size="0.9rem", opacity="0.8"),
                        align_items="center",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("5+", font_size="2rem", font_weight="700"),
                        rx.text("Años", font_size="0.9rem", opacity="0.8"),
                        align_items="center",
                        spacing="1",
                    ),
                    spacing="8",
                    margin_top="3rem",
                    justify_content="center",
                ),
                
                align_items="center",
                spacing="4",
                text_align="center",
            ),
            **container_style,
        ),
        id="inicio",
        **hero_style,
    )
