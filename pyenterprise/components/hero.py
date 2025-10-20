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


def service_card(icon: str, title: str, gradient: str, image_url: str) -> rx.Component:
    """Card de servicio con imagen de fondo y texto superpuesto."""
    return rx.box(
        # Card interno con imagen
        rx.box(
            # Overlay oscuro para legibilidad
            rx.box(
                position="absolute",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.7) 100%)",
                border_radius="17px",
            ),
            # Contenido
            rx.vstack(
                rx.icon(
                    tag=icon,
                    size=40,
                    color="white",
                    filter="drop-shadow(0 2px 8px rgba(0,0,0,0.5))",
                ),
                rx.text(
                    title,
                    color="white",
                    font_weight="700",
                    font_size=["1rem", "1.1rem", "1.2rem", "1.2rem"],
                    text_align="center",
                    text_shadow="0 2px 10px rgba(0,0,0,0.8)",
                    z_index="2",
                ),
                align_items="center",
                justify_content="center",
                spacing="3",
                height="100%",
                z_index="1",
                position="relative",
            ),
            # Imagen de fondo
            background_image=f"url('{image_url}')",
            background_size="cover",
            background_position="center",
            background_repeat="no-repeat",
            border_radius="17px",
            height="100%",
            width="100%",
            position="relative",
            overflow="hidden",
        ),
        # Wrapper con borde gradiente
        background=gradient,
        border_radius="20px",
        padding="3px",
        height=["180px", "200px", "220px", "220px"],
        box_shadow="0 8px 25px rgba(0, 0, 0, 0.5)",
        transition="all 0.4s ease",
        _hover={
            "transform": "translateY(-8px) scale(1.02)",
            "box_shadow": "0 15px 40px rgba(59, 130, 246, 0.6)",
        },
        cursor="pointer",
    )


def hero_section() -> rx.Component:
    """Hero section súper llamativo con servicios visuales."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal con efecto neón - responsive
                rx.box(
                    rx.heading(
                        "Soluciones Digitales",
                        size="6",
                        font_weight=["700", "800", "900", "900"],
                        color="white",
                        text_shadow="0 0 30px rgba(59, 130, 246, 0.8)",
                        margin_bottom="0.5rem",
                        line_height="1.2",
                        padding_bottom="0.3rem",
                        font_size=["2rem", "2.5rem", "3rem", "3.5rem"],
                    ),
                    rx.heading(
                        "que Impulsan tu Negocio",
                        size="6", 
                        font_weight=["700", "800", "900", "900"],
                        background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff, #ff00ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        animation="glow 2s ease-in-out infinite alternate",
                        line_height="1.2",
                        padding_bottom="0.5rem",
                        font_size=["2rem", "2.5rem", "3rem", "3.5rem"],
                    ),
                    text_align="center",
                    margin_bottom="1.5rem",
                    width="100%",
                    padding_x="1rem",
                ),
                
                # Subtítulo responsive
                rx.text(
                    "Somos PyLink, tu partner tecnológico integral. Desde desarrollo web hasta inteligencia artificial.",
                    font_size=["1rem", "1.1rem", "1.2rem", "1.2rem"],
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    max_width="700px",
                    line_height="1.6",
                    margin_bottom="2.5rem",
                    padding_x="1.5rem",
                ),
                
                # Grid de servicios - Bento style
                rx.box(
                    service_card("globe", "Desarrollo Web", "linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.2))", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=300&fit=crop"),
                    service_card("cpu", "Automatización", "linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(126, 34, 206, 0.2))", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=300&fit=crop"),
                    service_card("bar-chart", "Análisis de Datos", "linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(22, 163, 74, 0.2))", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop"),
                    service_card("cloud", "Cloud & DevOps", "linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(29, 78, 216, 0.2))", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=300&fit=crop"),
                    service_card("lightbulb", "Consultoría IT", "linear-gradient(135deg, rgba(251, 146, 60, 0.3), rgba(249, 115, 22, 0.2))", "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop"),
                    service_card("smartphone", "Apps Móviles", "linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(219, 39, 119, 0.2))", "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300&fit=crop"),
                    display="grid",
                    grid_template_columns=["repeat(2, 1fr)", "repeat(2, 1fr)", "repeat(3, 1fr)", "repeat(3, 1fr)"],
                    gap=["1rem", "1.2rem", "1.5rem", "1.5rem"],
                    width="100%",
                    max_width="900px",
                    margin_bottom="3rem",
                    padding_x=["1rem", "1.5rem", "2rem", "2rem"],
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
                        padding="20px 40px",
                        border_radius="50px",
                        font_size="1.2rem",
                        border="none",
                        box_shadow="0 10px 30px rgba(59, 130, 246, 0.5)",
                        transition="all 0.3s ease",
                        min_height="48px",
                        _hover={
                            "transform": "translateY(-5px) scale(1.05)",
                            "box_shadow": "0 20px 40px rgba(59, 130, 246, 0.7)",
                        },
                    ),
                    href="/servicios",
                ),
                
                align_items="center",
                spacing="4",
                text_align="center",
                padding_top=["6rem", "7rem", "8rem", "8rem"],
                padding_bottom="3rem",
            ),
            max_width="100%",
            margin="0 auto",
            padding="0 2rem",
            width="100%",
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
