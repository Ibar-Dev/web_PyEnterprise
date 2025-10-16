"""
Componente de Banner de Cookies con consentimiento GDPR/LOPD
"""

import reflex as rx
from ..styles import COLORS


class CookieState(rx.State):
    """Estado para gestión de cookies."""
    show_banner: bool = True
    cookies_accepted: bool = False
    show_preferences: bool = False
    
    # Preferencias de cookies
    essential_cookies: bool = True  # Siempre activadas
    analytics_cookies: bool = False
    marketing_cookies: bool = False
    
    def set_analytics_cookies(self, value: bool):
        """Setter para analytics_cookies."""
        self.analytics_cookies = value
    
    def set_marketing_cookies(self, value: bool):
        """Setter para marketing_cookies."""
        self.marketing_cookies = value
    
    def accept_all_cookies(self):
        """Aceptar todas las cookies."""
        self.cookies_accepted = True
        self.analytics_cookies = True
        self.marketing_cookies = True
        self.show_banner = False
        # Aquí guardarías en localStorage o cookie real
        
    def accept_essential_only(self):
        """Aceptar solo cookies esenciales."""
        self.cookies_accepted = True
        self.analytics_cookies = False
        self.marketing_cookies = False
        self.show_banner = False
        
    def toggle_preferences(self):
        """Mostrar/ocultar preferencias."""
        self.show_preferences = not self.show_preferences
        
    def save_preferences(self):
        """Guardar preferencias personalizadas."""
        self.cookies_accepted = True
        self.show_banner = False
        self.show_preferences = False


def cookie_banner() -> rx.Component:
    """Banner de cookies con opciones de consentimiento."""
    return rx.cond(
        CookieState.show_banner,
        rx.box(
            rx.container(
                rx.box(
                    # Versión compacta (por defecto)
                    rx.cond(
                        ~CookieState.show_preferences,
                        rx.hstack(
                            # Icono y texto
                            rx.hstack(
                                rx.box(
                                    "🍪",
                                    font_size="2rem",
                                ),
                                rx.vstack(
                                    rx.text(
                                        "Usamos cookies",
                                        font_size="1.1rem",
                                        font_weight="700",
                                        color="white",
                                        margin_bottom="0.3rem",
                                    ),
                                    rx.text(
                                        "Utilizamos cookies para mejorar tu experiencia, analizar el tráfico y personalizar el contenido. ",
                                        font_size="0.95rem",
                                        color="rgba(255,255,255,0.9)",
                                        max_width="600px",
                                    ),
                                    align_items="start",
                                    spacing="1",
                                ),
                                spacing="4",
                                align_items="center",
                                flex="1",
                            ),
                            
                            # Botones
                            rx.hstack(
                                rx.button(
                                    "Configurar",
                                    on_click=CookieState.toggle_preferences,
                                    background="transparent",
                                    color="white",
                                    border=f"2px solid {COLORS['primary']}",
                                    padding="0.7rem 1.5rem",
                                    border_radius="8px",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={
                                        "background": "rgba(59, 130, 246, 0.1)",
                                    },
                                ),
                                rx.button(
                                    "Rechazar",
                                    on_click=CookieState.accept_essential_only,
                                    background="rgba(255,255,255,0.1)",
                                    color="white",
                                    padding="0.7rem 1.5rem",
                                    border_radius="8px",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={
                                        "background": "rgba(255,255,255,0.2)",
                                    },
                                ),
                                rx.button(
                                    "Aceptar todas",
                                    on_click=CookieState.accept_all_cookies,
                                    background=COLORS["primary"],
                                    color="white",
                                    padding="0.7rem 1.5rem",
                                    border_radius="8px",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={
                                        "background": "#2563eb",
                                        "transform": "translateY(-2px)",
                                    },
                                    transition="all 0.2s",
                                ),
                                spacing="3",
                                flex_wrap="wrap",
                            ),
                            
                            spacing="6",
                            align_items="center",
                            padding=["1rem", "1.5rem"],
                            flex_wrap=["wrap", "wrap", "nowrap"],
                        ),
                    ),
                    
                    # Versión expandida (preferencias)
                    rx.cond(
                        CookieState.show_preferences,
                        rx.vstack(
                            rx.hstack(
                                rx.heading(
                                    "🍪 Configuración de Cookies",
                                    size="6",
                                    color="white",
                                ),
                                rx.button(
                                    "✕",
                                    on_click=CookieState.toggle_preferences,
                                    background="transparent",
                                    color="white",
                                    font_size="1.5rem",
                                    cursor="pointer",
                                    padding="0.5rem",
                                    _hover={"color": COLORS["primary"]},
                                ),
                                justify_content="space-between",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            
                            # Cookie esenciales
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            "🔒 Cookies Esenciales",
                                            font_weight="700",
                                            font_size="1rem",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Necesarias para el funcionamiento básico del sitio. No se pueden desactivar.",
                                            font_size="0.9rem",
                                            color="rgba(255,255,255,0.8)",
                                        ),
                                        align_items="start",
                                        flex="1",
                                    ),
                                    rx.switch(
                                        checked=True,
                                        disabled=True,
                                        size="3",
                                    ),
                                    justify_content="space-between",
                                    width="100%",
                                ),
                                padding="1rem",
                                background="rgba(255,255,255,0.05)",
                                border_radius="8px",
                                margin_bottom="0.8rem",
                            ),
                            
                            # Analytics
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            "📊 Cookies Analíticas",
                                            font_weight="700",
                                            font_size="1rem",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Nos ayudan a entender cómo interactúas con nuestro sitio para mejorarlo.",
                                            font_size="0.9rem",
                                            color="rgba(255,255,255,0.8)",
                                        ),
                                        align_items="start",
                                        flex="1",
                                    ),
                                    rx.switch(
                                        checked=CookieState.analytics_cookies,
                                        on_change=CookieState.set_analytics_cookies,
                                        size="3",
                                    ),
                                    justify_content="space-between",
                                    width="100%",
                                ),
                                padding="1rem",
                                background="rgba(255,255,255,0.05)",
                                border_radius="8px",
                                margin_bottom="0.8rem",
                            ),
                            
                            # Marketing
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            "🎯 Cookies de Marketing",
                                            font_weight="700",
                                            font_size="1rem",
                                            color="white",
                                        ),
                                        rx.text(
                                            "Utilizadas para mostrarte contenido y publicidad relevante.",
                                            font_size="0.9rem",
                                            color="rgba(255,255,255,0.8)",
                                        ),
                                        align_items="start",
                                        flex="1",
                                    ),
                                    rx.switch(
                                        checked=CookieState.marketing_cookies,
                                        on_change=CookieState.set_marketing_cookies,
                                        size="3",
                                    ),
                                    justify_content="space-between",
                                    width="100%",
                                ),
                                padding="1rem",
                                background="rgba(255,255,255,0.05)",
                                border_radius="8px",
                                margin_bottom="1.5rem",
                            ),
                            
                            # Botones de acción
                            rx.hstack(
                                rx.button(
                                    "Rechazar todas",
                                    on_click=CookieState.accept_essential_only,
                                    background="transparent",
                                    color="white",
                                    border=f"2px solid rgba(255,255,255,0.3)",
                                    padding="0.7rem 1.5rem",
                                    border_radius="8px",
                                    font_weight="600",
                                    cursor="pointer",
                                ),
                                rx.button(
                                    "Guardar preferencias",
                                    on_click=CookieState.save_preferences,
                                    background=COLORS["primary"],
                                    color="white",
                                    padding="0.7rem 1.5rem",
                                    border_radius="8px",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={
                                        "background": "#2563eb",
                                    },
                                ),
                                spacing="3",
                                justify_content="flex-end",
                                width="100%",
                            ),
                            
                            spacing="3",
                            padding="1.5rem",
                            max_height="70vh",
                            overflow_y="auto",
                        ),
                    ),
                    
                    background="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
                    border_top=f"3px solid {COLORS['primary']}",
                    box_shadow="0 -4px 20px rgba(0,0,0,0.3)",
                    border_radius="12px 12px 0 0",
                ),
                max_width="1200px",
                margin="0 auto",
            ),
            
            position="fixed",
            bottom="0",
            left="0",
            right="0",
            z_index="9999",
            animation="slideUp 0.4s ease-out",
            style={
                "@keyframes slideUp": {
                    "from": {"transform": "translateY(100%)"},
                    "to": {"transform": "translateY(0)"},
                }
            }
        ),
    )
