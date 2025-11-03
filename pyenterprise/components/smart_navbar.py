"""
Navbar inteligente que se adapta según el estado de autenticación
"""

import reflex as rx
from ..styles import COLORS
from .employee_auth import EmployeeAuthState
from shared.nav_utils import (
    public_nav_items,
    employee_nav_items,
    user_menu,
    mobile_menu_button
)


def smart_navbar() -> rx.Component:
    """Navbar que cambia según el estado de autenticación."""
    return rx.box(
        rx.container(
            rx.hstack(
                # Logo y nombre
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/logopylink.png",
                            alt="PyLink Logo",
                            width="40px",
                            height="40px",
                            object_fit="contain",
                        ),
                        width="40px",
                        height="40px",
                        border_radius="50%",
                        padding="4px",
                        background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                        box_shadow="0 0 20px rgba(94, 234, 212, 0.4)",
                        transition="all 0.4s ease",
                        _hover={
                            "transform": "scale(1.1) rotate(5deg)",
                            "box_shadow": "0 0 30px rgba(94, 234, 212, 0.6)",
                        },
                    ),
                    rx.heading(
                        "PyLink",
                        size="5",
                        color=COLORS["primary"],
                        font_weight="800",
                        background=f"linear-gradient(45deg, #5EEAD4, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        font_size=["1.2rem", "1.2rem", "1.5rem", "1.5rem"],
                    ),
                    align_items="center",
                    spacing="2",
                ),

                # Spacer
                rx.spacer(),

                # Navegación condicional
                rx.cond(
                    EmployeeAuthState.is_authenticated,
                    # Navegación para usuarios autenticados
                    rx.hstack(
                        employee_nav_items(),
                        user_menu(),
                        align_items="center",
                        spacing="4",
                    ),
                    # Navegación para público general
                    rx.hstack(
                        public_nav_items(),
                        align_items="center",
                        spacing="4",
                    )
                ),

                # Menú móvil
                mobile_menu_button(),

                align_items="center",
                justify="space-between",
                width="100%",
            ),
            max_width="1200px",
            padding_x="20px",
        ),
        background_color="rgba(26, 26, 46, 0.95)",
        backdrop_filter="blur(20px)",
        border_bottom=f"1px solid {COLORS['border']}",
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="1000",
        padding="16px 0",
        width="100%",
    )


def public_navbar() -> rx.Component:
    """Navbar para páginas públicas (sin autenticación)."""
    return rx.box(
        rx.container(
            rx.hstack(
                # Logo
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/logopylink.png",
                            alt="PyLink Logo",
                            width="40px",
                            height="40px",
                            object_fit="contain",
                        ),
                        width="40px",
                        height="40px",
                        border_radius="50%",
                        padding="4px",
                        background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                    ),
                    rx.heading(
                        "PyLink",
                        size="5",
                        color=COLORS["primary"],
                        font_weight="800",
                        background=f"linear-gradient(45deg, #5EEAD4, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                    ),
                    align_items="center",
                    spacing="2",
                ),

                # Spacer
                rx.spacer(),

                # Navegación pública
                public_nav_items(),

                # Contacto
                rx.hstack(
                    rx.link(
                        rx.box(
                            rx.html('<i class="fas fa-envelope"></i>'),
                            background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                            padding="12px",
                            border_radius="50%",
                            color="white",
                        ),
                        href="mailto:hola@pylink.dev",
                    ),
                    rx.link(
                        rx.box(
                            rx.html('<i class="fab fa-whatsapp"></i>'),
                            background="linear-gradient(45deg, #25D366, #128C7E)",
                            padding="12px",
                            border_radius="50%",
                            color="white",
                        ),
                        href="https://wa.me/34900123456",
                        is_external=True,
                    ),
                    spacing="3",
                ),

                # Menú móvil
                mobile_menu_button(),

                align_items="center",
                justify="space-between",
                width="100%",
            ),
            max_width="1200px",
            padding_x="20px",
        ),
        background_color="rgba(26, 26, 46, 0.95)",
        backdrop_filter="blur(20px)",
        border_bottom=f"1px solid {COLORS['border']}",
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="1000",
        padding="16px 0",
        width="100%",
    )