"""
Página de Política de Cookies
"""

import reflex as rx
from ..styles import COLORS


def cookies_policy() -> rx.Component:
    """Página de política de cookies."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Header
                rx.heading(
                    "🍪 Política de Cookies",
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
                
                # ¿Qué son las cookies?
                cookie_section(
                    "¿Qué son las Cookies?",
                    """
                    Las cookies son pequeños archivos de texto que los sitios web almacenan en tu dispositivo 
                    cuando los visitas. Se utilizan ampliamente para hacer que los sitios web funcionen de 
                    manera más eficiente y proporcionar información a los propietarios del sitio.
                    """,
                    "🍪"
                ),
                
                # Tipos de cookies
                rx.heading(
                    "Tipos de Cookies que Utilizamos",
                    size="7",
                    color="white",
                    font_weight="700",
                    margin_bottom="2rem",
                    margin_top="2rem",
                ),
                
                cookie_type_card(
                    "🔒 Cookies Esenciales",
                    "Necesarias",
                    "Estas cookies son estrictamente necesarias para el funcionamiento del sitio web.",
                    [
                        ("session_id", "Identificador de sesión", "Sesión"),
                        ("csrf_token", "Protección contra ataques CSRF", "Sesión"),
                        ("cookie_consent", "Tu preferencia de cookies", "1 año"),
                    ],
                    "success"
                ),
                
                cookie_type_card(
                    "📊 Cookies Analíticas",
                    "Opcionales",
                    "Nos ayudan a entender cómo interactúas con nuestro sitio para mejorarlo.",
                    [
                        ("_ga", "Google Analytics - Usuario único", "2 años"),
                        ("_gid", "Google Analytics - Sesión", "24 horas"),
                        ("_gat", "Google Analytics - Tasa de solicitud", "1 minuto"),
                    ],
                    "info"
                ),
                
                cookie_type_card(
                    "🎯 Cookies de Marketing",
                    "Opcionales",
                    "Utilizadas para mostrarte contenido y publicidad más relevante.",
                    [
                        ("_fbp", "Facebook Pixel - Seguimiento", "3 meses"),
                        ("ad_preferences", "Preferencias de anuncios", "1 año"),
                    ],
                    "warning"
                ),
                
                # Gestión de cookies
                cookie_section(
                    "Cómo Gestionar las Cookies",
                    """
                    Puedes controlar y/o eliminar las cookies como desees. Puedes eliminar todas las 
                    cookies que ya están en tu ordenador y puedes configurar la mayoría de los navegadores 
                    para evitar que se coloquen. Sin embargo, si haces esto, es posible que tengas que 
                    ajustar manualmente algunas preferencias cada vez que visites un sitio.
                    """,
                    "⚙️"
                ),
                
                # Navegadores
                rx.box(
                    rx.heading(
                        "Configuración por Navegador",
                        size="6",
                        color="white",
                        font_weight="700",
                        margin_bottom="1.5rem",
                    ),
                    rx.grid(
                        browser_link("Chrome", "https://support.google.com/chrome/answer/95647"),
                        browser_link("Firefox", "https://support.mozilla.org/es/kb/cookies-terceros-firefox"),
                        browser_link("Safari", "https://support.apple.com/es-es/guide/safari/sfri11471/mac"),
                        browser_link("Edge", "https://support.microsoft.com/es-es/microsoft-edge"),
                        columns="4",
                        spacing="4",
                        width="100%",
                        display=["grid"],
                        grid_template_columns=["1fr", "repeat(2, 1fr)", "repeat(2, 1fr)", "repeat(4, 1fr)"],
                    ),
                    padding="2rem",
                    background="rgba(255,255,255,0.05)",
                    border_radius="12px",
                    margin_bottom="2rem",
                ),
                
                # Contacto
                cookie_section(
                    "¿Preguntas sobre Cookies?",
                    """
                    Si tienes alguna pregunta sobre nuestra política de cookies, puedes contactarnos en:
                    
                    **Email**: privacy@pylink.com
                    
                    Estaremos encantados de ayudarte.
                    """,
                    "📧"
                ),
                
                # Volver
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
            max_width="1000px",
        ),
        
        min_height="100vh",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )


def cookie_section(title: str, content: str, emoji: str) -> rx.Component:
    """Sección de información de cookies."""
    return rx.box(
        rx.hstack(
            rx.text(
                emoji,
                font_size="2.5rem",
            ),
            rx.heading(
                title,
                size="7",
                color="white",
                font_weight="700",
            ),
            spacing="3",
            margin_bottom="1rem",
        ),
        rx.text(
            content,
            color="rgba(255,255,255,0.9)",
            font_size="1.05rem",
            line_height="1.8",
            white_space="pre-line",
        ),
        padding="2rem",
        background="rgba(255,255,255,0.05)",
        border_radius="12px",
        margin_bottom="2rem",
    )


def cookie_type_card(title: str, badge: str, description: str, cookies: list, variant: str) -> rx.Component:
    """Tarjeta de tipo de cookie con detalles."""
    badge_colors = {
        "success": {"bg": "rgba(34, 197, 94, 0.2)", "color": "#22c55e"},
        "info": {"bg": "rgba(59, 130, 246, 0.2)", "color": "#3b82f6"},
        "warning": {"bg": "rgba(234, 179, 8, 0.2)", "color": "#eab308"},
    }
    
    return rx.box(
        rx.hstack(
            rx.heading(
                title,
                size="6",
                color="white",
                font_weight="700",
            ),
            rx.badge(
                badge,
                background=badge_colors[variant]["bg"],
                color=badge_colors[variant]["color"],
                padding="0.3rem 0.8rem",
                border_radius="20px",
                font_weight="600",
            ),
            justify_content="space-between",
            width="100%",
            margin_bottom="1rem",
        ),
        rx.text(
            description,
            color="rgba(255,255,255,0.8)",
            font_size="1rem",
            margin_bottom="1.5rem",
        ),
        rx.vstack(
            *[
                rx.box(
                    rx.hstack(
                        rx.text(
                            cookie[0],
                            font_weight="700",
                            color=COLORS["primary"],
                            font_size="0.95rem",
                            min_width="150px",
                        ),
                        rx.text(
                            cookie[1],
                            color="rgba(255,255,255,0.9)",
                            font_size="0.9rem",
                            flex="1",
                        ),
                        rx.badge(
                            cookie[2],
                            background="rgba(255,255,255,0.1)",
                            color="white",
                            padding="0.2rem 0.6rem",
                            border_radius="12px",
                            font_size="0.8rem",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="0.8rem",
                    background="rgba(0,0,0,0.2)",
                    border_radius="6px",
                )
                for cookie in cookies
            ],
            spacing="2",
            width="100%",
        ),
        padding="2rem",
        background="rgba(255,255,255,0.05)",
        border_left=f"4px solid {badge_colors[variant]['color']}",
        border_radius="12px",
        margin_bottom="2rem",
    )


def browser_link(name: str, url: str) -> rx.Component:
    """Enlace a configuración de navegador."""
    return rx.link(
        rx.box(
            rx.text(
                name,
                font_weight="600",
                color="white",
                font_size="1rem",
            ),
            rx.text(
                "Configurar →",
                color=COLORS["primary"],
                font_size="0.9rem",
            ),
            padding="1rem",
            background="rgba(59, 130, 246, 0.1)",
            border_radius="8px",
            border=f"1px solid {COLORS['primary']}",
            text_align="center",
            cursor="pointer",
            _hover={
                "background": "rgba(59, 130, 246, 0.2)",
                "transform": "translateY(-2px)",
            },
            transition="all 0.2s",
        ),
        href=url,
        is_external=True,
    )
