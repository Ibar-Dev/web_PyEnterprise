"""
Componente About Section para PyEnterprise
"""

import reflex as rx
from shared.styles import section_style, container_style, subtitle_style, card_style, COLORS


def about_section() -> rx.Component:
    """Sección sobre nosotros con información de la empresa."""
    return rx.box(
        rx.container(
            # Título de la sección
            rx.heading(
                "Sobre PyEnterprise",
                **subtitle_style,
                margin_bottom="3rem",
            ),
            
            rx.grid(
                # Columna izquierda - Texto principal
                rx.vstack(
                    rx.heading(
                        "Expertos en Desarrollo Python",
                        size="lg",
                        color=COLORS["text"],
                        margin_bottom="1.5rem",
                        font_weight="600",
                    ),
                    
                    rx.text(
                        "En PyEnterprise, somos especialistas en crear soluciones "
                        "tecnológicas robustas y escalables utilizando Python. Con más de "
                        "5 años de experiencia en el mercado, hemos ayudado a empresas de "
                        "todos los tamaños a digitalizar sus procesos y optimizar sus operaciones.",
                        font_size="1.1rem",
                        color=COLORS["text_light"],
                        line_height="1.7",
                        margin_bottom="1.5rem",
                    ),
                    
                    rx.text(
                        "Nuestro equipo combina experiencia técnica con una profunda "
                        "comprensión de las necesidades empresariales, lo que nos permite "
                        "entregar soluciones que realmente impactan en el crecimiento de nuestros clientes.",
                        font_size="1.1rem",
                        color=COLORS["text_light"],
                        line_height="1.7",
                        margin_bottom="2rem",
                    ),
                    
                    # Lista de ventajas
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="check_circle", color=COLORS["success"], size="20px"),
                            rx.text("Metodología ágil y entregas rápidas", font_weight="500"),
                            align_items="center",
                            spacing="3",
                        ),
                        rx.hstack(
                            rx.icon(tag="check_circle", color=COLORS["success"], size="20px"),
                            rx.text("Soporte técnico continuo y mantenimiento", font_weight="500"),
                            align_items="center",
                            spacing="3",
                        ),
                        rx.hstack(
                            rx.icon(tag="check_circle", color=COLORS["success"], size="20px"),
                            rx.text("Soluciones escalables y personalizadas", font_weight="500"),
                            align_items="center",
                            spacing="3",
                        ),
                        rx.hstack(
                            rx.icon(tag="check_circle", color=COLORS["success"], size="20px"),
                            rx.text("Equipo certificado en tecnologías Python", font_weight="500"),
                            align_items="center",
                            spacing="3",
                        ),
                        align_items="start",
                        spacing="3",
                    ),
                    
                    align_items="start",
                    spacing="4",
                ),
                
                # Columna derecha - Estadísticas y valores
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Nuestra Misión",
                                size="md",
                                color=COLORS["primary"],
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Democratizar el acceso a tecnología avanzada, "
                                "ayudando a las empresas a innovar y crecer "
                                "mediante soluciones Python de alta calidad.",
                                color=COLORS["text_light"],
                                line_height="1.6",
                            ),
                            align_items="start",
                            spacing="2",
                        ),
                        **card_style,
                        margin_bottom="1.5rem",
                    ),
                    
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Nuestra Visión",
                                size="md",
                                color=COLORS["primary"],
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Ser la empresa líder en soluciones Python "
                                "empresariales, reconocida por la excelencia "
                                "técnica y el impacto positivo en nuestros clientes.",
                                color=COLORS["text_light"],
                                line_height="1.6",
                            ),
                            align_items="start",
                            spacing="2",
                        ),
                        **card_style,
                        margin_bottom="1.5rem",
                    ),
                    
                    # Estadísticas rápidas
                    rx.grid(
                        rx.box(
                            rx.text("100+", font_size="2rem", font_weight="700", color=COLORS["primary"]),
                            rx.text("Proyectos", font_size="0.9rem", color=COLORS["text_light"]),
                            text_align="center",
                            padding="1rem",
                        ),
                        rx.box(
                            rx.text("50+", font_size="2rem", font_weight="700", color=COLORS["primary"]),
                            rx.text("Clientes", font_size="0.9rem", color=COLORS["text_light"]),
                            text_align="center",
                            padding="1rem",
                        ),
                        columns="2",
                        spacing="4",
                        **card_style,
                    ),
                    
                    spacing="4",
                ),
                
                columns=["1", "1", "2", "2"],  # Responsive: 1 columna en móvil, 2 en desktop
                spacing="8",
                align_items="start",
            ),
            **container_style,
        ),
        id="nosotros",
        background_color=COLORS["surface"],
        **section_style,
    )
