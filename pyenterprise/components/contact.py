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
                    "¿Listo para comenzar?",
                    size="8",
                    color="white",
                    font_weight="800",
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Hablemos sobre tu próximo proyecto",
                    font_size="1.3rem",
                    color=COLORS["primary"],
                    text_align="center",
                    margin_bottom="4rem",
                ),
                
                # Información de contacto
                rx.grid(
                    # Email
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.icon(tag="email", size=40, color=COLORS["primary"]),
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
                        },
                    ),
                    
                    # Teléfono
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
                        },
                    ),
                    
                    columns="2",
                    spacing="6",
                    width="100%",
                    margin_bottom="4rem",
                ),
                
                # CTA Final
                rx.box(
                    rx.vstack(
                        rx.text(
                            "💡",
                            font_size="4rem",
                            margin_bottom="1rem",
                        ),
                        rx.heading(
                            "¿Tienes una idea?",
                            size="6",
                            color="white",
                            font_weight="700",
                            text_align="center",
                            margin_bottom="1rem",
                        ),
                        rx.text(
                            "No importa qué tan grande o pequeña sea, estamos aquí para hacerla realidad",
                            font_size="1.1rem",
                            color="rgba(255, 255, 255, 0.8)",
                            text_align="center",
                            margin_bottom="2rem",
                        ),
                        rx.button(
                            "Envíanos un WhatsApp",
                            background=f"linear-gradient(45deg, #25D366, #128C7E)",
                            color="white",
                            font_weight="700",
                            padding="16px 32px",
                            border_radius="50px",
                            font_size="1.1rem",
                            border="none",
                            box_shadow="0 10px 30px rgba(37, 211, 102, 0.5)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-3px) scale(1.05)",
                                "box_shadow": "0 20px 40px rgba(37, 211, 102, 0.7)",
                            },
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    background=f"linear-gradient(135deg, rgba(37, 211, 102, 0.1), rgba(18, 140, 126, 0.1))",
                    border="1px solid rgba(37, 211, 102, 0.3)",
                    border_radius="25px",
                    padding="3rem",
                    text_align="center",
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
