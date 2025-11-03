"""
Utilidades de navegación para el sistema de menús contextuales
"""

import reflex as rx
from pyenterprise.components.employee_auth import EmployeeAuthState
from shared.constants import ROUTES


def public_nav_items() -> rx.Component:
    """Elementos de navegación para usuarios no autenticados."""
    return rx.hstack(
        rx.link(
            "Inicio",
            href=ROUTES["home"],
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Servicios",
            href=ROUTES["services"],
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Nosotros",
            href=ROUTES["about"],
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Contacto",
            href=ROUTES["contact"],
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Acceso Empleados",
            href=ROUTES["empleados"],
            color="white",
            background_color="rgba(94, 234, 212, 0.2)",
            font_weight="600",
            padding="8px 16px",
            border_radius="8px",
            border="1px solid rgba(94, 234, 212, 0.5)",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(94, 234, 212, 0.3)",
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 12px rgba(94, 234, 212, 0.3)"
            }
        ),
        spacing="4",
        display=["none", "none", "flex", "flex"],
    )


def employee_nav_items() -> rx.Component:
    """Elementos de navegación para empleados autenticados."""
    return rx.hstack(
        rx.link(
            "Dashboard",
            href=ROUTES["empleado_dashboard"],
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Mis Proyectos",
            href=ROUTES["empleado_dashboard"] + "#projects",
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        rx.link(
            "Mis Tareas",
            href=ROUTES["empleado_dashboard"] + "#tasks",
            color="white",
            font_weight="500",
            padding="8px 16px",
            border_radius="8px",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(255, 255, 255, 0.1)",
                "transform": "translateY(-2px)"
            }
        ),
        # Enlace a admin solo para administradores
        rx.cond(
            EmployeeAuthState.is_admin,
            rx.link(
                "Administración",
                href=ROUTES["admin"],
                color="white",
                background_color="rgba(239, 68, 68, 0.2)",
                font_weight="600",
                padding="8px 16px",
                border_radius="8px",
                border="1px solid rgba(239, 68, 68, 0.5)",
                transition="all 0.3s ease",
                _hover={
                    "background_color": "rgba(239, 68, 68, 0.3)",
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.3)"
                }
            )
        ),
        spacing="4",
        display=["none", "none", "flex", "flex"],
    )


def user_menu() -> rx.Component:
    """Menú de usuario con opciones de perfil y logout."""
    return rx.hstack(
        # Nombre del usuario
        rx.text(
            f"{EmployeeAuthState.employee_name} {EmployeeAuthState.employee_role}",
            color="white",
            font_weight="500",
            padding="8px 12px",
            background_color="rgba(255, 255, 255, 0.1)",
            border_radius="8px",
        ),

        # Botón de logout
        rx.button(
            rx.hstack(
                rx.icon("log_out", size=16),
                rx.text("Cerrar Sesión", font_weight="500"),
                spacing="2"
            ),
            background_color="rgba(239, 68, 68, 0.2)",
            color="white",
            border="1px solid rgba(239, 68, 68, 0.5)",
            border_radius="8px",
            padding="8px 16px",
            font_weight="500",
            cursor="pointer",
            transition="all 0.3s ease",
            _hover={
                "background_color": "rgba(239, 68, 68, 0.3)",
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.3)"
            },
            on_click=EmployeeAuthState.logout,
        ),
        spacing="3",
        align_items="center",
    )


def mobile_menu_button() -> rx.Component:
    """Botón de menú para dispositivos móviles."""
    return rx.button(
        rx.icon("menu", size=24),
        background_color="transparent",
        color="white",
        border="none",
        cursor="pointer",
        padding="8px",
        _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
        display=["flex", "flex", "none", "none"],
    )