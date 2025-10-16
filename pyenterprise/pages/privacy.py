"""
Página de Política de Privacidad
"""

import reflex as rx
from ..styles import COLORS


def privacy_policy() -> rx.Component:
    """Página de política de privacidad."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Header
                rx.heading(
                    "Política de Privacidad",
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
                policy_section(
                    "1. Información que Recopilamos",
                    [
                        "**Información de contacto**: Nombre, email, teléfono cuando nos contactas.",
                        "**Datos de uso**: Páginas visitadas, tiempo de navegación, ubicación general.",
                        "**Cookies**: Datos técnicos almacenados en tu navegador para mejorar la experiencia.",
                    ]
                ),
                
                policy_section(
                    "2. Cómo Utilizamos tu Información",
                    [
                        "Responder a tus consultas y solicitudes de servicio.",
                        "Mejorar nuestro sitio web y servicios.",
                        "Enviar comunicaciones relevantes (con tu consentimiento).",
                        "Cumplir con obligaciones legales.",
                    ]
                ),
                
                policy_section(
                    "3. Base Legal del Tratamiento (RGPD)",
                    [
                        "**Consentimiento**: Para cookies no esenciales y comunicaciones marketing.",
                        "**Ejecución de contrato**: Para proporcionar servicios solicitados.",
                        "**Interés legítimo**: Para mejorar nuestros servicios y seguridad.",
                        "**Obligación legal**: Para cumplir con requisitos regulatorios.",
                    ]
                ),
                
                policy_section(
                    "4. Compartir Información",
                    [
                        "**No vendemos** tu información personal a terceros.",
                        "Compartimos datos solo con proveedores de servicios esenciales (hosting, analytics).",
                        "Podemos compartir información si es requerido legalmente.",
                    ]
                ),
                
                policy_section(
                    "5. Tus Derechos (RGPD/LOPD)",
                    [
                        "**Acceso**: Solicitar copia de tus datos personales.",
                        "**Rectificación**: Corregir datos inexactos.",
                        "**Supresión**: Solicitar eliminación de tus datos ('derecho al olvido').",
                        "**Portabilidad**: Recibir tus datos en formato estructurado.",
                        "**Oposición**: Oponerte al tratamiento de tus datos.",
                        "**Limitación**: Solicitar restricción del tratamiento.",
                    ]
                ),
                
                policy_section(
                    "6. Seguridad de Datos",
                    [
                        "Implementamos medidas técnicas y organizativas para proteger tus datos.",
                        "Uso de encriptación SSL/TLS para transmisión segura.",
                        "Acceso restringido a datos personales solo a personal autorizado.",
                        "Auditorías y actualizaciones regulares de seguridad.",
                    ]
                ),
                
                policy_section(
                    "7. Retención de Datos",
                    [
                        "Conservamos tus datos solo durante el tiempo necesario.",
                        "Datos de contacto: Hasta que solicites su eliminación o 3 años sin actividad.",
                        "Datos de cookies: Según configuración establecida (máx. 13 meses).",
                    ]
                ),
                
                policy_section(
                    "8. Cookies",
                    [
                        "Ver nuestra **Política de Cookies** detallada.",
                        "Puedes configurar tus preferencias en cualquier momento.",
                        "Las cookies esenciales son necesarias para el funcionamiento del sitio.",
                    ]
                ),
                
                policy_section(
                    "9. Contacto DPO",
                    [
                        "Para ejercer tus derechos o consultas sobre privacidad:",
                        "**Email**: privacy@pylink.com",
                        "**Dirección**: [Tu dirección completa]",
                        "Responderemos en un plazo máximo de 30 días.",
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


def policy_section(title: str, points: list) -> rx.Component:
    """Sección de política con título y puntos."""
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
