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
                            width="40px",
                            height="40px",
                            object_fit="contain",  # Mantiene proporción
                        ),
                        width="40px",  # Contenedor del mismo tamaño
                        height="40px",
                        border_radius="50%",
                        padding="4px",
                        background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                        box_shadow="0 0 20px rgba(94, 234, 212, 0.4), 0 0 40px rgba(59, 130, 246, 0.2)",
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",  # No se comprime
                        _hover={
                            "transform": "scale(1.1) rotate(5deg)",
                            "box_shadow": "0 0 30px rgba(94, 234, 212, 0.6), 0 0 60px rgba(59, 130, 246, 0.4)",
                        },
                    ),
                    rx.heading(
                        "PyLink",
                        size="5",  # Reducido para móvil
                        color=COLORS["primary"],
                        font_weight="800",
                        background=f"linear-gradient(45deg, #5EEAD4, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        white_space="nowrap",  # No se rompe
                    ),
                    align_items="center",
                    spacing="2",
                    flex_shrink="0",  # Logo y título no se comprimen
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
                
                # Iconos de contacto
                rx.hstack(
                    # WhatsApp
                    rx.link(
                        rx.box(
                            rx.html('<i class="fab fa-whatsapp"></i>'),
                            background="linear-gradient(45deg, #25D366, #128C7E)",
                            padding="12px",
                            border_radius="50%",
                            box_shadow="0 0 20px rgba(37, 211, 102, 0.5)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-3px) scale(1.1) rotate(5deg)",
                                "box_shadow": "0 10px 30px rgba(37, 211, 102, 0.8)",
                            },
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="48px",
                            height="48px",
                            font_size="24px",
                            color="white",
                        ),
                        href="https://wa.me/34900123456?text=Hola,%20me%20interesa%20conocer%20más%20sobre%20sus%20servicios",
                        is_external=True,
                    ),
                    
                    # Email
                    rx.link(
                        rx.box(
                            rx.html('<i class="fas fa-envelope"></i>'),
                            background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                            padding="12px",
                            border_radius="50%",
                            box_shadow="0 0 20px rgba(59, 130, 246, 0.5)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-3px) scale(1.1) rotate(5deg)",
                                "box_shadow": "0 10px 30px rgba(59, 130, 246, 0.8)",
                            },
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="48px",
                            height="48px",
                            font_size="20px",
                            color="white",
                        ),
                        href="mailto:hola@pylink.dev?subject=Consulta%20desde%20la%20web",
                    ),
                    
                    # Teléfono
                    rx.link(
                        rx.box(
                            rx.html('<i class="fas fa-phone"></i>'),
                            background="linear-gradient(45deg, #FF6B6B, #EE5A6F)",
                            padding="12px",
                            border_radius="50%",
                            box_shadow="0 0 20px rgba(255, 107, 107, 0.5)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-3px) scale(1.1) rotate(5deg)",
                                "box_shadow": "0 10px 30px rgba(255, 107, 107, 0.8)",
                            },
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="48px",
                            height="48px",
                            font_size="20px",
                            color="white",
                        ),
                        href="tel:+34900123456",
                    ),
                    
                    spacing="3",
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
        padding=["0.75rem 0", "0.75rem 0", "1rem 0", "1rem 0"],  # Menos padding en móvil
    )
