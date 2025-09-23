"""
Componente Contact Section para PyEnterprise
"""

import reflex as rx
from shared.styles import section_style, container_style, subtitle_style, card_style, input_style, COLORS


class ContactState(rx.State):
    """Estado para manejar el formulario de contacto."""
    name: str = ""
    email: str = ""
    company: str = ""
    message: str = ""
    is_submitted: bool = False
    error_message: str = ""
    
    def submit_form(self):
        """Manejar el envío del formulario."""
        try:
            # Validar campos requeridos
            if not self.name.strip() or not self.email.strip() or not self.message.strip():
                self.error_message = "Por favor, completa todos los campos obligatorios."
                return
            
            # Por ahora, simplemente simular el envío exitoso
            print(f"Formulario enviado: {self.name}, {self.email}, {self.company}")
            print(f"Mensaje: {self.message}")
            
            self.is_submitted = True
            self.error_message = ""
            
        except Exception as e:
            self.error_message = f"Error al enviar el mensaje: {str(e)}"
            print(f"Error en submit_form: {e}")
        
    def reset_form(self):
        """Resetear el formulario."""
        self.name = ""
        self.email = ""
        self.company = ""
        self.message = ""
        self.is_submitted = False
        self.error_message = ""


def contact_info_item(icon: str, title: str, content: str, link: str = None) -> rx.Component:
    """Item de información de contacto."""
    item_content = rx.vstack(
        rx.icon(tag=icon, size="24px", color=COLORS["primary"]),
        rx.heading(title, size="sm", color=COLORS["text"], margin_bottom="0.5rem"),
        rx.text(content, color=COLORS["text_light"], text_align="center"),
        align_items="center",
        spacing="3",
    )
    
    if link:
        return rx.link(
            item_content,
            href=link,
            _hover={"text_decoration": "none"},
        )
    return item_content


def contact_section() -> rx.Component:
    """Sección de contacto con formulario e información."""
    return rx.box(
        rx.container(
            # Título de la sección
            rx.heading(
                "Contáctanos",
                **subtitle_style,
                margin_bottom="1rem",
            ),
            
            rx.text(
                "¿Listo para comenzar tu proyecto? Estamos aquí para ayudarte",
                font_size="1.2rem",
                color=COLORS["text_light"],
                text_align="center",
                margin_bottom="4rem",
            ),
            
            rx.grid(
                # Columna izquierda - Información de contacto
                rx.vstack(
                    rx.heading(
                        "Información de Contacto",
                        size="lg",
                        color=COLORS["text"],
                        margin_bottom="2rem",
                    ),
                    
                    rx.vstack(
                        contact_info_item(
                            icon="email",
                            title="Email",
                            content="contacto@pyenterprise.com",
                            link="mailto:contacto@pyenterprise.com"
                        ),
                        
                        contact_info_item(
                            icon="phone",
                            title="Teléfono",
                            content="+34 900 123 456",
                            link="tel:+34900123456"
                        ),
                        
                        contact_info_item(
                            icon="location_on",
                            title="Ubicación",
                            content="Madrid, España"
                        ),
                        
                        contact_info_item(
                            icon="schedule",
                            title="Horario",
                            content="Lun - Vie: 9:00 - 18:00"
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    
                    # Redes sociales
                    rx.box(
                        rx.heading(
                            "Síguenos",
                            size="md",
                            color=COLORS["text"],
                            margin_bottom="1rem",
                        ),
                        rx.hstack(
                            rx.link(
                                rx.icon(tag="fab fa-linkedin", size="24px"),
                                href="https://linkedin.com/company/pyenterprise",
                                color=COLORS["primary"],
                                _hover={"color": COLORS["secondary"]},
                            ),
                            rx.link(
                                rx.icon(tag="fab fa-github", size="24px"),
                                href="https://github.com/pyenterprise",
                                color=COLORS["primary"],
                                _hover={"color": COLORS["secondary"]},
                            ),
                            rx.link(
                                rx.icon(tag="fab fa-twitter", size="24px"),
                                href="https://twitter.com/pyenterprise",
                                color=COLORS["primary"],
                                _hover={"color": COLORS["secondary"]},
                            ),
                            spacing="4",
                            justify_content="center",
                        ),
                        margin_top="2rem",
                        text_align="center",
                    ),
                    
                    align_items="start",
                    spacing="6",
                ),
                
                # Columna derecha - Formulario de contacto
                rx.box(
                    rx.cond(
                        ContactState.is_submitted,
                        # Mensaje de éxito
                        rx.vstack(
                            rx.icon(tag="check_circle", size="64px", color=COLORS["success"]),
                            rx.heading(
                                "¡Mensaje enviado!",
                                size="lg",
                                color=COLORS["success"],
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Gracias por contactarnos. Te responderemos pronto.",
                                color=COLORS["text_light"],
                                text_align="center",
                                margin_bottom="2rem",
                            ),
                            rx.button(
                                "Enviar otro mensaje",
                                on_click=ContactState.reset_form,
                                background_color=COLORS["primary"],
                                color="white",
                                padding="12px 24px",
                                border_radius="8px",
                            ),
                            align_items="center",
                            spacing="4",
                            padding="3rem",
                        ),
                        # Formulario
                        rx.form(
                            rx.vstack(
                                rx.heading(
                                    "Envíanos un mensaje",
                                    size="lg",
                                    color=COLORS["text"],
                                    margin_bottom="1.5rem",
                                ),
                                
                                # Mensaje de error si existe
                                rx.cond(
                                    ContactState.error_message != "",
                                    rx.box(
                                        rx.text(
                                            ContactState.error_message,
                                            color=COLORS["error"],
                                            font_weight="500",
                                        ),
                                        background_color="#fef2f2",
                                        border=f"1px solid {COLORS['error']}",
                                        border_radius="8px",
                                        padding="12px",
                                        margin_bottom="1rem",
                                    ),
                                    rx.box(),
                                ),
                                
                                rx.input(
                                    placeholder="Tu nombre *",
                                    value=ContactState.name,
                                    on_change=ContactState.set_name,
                                    required=True,
                                    **input_style,
                                ),
                                
                                rx.input(
                                    type="email",
                                    placeholder="Tu email *",
                                    value=ContactState.email,
                                    on_change=ContactState.set_email,
                                    required=True,
                                    **input_style,
                                ),
                                
                                rx.input(
                                    placeholder="Empresa",
                                    value=ContactState.company,
                                    on_change=ContactState.set_company,
                                    **input_style,
                                ),
                                
                                rx.text_area(
                                    placeholder="Describe tu proyecto o consulta *",
                                    value=ContactState.message,
                                    on_change=ContactState.set_message,
                                    required=True,
                                    rows="5",
                                    **input_style,
                                    resize="vertical",
                                ),
                                
                                rx.button(
                                    "Enviar Mensaje",
                                    type="submit",
                                    background_color=COLORS["primary"],
                                    color="white",
                                    font_weight="600",
                                    padding="16px 32px",
                                    border_radius="8px",
                                    width="100%",
                                    font_size="1.1rem",
                                    _hover={
                                        "background_color": COLORS["secondary"],
                                        "transform": "translateY(-2px)",
                                    },
                                    transition="all 0.3s ease",
                                ),
                                
                                spacing="4",
                                width="100%",
                            ),
                            on_submit=ContactState.submit_form,
                            width="100%",
                        ),
                    ),
                    **card_style,
                ),
                
                columns=["1", "1", "2", "2"],  # Responsive
                spacing="8",
                align_items="start",
            ),
            
            **container_style,
        ),
        id="contacto",
        background_color=COLORS["surface"],
        **section_style,
    )
