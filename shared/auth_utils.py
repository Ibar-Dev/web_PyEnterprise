"""
Utilidades de autenticación para proteger rutas
"""

import reflex as rx
from pyenterprise.components.employee_auth import EmployeeAuthState


def require_auth(component: rx.Component, fallback_route: str = "/empleados") -> rx.Component:
    """
    Protege un componente requiriendo autenticación.
    Si el usuario no está autenticado, redirige a la ruta de fallback.
    """
    return rx.cond(
        EmployeeAuthState.is_authenticated,
        component,
        rx.redirect(fallback_route)
    )


def require_admin(component: rx.Component, fallback_route: str = "/empleados") -> rx.Component:
    """
    Protege un componente requiriendo rol de administrador.
    Si el usuario no es admin, redirige a la ruta de fallback.
    """
    return rx.cond(
        EmployeeAuthState.is_admin,
        component,
        rx.redirect(fallback_route)
    )


def auth_guard(children: rx.Component) -> rx.Component:
    """
    Guardia de autenticación que muestra children solo si está autenticado.
    """
    return rx.cond(
        EmployeeAuthState.is_authenticated,
        children,
        rx.fragment()
    )


def admin_guard(children: rx.Component) -> rx.Component:
    """
    Guardia de administrador que muestra children solo si es admin.
    """
    return rx.cond(
        EmployeeAuthState.is_admin,
        children,
        rx.fragment()
    )