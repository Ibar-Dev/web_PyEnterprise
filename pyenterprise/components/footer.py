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
                    rx.box(
                        rx.image(
                            src="/logopylink.png",
                            alt="PyLink Logo",
                            width="40px",
                            height="40px",
                        ),
                        border_radius="50%",
                        padding="3px",
                        background="linear-gradient(135deg, rgba(94, 234, 212, 0.3), rgba(59, 130, 246, 0.3))",
                        box_shadow="0 0 15px rgba(94, 234, 212, 0.5), 0 0 30px rgba(59, 130, 246, 0.3)",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "scale(1.15) rotate(-5deg)",
                            "box_shadow": "0 0 25px rgba(94, 234, 212, 0.7), 0 0 50px rgba(59, 130, 246, 0.5)",
                        },
                    ),
                    rx.heading(
                        "PyLink",
                        size="5",
                        color="white",
                        font_weight="800",
                        background="linear-gradient(45deg, #5EEAD4, #3B82F6, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                    ),
                    align_items="center",
                    spacing="3",
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
                    margin_bottom="1.5rem",
                    flex_wrap="wrap",
                ),
                
                # Enlaces legales
                rx.hstack(
                    rx.link("Privacidad", href="/privacidad", color="rgba(255, 255, 255, 0.6)", font_size="0.85rem", _hover={"color": COLORS["primary"]}),
                    rx.text("|", color="rgba(255, 255, 255, 0.3)"),
                    rx.link("Cookies", href="/cookies", color="rgba(255, 255, 255, 0.6)", font_size="0.85rem", _hover={"color": COLORS["primary"]}),
                    rx.text("|", color="rgba(255, 255, 255, 0.3)"),
                    rx.link("Términos", href="/terminos", color="rgba(255, 255, 255, 0.6)", font_size="0.85rem", _hover={"color": COLORS["primary"]}),
                    spacing="3",
                    justify_content="center",
                    margin_bottom="1.5rem",
                ),
                
                # Copyright
                rx.vstack(
                    rx.text(
                        f"© 2025 PyLink. Construyendo el futuro, un proyecto a la vez.",
                        color="rgba(255, 255, 255, 0.5)",
                        font_size="0.9rem",
                        text_align="center",
                    ),
                    rx.text(
                        "🔒 Sitio seguro con SSL/TLS | GDPR Compliance",
                        color="rgba(94, 234, 212, 0.5)",
                        font_size="0.8rem",
                        text_align="center",
                    ),
                    spacing="1",
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
