"""
Componente Hero Section super llamativo para PyLink
"""

import reflex as rx
from ..styles import COLORS


def floating_element(icon: str, delay: str = "0s") -> rx.Component:
    """Elemento flotante con animación 3D."""
    return rx.box(
        rx.text(icon, font_size="3rem"),
        position="absolute",
        animation=f"float 6s ease-in-out infinite {delay}",
        opacity="0.7",
        z_index="1",
    )


def hero_section() -> rx.Component:
    """Hero section súper llamativo y limpio."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal con efecto neón - responsive
                rx.box(
                    rx.heading(
                        "Tu Web",
                        size="6",
                        font_weight=["700", "800", "900", "900"],
                        color="white",
                        text_shadow="0 0 30px rgba(59, 130, 246, 0.8)",
                        margin_bottom="0.5rem",
                        line_height="1.2",
                        font_size=["2rem", "2.5rem", "4rem", "4.5rem"],
                    ),
                    rx.heading(
                        "Perfecta",
                        size="6", 
                        font_weight=["700", "800", "900", "900"],
                        background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff, #ff00ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        animation="glow 2s ease-in-out infinite alternate",
                        line_height="1.2",
                        padding_bottom="0.3rem",
                        font_size=["2rem", "2.5rem", "4rem", "4.5rem"],
                    ),
                    text_align="center",
                    margin_bottom="2rem",
                    width="100%",
                ),
                
                # Subtítulo responsive
                rx.text(
                    "Somos PyLink, una empresa joven y ambiciosa especializada en desarrollo de software. "
                    "Transformamos ideas en soluciones digitales que impulsan el crecimiento de tu empresa.",
                    font_size=["1rem", "1.1rem", "1.2rem", "1.3rem"],  # Responsive
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    max_width="700px",
                    line_height="1.6",
                    margin_bottom="3rem",
                    padding_x="1.5rem",  # Padding para móvil
                ),
                
                # Botón principal
                rx.link(
                    rx.button(
                        rx.hstack( 
                            rx.icon(tag="rocket", margin_right="8px"),
                            rx.text("Iniciar Proyecto"),
                            align_items="center",
                        ),
                        background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                        color="white",
                        font_weight="700",
                        padding="20px 40px",  # Aumentado para mejor táctil en móvil
                        border_radius="50px",
                        font_size="1.2rem",
                        border="none",
                        box_shadow="0 10px 30px rgba(59, 130, 246, 0.5)",
                        transition="all 0.3s ease",
                        min_height="56px",  # Altura mínima para accesibilidad táctil
                        _hover={
                            "transform": "translateY(-5px) scale(1.05)",
                            "box_shadow": "0 20px 40px rgba(59, 130, 246, 0.7)",
                        },
                    ),
                    href="#contact",
                ),
                
                align_items="center",
                spacing="6",
                text_align="center",
                padding_top="8rem",  # Espacio para navbar fixed
            ),
            max_width="1200px",
            margin="0 auto",
            padding=["0 0.5rem", "0 1rem", "0 1.5rem", "0 2rem"],  # Responsive padding
        ),
        
        id="home",
        min_height="100vh",
        display="flex",
        align_items="center",
        position="relative",
        overflow="hidden",
        # Background épico con gradientes y partículas
        background=f"""
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)
        """,
        
        # CSS personalizado para animaciones
        style={
            "@keyframes float": {
                "0%, 100%": {"transform": "translateY(0px)"},
                "50%": {"transform": "translateY(-20px)"},
            },
            "@keyframes glow": {
                "0%": {"text-shadow": "0 0 20px rgba(59, 130, 246, 0.5)"},
                "100%": {"text-shadow": "0 0 40px rgba(59, 130, 246, 1)"},
            },
        },
    )
