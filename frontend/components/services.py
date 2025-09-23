"""
Componente Services Section para PyEnterprise
"""

import reflex as rx
from shared.styles import section_style, container_style, subtitle_style, card_style, COLORS


def service_card(icon: str, title: str, description: str, features: list) -> rx.Component:
    """Tarjeta individual de servicio."""
    return rx.box(
        rx.vstack(
            # Icono del servicio
            rx.box(
                rx.icon(tag=icon, size="48px", color="white"),
                background_color=COLORS["primary"],
                border_radius="16px",
                padding="16px",
                margin_bottom="1.5rem",
            ),
            
            # Título del servicio
            rx.heading(
                title,
                size="lg",
                color=COLORS["text"],
                margin_bottom="1rem",
                font_weight="600",
            ),
            
            # Descripción
            rx.text(
                description,
                color=COLORS["text_light"],
                line_height="1.6",
                margin_bottom="1.5rem",
                text_align="center",
            ),
            
            # Lista de características
            rx.vstack(
                *[
                    rx.hstack(
                        rx.icon(tag="check", color=COLORS["success"], size="16px"),
                        rx.text(feature, font_size="0.9rem", color=COLORS["text_light"]),
                        align_items="center",
                        spacing="2",
                        width="100%",
                    )
                    for feature in features
                ],
                align_items="start",
                spacing="2",
                width="100%",
            ),
            
            align_items="center",
            spacing="3",
            height="100%",
        ),
        **card_style,
        height="100%",
    )


def services_section() -> rx.Component:
    """Sección de servicios principales."""
    return rx.box(
        rx.container(
            # Título de la sección
            rx.heading(
                "Nuestros Servicios",
                **subtitle_style,
                margin_bottom="1rem",
            ),
            
            rx.text(
                "Ofrecemos soluciones completas en Python para impulsar tu negocio",
                font_size="1.2rem",
                color=COLORS["text_light"],
                text_align="center",
                margin_bottom="4rem",
            ),
            
            # Grid de servicios
            rx.grid(
                service_card(
                    icon="code",
                    title="Desarrollo Web",
                    description="Aplicaciones web modernas y escalables con frameworks como Django, Flask y FastAPI.",
                    features=[
                        "Desarrollo Full-Stack",
                        "APIs RESTful y GraphQL",
                        "Interfaces responsivas",  
                        "Integración de bases de datos",
                        "Optimización de rendimiento"
                    ]
                ),
                
                service_card(
                    icon="settings",
                    title="Automatización",
                    description="Automatizamos procesos empresariales para mejorar la eficiencia y reducir costos operativos.",
                    features=[
                        "Automatización de tareas",
                        "Web scraping inteligente",
                        "Procesamiento de documentos",
                        "Integración de sistemas",
                        "Workflows personalizados"
                    ]
                ),
                
                service_card(
                    icon="bar_chart",
                    title="Análisis de Datos",
                    description="Convertimos tus datos en insights accionables con herramientas de análisis avanzado.",
                    features=[
                        "Business Intelligence",
                        "Dashboards interactivos",
                        "Machine Learning",
                        "Visualización de datos",
                        "Reportes automatizados"
                    ]
                ),
                
                service_card(
                    icon="cloud",
                    title="Cloud & DevOps",
                    description="Implementación y gestión de infraestructura en la nube con mejores prácticas DevOps.",
                    features=[
                        "Despliegue en AWS/Azure/GCP",
                        "Containerización con Docker",
                        "CI/CD automatizado",
                        "Monitoreo y logging",
                        "Escalabilidad automática"
                    ]
                ),
                
                service_card(
                    icon="shield",
                    title="Consultoría Tech",
                    description="Asesoramiento técnico especializado para tomar las mejores decisiones tecnológicas.",
                    features=[
                        "Arquitectura de software",
                        "Auditoría de código",
                        "Migración de sistemas",
                        "Capacitación técnica",
                        "Estrategia tecnológica"
                    ]
                ),
                
                service_card(
                    icon="smartphone",
                    title="Aplicaciones Móviles",
                    description="Desarrollo de aplicaciones móviles multiplataforma con tecnologías modernas.",
                    features=[
                        "Apps nativas e híbridas",
                        "Backend con Python",
                        "Integración con APIs",
                        "Publicación en stores",
                        "Mantenimiento continuo"
                    ]
                ),
                
                columns=["1", "2", "3", "3"],  # Responsive grid
                spacing="6",
                width="100%",
            ),
            
            # Call to action
            rx.box(
                rx.vstack(
                    rx.heading(
                        "¿Necesitas una solución personalizada?",
                        size="lg",
                        color=COLORS["text"],
                        text_align="center",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Contáctanos para discutir tu proyecto y crear una propuesta a medida",
                        color=COLORS["text_light"],
                        text_align="center",
                        margin_bottom="2rem",
                    ),
                    rx.button(
                        "Solicitar Cotización",
                        background_color=COLORS["primary"],
                        color="white",
                        font_weight="600",
                        padding="16px 32px",
                        border_radius="10px",
                        font_size="1.1rem",
                        _hover={
                            "background_color": COLORS["secondary"],
                            "transform": "translateY(-2px)",
                        },
                        transition="all 0.3s ease",
                    ),
                    align_items="center",
                    spacing="4",
                ),
                margin_top="4rem",
                padding="3rem",
                background_color=COLORS["surface"],
                border_radius="16px",
                border=f"1px solid {COLORS['border']}",
            ),
            
            **container_style,
        ),
        id="servicios",
        **section_style,
    )
