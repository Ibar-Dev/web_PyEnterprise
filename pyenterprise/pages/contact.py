"""
Página de Contacto - Formulario para solicitar servicios
"""

import reflex as rx
from ..styles import COLORS


class ContactState(rx.State):
    """Estado para el formulario de contacto."""
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    empresa: str = ""
    servicio: str = ""
    mensaje: str = ""
    form_submitted: bool = False
    
    @rx.var
    def servicio_inicial(self) -> str:
        """Obtiene el servicio desde la URL."""
        # Obtener parámetros de query de la URL
        params = self.router.page.params if hasattr(self.router.page, 'params') else {}
        servicio_param = params.get("servicio", "")
        if servicio_param and servicio_param in SERVICIOS_MAP:
            return SERVICIOS_MAP[servicio_param]
        return ""
    
    def set_nombre(self, value: str):
        """Setter para nombre."""
        self.nombre = value
    
    def set_email(self, value: str):
        """Setter para email."""
        self.email = value
    
    def set_telefono(self, value: str):
        """Setter para teléfono."""
        self.telefono = value
    
    def set_empresa(self, value: str):
        """Setter para empresa."""
        self.empresa = value
    
    def set_servicio(self, value: str):
        """Setter para servicio."""
        self.servicio = value
    
    def set_mensaje(self, value: str):
        """Setter para mensaje."""
        self.mensaje = value
    
    def handle_submit(self):
        """Maneja el envío del formulario."""
        if self.nombre and self.email and self.mensaje:
            # Aquí iría la lógica para enviar el email
            self.form_submitted = True
            # Resetear formulario después de 3 segundos
            yield
        
    def reset_form(self):
        """Resetea el formulario."""
        self.nombre = ""
        self.email = ""
        self.telefono = ""
        self.empresa = ""
        self.servicio = ""
        self.mensaje = ""
        self.form_submitted = False


# Mapeo de servicios para mostrar en el formulario
SERVICIOS_MAP = {
    "web-corporativo": "Sitios Web Corporativos",
    "ecommerce": "E-commerce",
    "portal-web": "Portales Web",
    "landing-page": "Landing Pages",
    "app-nativa": "Apps iOS & Android",
    "app-multiplataforma": "Apps Multiplataforma",
    "pwa": "Apps Web Progresivas",
    "app-gestion": "Apps de Gestión",
    "software-escritorio": "Sistemas de Escritorio",
    "automatizacion": "Automatización de Procesos",
    "ia": "Inteligencia Artificial",
    "apis": "APIs y Integraciones",
    "ui-ux": "Diseño UI/UX",
    "consultoria": "Consultoría Tecnológica",
    "mantenimiento": "Mantenimiento y Soporte",
    "cloud-devops": "Cloud & DevOps",
    "consulta-general": "Consulta General",
}


def contact_page() -> rx.Component:
    """Página de contacto con formulario."""
    return rx.box(
        # Navbar spacing
        rx.box(height="80px"),
        
        rx.container(
            rx.vstack(
                # Header moderno
                rx.vstack(
                    # Badge
                    rx.box(
                        rx.text(
                            "💬 Contáctanos",
                            color=COLORS["primary"],
                            font_weight="600",
                            font_size="0.9rem",
                            letter_spacing="1px",
                        ),
                        padding="8px 20px",
                        background="rgba(59, 130, 246, 0.1)",
                        border=f"1px solid {COLORS['primary']}",
                        border_radius="50px",
                        margin_bottom="1.5rem",
                    ),
                    # Título con gradiente
                    rx.heading(
                        "Hablemos de tu Proyecto",
                        size="9",
                        color="white",
                        font_weight="900",
                        text_align="center",
                        background=f"linear-gradient(135deg, white, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        margin_bottom="1rem",
                        letter_spacing="-1px",
                        line_height="1.2",
                        padding_bottom="0.5rem",
                    ),
                    # Subtítulo
                    rx.text(
                        "Cuéntanos tu idea y te ayudaremos a convertirla en realidad",
                        font_size="1.25rem",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                        margin_bottom="1rem",
                        max_width="600px",
                        line_height="1.6",
                    ),
                    # Línea decorativa
                    rx.box(
                        width="80px",
                        height="4px",
                        background=f"linear-gradient(90deg, transparent, {COLORS['primary']}, transparent)",
                        border_radius="2px",
                        margin_bottom="3rem",
                    ),
                    align_items="center",
                    width="100%",
                ),
                
                # Contenedor principal
                rx.grid(
                    # Formulario
                    rx.box(
                        rx.cond(
                            ContactState.form_submitted,
                            # Mensaje de éxito
                            rx.vstack(
                                rx.box(
                                    rx.text(
                                        "✓",
                                        font_size="4rem",
                                        color="#22c55e",
                                        text_align="center",
                                    ),
                                ),
                                rx.heading(
                                    "¡Mensaje Enviado!",
                                    size="6",
                                    color="white",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Gracias por contactarnos. Nos pondremos en contacto contigo pronto.",
                                    color="rgba(255, 255, 255, 0.8)",
                                    text_align="center",
                                    margin_bottom="2rem",
                                ),
                                rx.button(
                                    "Enviar otro mensaje",
                                    on_click=ContactState.reset_form,
                                    background=COLORS["primary"],
                                    color="white",
                                    padding="12px 24px",
                                    border_radius="8px",
                                    cursor="pointer",
                                    _hover={
                                        "background": "#2563eb",
                                    },
                                ),
                                align_items="center",
                                spacing="3",
                                padding="3rem",
                            ),
                        ),
                        rx.cond(
                            ~ContactState.form_submitted,
                            # Formulario
                            rx.vstack(
                                # Nombre
                                rx.vstack(
                                    rx.text(
                                        "Nombre Completo *",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.input(
                                        placeholder="Tu nombre",
                                        value=ContactState.nombre,
                                        on_change=ContactState.set_nombre,
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        height="52px",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Email
                                rx.vstack(
                                    rx.text(
                                        "Email *",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.input(
                                        placeholder="tu@email.com",
                                        value=ContactState.email,
                                        on_change=ContactState.set_email,
                                        type_="email",
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        height="52px",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Teléfono
                                rx.vstack(
                                    rx.text(
                                        "Teléfono",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.input(
                                        placeholder="+34 900 123 456",
                                        value=ContactState.telefono,
                                        on_change=ContactState.set_telefono,
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        height="52px",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Empresa
                                rx.vstack(
                                    rx.text(
                                        "Empresa",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.input(
                                        placeholder="Nombre de tu empresa",
                                        value=ContactState.empresa,
                                        on_change=ContactState.set_empresa,
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        height="52px",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Servicio
                                rx.vstack(
                                    rx.text(
                                        "Servicio de Interés",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.input(
                                        placeholder="Selecciona un servicio",
                                        value=rx.cond(
                                            ContactState.servicio != "",
                                            ContactState.servicio,
                                            ContactState.servicio_inicial,
                                        ),
                                        on_change=ContactState.set_servicio,
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        height="52px",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                        read_only=False,
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Mensaje
                                rx.vstack(
                                    rx.text(
                                        "Cuéntanos sobre tu proyecto *",
                                        color="white",
                                        font_weight="600",
                                        font_size="0.95rem",
                                    ),
                                    rx.text_area(
                                        placeholder="Describe tu proyecto, necesidades y objetivos...",
                                        value=ContactState.mensaje,
                                        on_change=ContactState.set_mensaje,
                                        width="100%",
                                        max_width=["100%", "100%", "100%", "100%"],
                                        min_height="180px",
                                        padding="14px 16px",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS['primary']}",
                                        background="rgba(255, 255, 255, 0.05)",
                                        color="white",
                                        font_size="1rem",
                                        _placeholder={"color": "rgba(255, 255, 255, 0.5)"},
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Botón enviar
                                rx.button(
                                    rx.hstack(
                                        rx.icon(tag="send", margin_right="8px"),
                                        rx.text("Enviar Mensaje"),
                                        align_items="center",
                                    ),
                                    on_click=ContactState.handle_submit,
                                    background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                                    color="white",
                                    font_weight="700",
                                    padding="14px 28px",
                                    border_radius="8px",
                                    width="100%",
                                    cursor="pointer",
                                    _hover={
                                        "transform": "translateY(-2px)",
                                        "box_shadow": "0 10px 25px rgba(59, 130, 246, 0.4)",
                                    },
                                    transition="all 0.3s ease",
                                ),
                                
                                spacing="4",
                                width="100%",
                                align_items="stretch",
                            ),
                        ),
                        padding=["1rem", "1.5rem", "1.5rem", "2rem"],
                        background="rgba(30, 41, 59, 0.8)",
                        border_radius="16px",
                        border=f"2px solid {COLORS['primary']}",
                    ),
                    
                    # Información de contacto
                    rx.vstack(
                        rx.heading(
                            "Información de Contacto",
                            size="6",
                            color="white",
                            font_weight="700",
                            margin_bottom="2rem",
                        ),
                        
                        # Email
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="mail", font_size="1.5rem", color=COLORS["primary"]),
                                width="40px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Email",
                                    color="white",
                                    font_weight="600",
                                ),
                                rx.link(
                                    "hola@pylink.dev",
                                    href="mailto:hola@pylink.dev",
                                    color=COLORS["primary"],
                                    text_decoration="none",
                                    _hover={"text_decoration": "underline"},
                                ),
                                spacing="1",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        
                        # Teléfono
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="phone", font_size="1.5rem", color=COLORS["primary"]),
                                width="40px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Teléfono",
                                    color="white",
                                    font_weight="600",
                                ),
                                rx.link(
                                    "+34 900 123 456",
                                    href="tel:+34900123456",
                                    color=COLORS["primary"],
                                    text_decoration="none",
                                    _hover={"text_decoration": "underline"},
                                ),
                                spacing="1",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        
                        # WhatsApp
                        rx.hstack(
                            rx.box(
                                rx.html('<i class="fab fa-whatsapp"></i>'),
                                width="40px",
                                font_size="1.5rem",
                                color="#25D366",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "WhatsApp",
                                    color="white",
                                    font_weight="600",
                                ),
                                rx.link(
                                    "Enviar mensaje",
                                    href="https://wa.me/34900123456?text=Hola,%20me%20interesa%20conocer%20m%C3%A1s%20sobre%20sus%20servicios",
                                    color=COLORS["primary"],
                                    text_decoration="none",
                                    _hover={"text_decoration": "underline"},
                                    is_external=True,
                                ),
                                spacing="1",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        
                        # Ubicación
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="map_pin", font_size="1.5rem", color=COLORS["primary"]),
                                width="40px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Ubicación",
                                    color="white",
                                    font_weight="600",
                                ),
                                rx.text(
                                    "Madrid, España",
                                    color="rgba(255, 255, 255, 0.8)",
                                ),
                                spacing="1",
                            ),
                            spacing="3",
                            align_items="start",
                        ),
                        
                        # Horario
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Horario de Atención",
                                    color="white",
                                    font_weight="600",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "Lunes - Viernes: 9:00 - 18:00",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_size="0.9rem",
                                ),
                                rx.text(
                                    "Sábado - Domingo: Cerrado",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_size="0.9rem",
                                ),
                                spacing="1",
                            ),
                            padding="1.5rem",
                            background="rgba(59, 130, 246, 0.1)",
                            border_radius="8px",
                            border=f"1px solid {COLORS['primary']}",
                            margin_top="1rem",
                        ),
                        
                        padding=["1rem", "1.5rem", "1.5rem", "2rem"],
                        background="rgba(30, 41, 59, 0.8)",
                        border_radius="16px",
                        border=f"2px solid {COLORS['primary']}",
                        spacing="4",
                        height="fit-content",
                    ),
                    
                    template_columns=["1fr", "1fr", "1fr 1fr", "1fr 1fr"],
                    gap=["4", "4", "6", "6"],
                    width="100%",
                ),
                
                spacing="6",
                padding=["2rem 1rem", "3rem 1.5rem", "6rem 2rem", "6rem 2rem"],
            ),
            max_width="1200px",
            margin="0 auto",
        ),
        
        min_height="100vh",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )
