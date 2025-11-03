"""
Landing page responsive y moderno para PyEnterprise
"""

import reflex as rx
from ..styles import COLORS
from shared.responsive_utils import (
    responsive_container,
    responsive_grid,
    responsive_heading,
    responsive_text,
    responsive_card,
    responsive_button,
    responsive_stack,
    responsive_image,
    responsive_form_field
)


def responsive_hero() -> rx.Component:
    """Sección hero responsive"""
    return rx.section(
        responsive_container(
            rx.vstack(
                # Contenido principal
                rx.vstack(
                    responsive_heading(1, weight="700", align="center"),
                    responsive_text(
                        "Transforma tu empresa con soluciones Python personalizadas",
                        size_mobile="1.125rem",
                        size_desktop="1.25rem"
                    ),
                    rx.text(
                        "Desarrollo de software, automatización y consultoría empresarial",
                        font_size="1rem",
                        color=COLORS["text_light"],
                        text_align="center",
                        margin_bottom="2rem"
                    ),
                    # Botones de CTA
                    rx.hstack(
                        responsive_button(
                            size_tablet="4",
                            color_scheme="blue",
                            full_width_mobile=False
                        ),
                        responsive_button(
                            size_tablet="4",
                            color_scheme="gray",
                            full_width_mobile=False
                        ),
                        spacing="4",
                        align_items="center",
                        justify="center"
                    ),
                    spacing="4",
                    align_items="center",
                    width="100%",
                    max_width="800px"
                ),

                # Espaciador
                rx.box(height="3rem"),

                # Imagen hero responsive
                responsive_image(
                    "/hero-image.jpg",
                    "PyEnterprise Platform",
                    height_mobile="250px",
                    height_tablet="400px",
                    height_desktop="500px"
                ),
                spacing="6",
                align_items="center",
                width="100%",
                padding_y="4rem"
            )
        ),
        background=f"""
            linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%)
        """,
        color="white",
        width="100%",
        min_height="100vh",
        display="flex",
        align_items="center"
    )


def responsive_services() -> rx.Component:
    """Sección de servicios responsive"""
    services = [
        {
            "icon": "code",
            "title": "Desarrollo a Medida",
            "description": "Soluciones software personalizadas con Python y tecnologías modernas",
            "color": "blue"
        },
        {
            "icon": "brain",
            "title": "Automatización",
            "description": "Automatización de procesos para aumentar la eficiencia empresarial",
            "color": "green"
        },
        {
            "icon": "bar_chart",
            "title": "Análisis de Datos",
            "description": "Visualización y análisis de datos para toma de decisiones informada",
            "color": "purple"
        },
        {
            "icon": "cloud",
            "title": "Cloud Computing",
            "description": "Soluciones escalables en la nube con AWS, Google Cloud y Azure",
            "color": "orange"
        }
    ]

    return rx.section(
        responsive_container(
            rx.vstack(
                responsive_heading(2, weight="600", align="center"),
                rx.text(
                    "Servicios que impulsan tu negocio",
                    font_size="1.125rem",
                    color=COLORS["text_light"],
                    text_align="center",
                    margin_bottom="3rem"
                ),

                # Grid de servicios responsive
                responsive_grid(
                    mobile_columns=1,
                    tablet_columns=2,
                    desktop_columns=4,
                    spacing="6"
                )(
                    *[responsive_card(padding_mobile="1.5rem")(
                        rx.vstack(
                            rx.icon(
                                service["icon"],
                                size=32,
                                color=COLORS[service["color"]]
                            ),
                            responsive_heading(4, weight="600"),
                            rx.text(
                                service["description"],
                                font_size="0.875rem",
                                color=COLORS["text_light"],
                                text_align="center"
                            ),
                            spacing="3",
                            align_items="center"
                        )
                    ) for service in services]
                ),

                spacing="8",
                width="100%",
                padding_y="4rem"
            )
        ),
        background_color=COLORS["background"],
        width="100%"
    )


def responsive_contact() -> rx.Component:
    """Sección de contacto responsive"""
    return rx.section(
        responsive_container(
            rx.vstack(
                responsive_heading(2, weight="600", align="center"),
                rx.text(
                    "Hablemos sobre tu próximo proyecto",
                    font_size="1.125rem",
                    color=COLORS["text_light"],
                    text_align="center",
                    margin_bottom="3rem"
                ),

                # Formulario responsive
                responsive_card(padding_mobile="2rem")(
                    rx.vstack(
                        responsive_form_field("Nombre", "Tu nombre completo"),
                        responsive_form_field("Email", "tu@email.com", "email"),
                        responsive_form_field("Teléfono", "Teléfono de contacto", "tel"),
                        responsive_form_field("Mensaje", "Cuéntanos sobre tu proyecto", "textarea"),

                        responsive_button(
                            size_tablet="4",
                            color_scheme="blue",
                            full_width_mobile=True
                        ),
                        spacing="4",
                        width="100%"
                    )
                ),

                spacing="6",
                width="100%",
                max_width="600px",
                padding_y="4rem"
            )
        ),
        background_color=COLORS["surface"],
        width="100%"
    )


def responsive_footer() -> rx.Component:
    """Footer responsive"""
    return rx.footer(
        responsive_container(
            responsive_stack(
                direction_mobile="column",
                direction_tablet="row",
                spacing="6",
                align_items="start"
            )(
                # Company info
                rx.vstack(
                    rx.heading("PyEnterprise", size="4", font_weight="700"),
                    rx.text(
                        "Soluciones empresariales con Python",
                        font_size="0.875rem",
                        color=COLORS["text_light"]
                    ),
                    spacing="2",
                    align_items="start"
                ),

                # Links
                rx.vstack(
                    rx.text("Enlaces", font_weight="600"),
                    rx.link("Inicio", href="/", color=COLORS["text_light"]),
                    rx.link("Servicios", href="/servicios", color=COLORS["text_light"]),
                    rx.link("Contacto", href="/contacto", color=COLORS["text_light"]),
                    spacing="2",
                    align_items="start"
                ),

                # Contact info
                rx.vstack(
                    rx.text("Contacto", font_weight="600"),
                    rx.text("hola@pyenterprise.com", color=COLORS["text_light"]),
                    rx.text("+34 900 123 456", color=COLORS["text_light"]),
                    spacing="2",
                    align_items="start"
                ),

                # Social links
                rx.vstack(
                    rx.text("Síguenos", font_weight="600"),
                    rx.hstack(
                        rx.icon("mail", size=20),
                        rx.icon("phone", size=20),
                        rx.icon("linkedin", size=20),
                        spacing="3"
                    ),
                    spacing="2",
                    align_items="start"
                )
            ),

            # Divider
            rx.divider(border_color=COLORS["border"], margin_y="2rem"),

            # Copyright
            rx.hstack(
                rx.text("© 2024 PyEnterprise. Todos los derechos reservados."),
                rx.text("Desarrollado con ❤️ y Python"),
                justify="space_between",
                align_items="center",
                width="100%"
            ),

            padding_y="3rem",
            width="100%"
        ),
        background_color=COLORS["background"],
        border_top=f"1px solid {COLORS['border']}",
        width="100%"
    )


def responsive_landing_page() -> rx.Component:
    """Landing page completa y responsive"""
    return rx.box(
        responsive_hero(),
        responsive_services(),
        responsive_contact(),
        responsive_footer(),
        width="100%"
    )