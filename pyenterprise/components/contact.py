"""
Componente Contact Section para PyLink
"""

import reflex as rx
from ..styles import COLORS


def contact_section() -> rx.Component:
    """Sección de contacto moderna."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal
                rx.heading(
                    "Contacta con Nosotros",
                    size="8",
                    color="white",
                    font_weight="800",
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Estamos disponibles para atender tus consultas",
                    font_size="1.3rem",
                    color=COLORS["primary"],
                    text_align="center",
                    margin_bottom="4rem",
                ),
                
                # Información de contacto
                rx.grid(
                    # Email - clickable
                    rx.link(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon(tag="mail", size=40, color=COLORS["primary"]),
                                    padding="1.5rem",
                                    background=f"linear-gradient(135deg, {COLORS['primary']}, #00d4ff)",
                                    border_radius="20px",
                                    box_shadow="0 10px 30px rgba(59, 130, 246, 0.3)",
                                    margin_bottom="1.5rem",
                                ),
                                rx.heading(
                                    "Email",
                                    size="5",
                                    color="white",
                                    font_weight="700",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    "hola@pylink.dev",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_size="1.1rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Click para enviar email",
                                    color=COLORS["primary"],
                                    font_size="0.9rem",
                                    text_align="center",
                                    font_weight="600",
                                    margin_top="0.5rem",
                                ),
                                align_items="center",
                                spacing="3",
                            ),
                            background="rgba(255, 255, 255, 0.05)",
                            backdrop_filter="blur(10px)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="25px",
                            padding="2.5rem",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 20px 50px rgba(59, 130, 246, 0.2)",
                                "cursor": "pointer",
                            },
                        ),
                        href="mailto:hola@pylink.dev?subject=Consulta%20desde%20la%20web",
                        _hover={"text_decoration": "none"},
                    ),
                    
                    # Teléfono - clickable
                    rx.link(
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.icon(tag="phone", size=40, color=COLORS["primary"]),
                                    padding="1.5rem",
                                    background=f"linear-gradient(135deg, {COLORS['primary']}, #00d4ff)",
                                    border_radius="20px",
                                    box_shadow="0 10px 30px rgba(59, 130, 246, 0.3)",
                                    margin_bottom="1.5rem",
                                ),
                                rx.heading(
                                    "Teléfono",
                                    size="5",
                                    color="white",
                                    font_weight="700",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    "+34 900 123 456",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_size="1.1rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Click para llamar",
                                    color=COLORS["primary"],
                                    font_size="0.9rem",
                                    text_align="center",
                                    font_weight="600",
                                    margin_top="0.5rem",
                                ),
                                align_items="center",
                                spacing="3",
                            ),
                            background="rgba(255, 255, 255, 0.05)",
                            backdrop_filter="blur(10px)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="25px",
                            padding="2.5rem",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-10px)",
                                "box_shadow": "0 20px 50px rgba(59, 130, 246, 0.2)",
                                "cursor": "pointer",
                            },
                        ),
                        href="tel:+34900123456",
                        _hover={"text_decoration": "none"},
                    ),
                    
                    columns="2",
                    spacing="6",
                    width="100%",
                ),
                
                align_items="center",
                spacing="6",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="6rem 2rem",
        ),
        
        id="contact",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(37, 211, 102, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(18, 140, 126, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )
