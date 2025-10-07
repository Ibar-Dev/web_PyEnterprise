"""
Componente Navbar moderno para PyLink
"""

import reflex as rx
from ..styles import COLORS


def navbar() -> rx.Component:
    """Navbar moderno con efectos glassmorphism."""
    return rx.box(
        rx.container(
            rx.hstack(
                # Logo y nombre con efecto glow
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/logopylink.png",
                            alt="PyLink Logo",
                            width="48px",
                            height="48px",
                        ),
                        border_radius="50%",
                        padding="4px",
                        background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                        box_shadow="0 0 20px rgba(94, 234, 212, 0.4), 0 0 40px rgba(59, 130, 246, 0.2)",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        _hover={
                            "transform": "scale(1.1) rotate(5deg)",
                            "box_shadow": "0 0 30px rgba(94, 234, 212, 0.6), 0 0 60px rgba(59, 130, 246, 0.4)",
                        },
                    ),
                    rx.heading(
                        "PyLink",
                        size="6",
                        color=COLORS["primary"],
                        font_weight="800",
                        background=f"linear-gradient(45deg, #5EEAD4, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                
                # Menú de navegación con botones 3D
                rx.hstack(
                    rx.box(
                        rx.link(
                            "Inicio",
                            href="#home",
                            class_name="nav-span",
                        ),
                        class_name="nav-button",
                    ),
                    rx.box(
                        rx.link(
                            "Nosotros",
                            href="#about",
                            class_name="nav-span",
                        ),
                        class_name="nav-button",
                    ),
                    rx.box(
                        rx.link(
                            "Equipo",
                            href="#team",
                            class_name="nav-span",
                        ),
                        class_name="nav-button",
                    ),
                    rx.box(
                        rx.link(
                            "Empleados",
                            href="/empleados",
                            class_name="nav-span",
                        ),
                        class_name="nav-button",
                    ),
                    spacing="3",
                    display=["none", "none", "flex", "flex"],
                ),
                
                # Botón CTA con efecto neón
                rx.button(
                    "Contáctanos",
                    background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                    color="white",
                    font_weight="600",
                    padding="12px 24px",
                    border_radius="25px",
                    border="none",
                    box_shadow="0 0 20px rgba(59, 130, 246, 0.5)",
                    transition="all 0.3s ease",
                    _hover={
                        "transform": "translateY(-3px) scale(1.05)",
                        "box_shadow": "0 10px 30px rgba(59, 130, 246, 0.7)",
                    },
                ),
                
                justify_content="space-between",
                align_items="center",
                width="100%",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="0 2rem",
        ),
        position="fixed",
        top="0",
        width="100%",
        z_index="1000",
        # Efecto glassmorphism
        background="rgba(255, 255, 255, 0.1)",
        backdrop_filter="blur(10px)",
        border_bottom="1px solid rgba(255, 255, 255, 0.2)",
        padding="1rem 0",
    )
