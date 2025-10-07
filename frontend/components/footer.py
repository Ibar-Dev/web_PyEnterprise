"""
Componente Footer para PyEnterprise
"""

import reflex as rx
from shared.styles import container_style, COLORS


def footer_link(text: str, href: str) -> rx.Component:
    """Link del footer con estilos consistentes."""
    return rx.link(
        text,
        href=href,
        color=COLORS["text_light"],
        _hover={
            "color": COLORS["primary"],
            "text_decoration": "none",
        },
        transition="color 0.3s ease",
    )


def footer() -> rx.Component:
    """Footer principal con información de la empresa y enlaces."""
    return rx.box(
        rx.container(
            rx.grid(
                # Columna 1 - Información de la empresa
                rx.vstack(
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
                            background="linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(59, 130, 246, 0.2))",
                            box_shadow="0 0 15px rgba(94, 234, 212, 0.4), 0 0 30px rgba(59, 130, 246, 0.2)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "scale(1.15) rotate(-5deg)",
                                "box_shadow": "0 0 25px rgba(94, 234, 212, 0.6), 0 0 50px rgba(59, 130, 246, 0.4)",
                            },
                        ),
                        rx.heading(
                            "PyLink",
                            size="md",
                            color=COLORS["primary"],
                            font_weight="700",
                        ),
                        align_items="center",
                        spacing="3",
                        margin_bottom="1rem",
                    ),
                    
                    rx.text(
                        "Transformamos negocios con soluciones Python avanzadas. "
                        "Especialistas en desarrollo web, automatización y análisis de datos.",
                        color=COLORS["text_light"],
                        line_height="1.6",
                        font_size="0.9rem",
                        margin_bottom="1.5rem",
                    ),
                    
                    # Redes sociales
                    rx.hstack(
                        rx.link(
                            rx.icon(tag="fab fa-linkedin", size="20px"),
                            href="https://linkedin.com/company/pyenterprise",
                            color=COLORS["text_light"],
                            _hover={"color": COLORS["primary"]},
                            transition="color 0.3s ease",
                        ),
                        rx.link(
                            rx.icon(tag="fab fa-github", size="20px"),
                            href="https://github.com/pyenterprise",
                            color=COLORS["text_light"],
                            _hover={"color": COLORS["primary"]},
                            transition="color 0.3s ease",
                        ),
                        rx.link(
                            rx.icon(tag="fab fa-twitter", size="20px"),
                            href="https://twitter.com/pyenterprise",
                            color=COLORS["text_light"],
                            _hover={"color": COLORS["primary"]},
                            transition="color 0.3s ease",
                        ),
                        rx.link(
                            rx.icon(tag="fab fa-youtube", size="20px"),
                            href="https://youtube.com/@pyenterprise",
                            color=COLORS["text_light"],
                            _hover={"color": COLORS["primary"]},
                            transition="color 0.3s ease",
                        ),
                        spacing="4",
                    ),
                    
                    align_items="start",
                    spacing="3",
                ),
                
                # Columna 2 - Enlaces rápidos
                rx.vstack(
                    rx.heading(
                        "Enlaces Rápidos",
                        size="sm",
                        color=COLORS["text"],
                        margin_bottom="1rem",
                        font_weight="600",
                    ),
                    
                    footer_link("Inicio", "#inicio"),
                    footer_link("Sobre Nosotros", "#nosotros"),
                    footer_link("Servicios", "#servicios"),
                    footer_link("Contacto", "#contacto"),
                    footer_link("Blog", "/blog"),
                    footer_link("Casos de Éxito", "/casos-exito"),
                    
                    align_items="start",
                    spacing="2",
                ),
                
                # Columna 3 - Servicios
                rx.vstack(
                    rx.heading(
                        "Servicios",
                        size="sm",
                        color=COLORS["text"],
                        margin_bottom="1rem",
                        font_weight="600",
                    ),
                    
                    footer_link("Desarrollo Web", "/servicios/desarrollo-web"),
                    footer_link("Automatización", "/servicios/automatizacion"),
                    footer_link("Análisis de Datos", "/servicios/analisis-datos"),
                    footer_link("Cloud & DevOps", "/servicios/cloud-devops"),
                    footer_link("Consultoría", "/servicios/consultoria"),
                    footer_link("Apps Móviles", "/servicios/apps-moviles"),
                    
                    align_items="start",
                    spacing="2",
                ),
                
                # Columna 4 - Contacto
                rx.vstack(
                    rx.heading(
                        "Contacto",
                        size="sm",
                        color=COLORS["text"],
                        margin_bottom="1rem",
                        font_weight="600",
                    ),
                    
                    rx.hstack(
                        rx.icon(tag="email", size="16px", color=COLORS["primary"]),
                        rx.text(
                            "contacto@pyenterprise.com",
                            color=COLORS["text_light"],
                            font_size="0.9rem",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    
                    rx.hstack(
                        rx.icon(tag="phone", size="16px", color=COLORS["primary"]),
                        rx.text(
                            "+34 900 123 456",
                            color=COLORS["text_light"],
                            font_size="0.9rem",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    
                    rx.hstack(
                        rx.icon(tag="location_on", size="16px", color=COLORS["primary"]),
                        rx.text(
                            "Madrid, España",
                            color=COLORS["text_light"],
                            font_size="0.9rem",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    
                    rx.hstack(
                        rx.icon(tag="schedule", size="16px", color=COLORS["primary"]),
                        rx.text(
                            "Lun - Vie: 9:00 - 18:00",
                            color=COLORS["text_light"],
                            font_size="0.9rem",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    
                    align_items="start",
                    spacing="3",
                ),
                
                columns=["1", "2", "4", "4"],  # Responsive
                spacing="8",
                align_items="start",
            ),
            
            # Línea divisoria
            rx.divider(
                border_color=COLORS["border"],
                margin="3rem 0 2rem 0",
            ),
            
            # Copyright y enlaces legales
            rx.hstack(
                rx.text(
                    f"© 2024 PyEnterprise. Todos los derechos reservados.",
                    color=COLORS["text_light"],
                    font_size="0.9rem",
                ),
                
                rx.hstack(
                    footer_link("Política de Privacidad", "/privacidad"),
                    footer_link("Términos de Servicio", "/terminos"),
                    footer_link("Cookies", "/cookies"),
                    spacing="6",
                ),
                
                justify_content="space-between",
                align_items="center",
                wrap="wrap",
                width="100%",
            ),
            
            **container_style,
        ),
        
        background_color=COLORS["text"],
        color="white",
        padding="4rem 0 2rem 0",
        margin_top="4rem",
    )
