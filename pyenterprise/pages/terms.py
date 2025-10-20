"""
Página de Términos y Condiciones
"""

import reflex as rx
from ..styles import COLORS


def terms_page() -> rx.Component:
    """Página de términos y condiciones."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Header
                rx.heading(
                    "Términos y Condiciones",
                    size="9",
                    color="white",
                    font_weight="800",
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Última actualización: Octubre 2025",
                    color=COLORS["primary"],
                    font_size="1.1rem",
                    text_align="center",
                    margin_bottom="3rem",
                ),
                
                # Secciones
                terms_section(
                    "1. Aceptación de los Términos",
                    [
                        "Al acceder y utilizar este sitio web, aceptas estar sujeto a estos términos y condiciones.",
                        "Si no estás de acuerdo con alguna parte de estos términos, no debes usar nuestros servicios.",
                        "Nos reservamos el derecho de modificar estos términos en cualquier momento.",
                    ]
                ),
                
                terms_section(
                    "2. Uso del Sitio Web",
                    [
                        "**Uso permitido**: Puedes usar nuestro sitio para fines legales y de acuerdo con estos términos.",
                        "**Prohibiciones**: No puedes usar el sitio para actividades ilegales, spam, o transmitir malware.",
                        "**Propiedad intelectual**: Todo el contenido del sitio es propiedad de PyLink o sus licenciantes.",
                    ]
                ),
                
                terms_section(
                    "3. Servicios Ofrecidos",
                    [
                        "PyLink proporciona servicios de desarrollo web, automatización, análisis de datos y consultoría IT.",
                        "Los servicios específicos se detallan en propuestas personalizadas para cada cliente.",
                        "Nos reservamos el derecho de modificar o discontinuar servicios sin previo aviso.",
                    ]
                ),
                
                terms_section(
                    "4. Registro y Cuentas",
                    [
                        "Algunos servicios pueden requerir creación de cuenta.",
                        "Eres responsable de mantener la confidencialidad de tus credenciales.",
                        "Debes notificarnos inmediatamente de cualquier uso no autorizado de tu cuenta.",
                    ]
                ),
                
                terms_section(
                    "5. Privacidad y Protección de Datos",
                    [
                        "El tratamiento de datos personales se rige por nuestra **Política de Privacidad**.",
                        "Cumplimos con RGPD, LOPD y normativas aplicables de protección de datos.",
                        "Ver nuestra Política de Privacidad para más detalles.",
                    ]
                ),
                
                terms_section(
                    "6. Propiedad Intelectual",
                    [
                        "**Copyright**: Todo el contenido del sitio está protegido por derechos de autor.",
                        "**Marcas**: PyLink y nuestro logo son marcas registradas.",
                        "**Licencias**: No se otorga ninguna licencia sobre nuestra propiedad intelectual sin autorización escrita.",
                    ]
                ),
                
                terms_section(
                    "7. Responsabilidad",
                    [
                        "**Disponibilidad**: No garantizamos que el sitio esté libre de errores o disponible ininterrumpidamente.",
                        "**Contenido de terceros**: No somos responsables del contenido de sitios externos enlazados.",
                        "**Daños**: PyLink no será responsable de daños indirectos, incidentales o consecuentes.",
                    ]
                ),
                
                terms_section(
                    "8. Contratos de Servicio",
                    [
                        "Los proyectos de desarrollo se rigen por contratos específicos adicionales.",
                        "Los términos comerciales, plazos y precios se acuerdan por separado.",
                        "Los contratos de servicio prevalecen sobre estos términos generales en caso de conflicto.",
                    ]
                ),
                
                terms_section(
                    "9. Terminación",
                    [
                        "Podemos suspender o terminar tu acceso al sitio por incumplimiento de estos términos.",
                        "Puedes dejar de usar nuestros servicios en cualquier momento.",
                        "Las disposiciones sobre propiedad intelectual y responsabilidad sobreviven a la terminación.",
                    ]
                ),
                
                terms_section(
                    "10. Ley Aplicable y Jurisdicción",
                    [
                        "Estos términos se rigen por las leyes de España.",
                        "Cualquier disputa será resuelta en los tribunales de [Tu ciudad], España.",
                        "Intentaremos resolver disputas amigablemente antes de litigio.",
                    ]
                ),
                
                terms_section(
                    "11. Contacto",
                    [
                        "Para preguntas sobre estos términos:",
                        "**Email**: legal@pylink.com",
                        "**Teléfono**: +34 XXX XXX XXX",
                        "**Dirección**: [Tu dirección completa]",
                    ]
                ),
                
                # Footer con volver
                rx.box(
                    rx.link(
                        rx.button(
                            "← Volver al Inicio",
                            background=COLORS["primary"],
                            color="white",
                            padding="1rem 2rem",
                            border_radius="10px",
                            font_weight="600",
                            cursor="pointer",
                            _hover={
                                "background": "#2563eb",
                                "transform": "translateY(-2px)",
                            },
                            transition="all 0.2s",
                        ),
                        href="/",
                    ),
                    margin_top="3rem",
                    text_align="center",
                ),
                
                spacing="6",
                padding="6rem 2rem",
            ),
            max_width="900px",
        ),
        
        min_height="100vh",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )


def terms_section(title: str, points: list) -> rx.Component:
    """Sección de términos con título y puntos."""
    return rx.box(
        rx.heading(
            title,
            size="6",
            color="white",
            font_weight="700",
            margin_bottom="1rem",
        ),
        rx.vstack(
            *[
                rx.text(
                    point,
                    color="rgba(255,255,255,0.9)",
                    font_size="1.05rem",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                )
                for point in points
            ],
            align_items="start",
            spacing="2",
            padding_left="1rem",
        ),
        
        padding="2rem",
        background="rgba(255,255,255,0.05)",
        border_left=f"4px solid {COLORS['primary']}",
        border_radius="8px",
        margin_bottom="2rem",
    )
