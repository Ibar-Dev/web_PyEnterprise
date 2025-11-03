"""
Utilidades de diseño responsive para PyEnterprise
"""

import reflex as rx
from typing import Dict, Any


# Breakpoints para dispositivos móviles
BREAKPOINTS = {
    "mobile": "480px",
    "tablet": "768px",
    "desktop": "1024px",
    "wide": "1280px"
}


def responsive_style(
    mobile: Dict[str, Any],
    tablet: Dict[str, Any] = None,
    desktop: Dict[str, Any] = None,
    wide: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Crea estilos responsive que se adaptan según el tamaño de pantalla.
    Los estilos se aplican en cascada (mobile < tablet < desktop < wide).
    """
    base_style = mobile.copy()

    if tablet:
        base_style.update(tablet)
    if desktop:
        base_style.update(desktop)
    if wide:
        base_style.update(wide)

    return base_style


def responsive_grid(
    mobile_columns: int = 1,
    tablet_columns: int = 2,
    desktop_columns: int = 3,
    wide_columns: int = 4,
    spacing: str = "4"
) -> rx.Component:
    """
    Crea una cuadrícula responsive con diferentes columnas según el dispositivo.
    """
    return rx.grid(
        columns=[f"{mobile_columns}fr", f"{tablet_columns}fr", f"{desktop_columns}fr", f"{wide_columns}fr"],
        spacing=spacing,
        width="100%"
    )


def responsive_container(
    padding_mobile: str = "1rem",
    padding_tablet: str = "2rem",
    padding_desktop: str = "3rem",
    max_width: str = "1200px"
) -> rx.Component:
    """
    Crea un contenedor responsive con padding adaptativo.
    """
    return rx.container(
        max_width=max_width,
        padding_x=[
            padding_mobile,
            padding_tablet,
            padding_desktop,
            padding_desktop
        ],
        width="100%"
    )


def responsive_text(
    size_mobile: str = "1rem",
    size_tablet: str = "1.125rem",
    size_desktop: str = "1.25rem",
    weight: str = "400"
) -> rx.Component:
    """
    Crea texto responsive con tamaños adaptativos.
    """
    return rx.text(
        font_size=[size_mobile, size_tablet, size_desktop],
        font_weight=weight
    )


def responsive_heading(
    level: int = 3,
    weight: str = "600",
    align: str = "left"
) -> rx.Component:
    """
    Crea encabezados responsive.
    """
    sizes = {
        1: ["2rem", "2.5rem", "3rem", "3.5rem"],
        2: ["1.5rem", "1.75rem", "2rem", "2.25rem"],
        3: ["1.25rem", "1.5rem", "1.75rem", "2rem"],
        4: ["1.125rem", "1.25rem", "1.5rem", "1.75rem"],
        5: ["1rem", "1.125rem", "1.25rem", "1.5rem"],
        6: ["0.875rem", "1rem", "1.125rem", "1.25rem"]
    }

    return rx.heading(
        size=sizes[level],
        font_weight=weight,
        text_align=align
    )


def responsive_card(
    padding_mobile: str = "1rem",
    padding_tablet: str = "1.5rem",
    padding_desktop: str = "2rem",
    shadow: bool = True,
    border: bool = True
) -> rx.Component:
    """
    Crea una tarjeta responsive con padding adaptativo.
    """
    base_style = {
        "padding": [padding_mobile, padding_tablet, padding_desktop],
        "border_radius": "12px",
        "transition": "all 0.3s ease",
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.1)"
        }
    }

    if shadow:
        base_style["box_shadow"] = "0 4px 6px rgba(0, 0, 0, 0.05)"

    if border:
        from ..styles import COLORS
        base_style["border"] = f"1px solid {COLORS['border']}"

    return rx.card(**base_style)


def responsive_button(
    size_mobile: str = "2",
    size_tablet: str = "3",
    color_scheme: str = "blue",
    full_width_mobile: bool = True
) -> rx.Component:
    """
    Crea un botón responsive.
    """
    return rx.button(
        size=[size_mobile, size_tablet, size_tablet, size_tablet],
        color_scheme=color_scheme,
        width="100%" if full_width_mobile else "auto",
        _hover={"transform": "translateY(-1px)"}
    )


def responsive_stack(
    direction_mobile: str = "column",
    direction_tablet: str = "row",
    spacing: str = "4",
    align_items: str = "center"
) -> rx.Component:
    """
    Crea un stack responsive que cambia de dirección según el dispositivo.
    """
    return rx.hstack(
        direction=[direction_mobile, direction_tablet, direction_tablet],
        spacing=spacing,
        align_items=align_items,
        width="100%"
    )


def mobile_menu() -> rx.Component:
    """
    Menú hamburguesa para dispositivos móviles.
    """
    return rx.box(
        rx.button(
            rx.icon("menu", size=24),
            background_color="transparent",
            color="white",
            border="none",
            cursor="pointer",
            padding="8px",
            _hover={"background_color": "rgba(255, 255, 255, 0.1)"},
            display=["flex", "flex", "none", "none"],
        ),
        position="fixed",
        top="1rem",
        right="1rem",
        z_index="1000"
    )


def responsive_sidebar() -> rx.Component:
    """
    Sidebar responsive que se convierte en menú móvil.
    """
    return rx.box(
        # Sidebar content would go here
        # This is a placeholder for the responsive sidebar implementation
        width="250px",
        background_color="white",
        border="1px solid #e5e7eb",
        display=["none", "none", "block", "block"],
        height="100vh",
        position="fixed",
        left="0",
        top="0",
        z_index="999"
    )


def responsive_image(
    src: str,
    alt: str,
    height_mobile: str = "200px",
    height_tablet: str = "300px",
    height_desktop: str = "400px",
    object_fit: str = "cover"
) -> rx.Component:
    """
    Crea una imagen responsive con alturas adaptativas.
    """
    return rx.image(
        src=src,
        alt=alt,
        height=[height_mobile, height_tablet, height_desktop],
        width="100%",
        object_fit=object_fit,
        border_radius="8px"
    )


def responsive_form_field(
    label: str,
    placeholder: str,
    input_type: str = "text"
) -> rx.Component:
    """
    Crea un campo de formulario responsive.
    """
    return rx.vstack(
        rx.text(label, font_weight="500", margin_bottom="0.5rem"),
        rx.input(
            placeholder=placeholder,
            type=input_type,
            width="100%",
            padding="12px 16px",
            border="1px solid #d1d5db",
            border_radius="8px",
            font_size="16px",
            _focus={
                "outline": "none",
                "border_color": "#3b82f6",
                "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.1)"
            }
        ),
        spacing="1",
        width="100%"
    )


def hide_on_mobile(element: rx.Component) -> rx.Component:
    """
    Oculta un elemento en dispositivos móviles.
    """
    return rx.box(
        element,
        display=["none", "block", "block", "block"]
    )


def show_only_mobile(element: rx.Component) -> rx.Component:
    """
    Muestra un elemento solo en dispositivos móviles.
    """
    return rx.box(
        element,
        display=["block", "none", "none", "none"]
    )