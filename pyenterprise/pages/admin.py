"""
Panel de administración para PyEnterprise
"""

import reflex as rx
from typing import List
from ..models.contact import Contact
from ..services.contact_service import ContactService
from ..styles import COLORS, container_style, card_style


class AdminState(rx.State):
    """Estado para el panel de administración."""
    contacts: List[Contact] = []
    selected_contact: Contact = None
    
    def load_contacts(self):
        """Cargar todos los contactos."""
        self.contacts = ContactService.get_all_contacts()
    
    def select_contact(self, contact_id: int):
        """Seleccionar un contacto específico."""
        self.selected_contact = ContactService.get_contact_by_id(contact_id)
    
    def update_status(self, contact_id: int, status: str):
        """Actualizar estado del contacto."""
        if ContactService.update_contact_status(contact_id, status):
            self.load_contacts()  # Recargar lista
            if self.selected_contact and self.selected_contact.id == contact_id:
                self.selected_contact.status = status
    
    def delete_contact(self, contact_id: int):
        """Eliminar contacto."""
        if ContactService.delete_contact(contact_id):
            self.load_contacts()  # Recargar lista
            if self.selected_contact and self.selected_contact.id == contact_id:
                self.selected_contact = None


def contact_row(contact: Contact) -> rx.Component:
    """Fila de contacto en la tabla."""
    status_color = {
        "pending": COLORS["warning"],
        "reviewed": COLORS["primary"],
        "responded": COLORS["success"]
    }.get(contact.status, COLORS["text_light"])
    
    return rx.tr(
        rx.td(contact.name, padding="12px"),
        rx.td(contact.email, padding="12px"),
        rx.td(contact.company or "-", padding="12px"),
        rx.td(
            rx.badge(
                contact.status,
                background_color=status_color,
                color="white",
                padding="4px 8px",
                border_radius="4px",
            ),
            padding="12px"
        ),
        rx.td(
            contact.created_at.strftime("%d/%m/%Y %H:%M") if contact.created_at else "-",
            padding="12px"
        ),
        rx.td(
            rx.hstack(
                rx.button(
                    "Ver",
                    on_click=AdminState.select_contact(contact.id),
                    size="sm",
                    background_color=COLORS["primary"],
                    color="white",
                ),
                rx.select(
                    ["pending", "reviewed", "responded"],
                    value=contact.status,
                    on_change=lambda status: AdminState.update_status(contact.id, status),
                    size="sm",
                ),
                rx.button(
                    "Eliminar",
                    on_click=AdminState.delete_contact(contact.id),
                    size="sm",
                    background_color=COLORS["error"],
                    color="white",
                ),
                spacing="2",
            ),
            padding="12px"
        ),
        _hover={"background_color": COLORS["surface"]},
    )


def contact_detail() -> rx.Component:
    """Panel de detalle del contacto seleccionado."""
    return rx.cond(
        AdminState.selected_contact,
        rx.box(
            rx.heading(
                "Detalle del Contacto",
                size="lg",
                margin_bottom="1rem",
                color=COLORS["text"],
            ),
            rx.vstack(
                rx.hstack(
                    rx.text("Nombre:", font_weight="600"),
                    rx.text(AdminState.selected_contact.name),
                    spacing="2",
                ),
                rx.hstack(
                    rx.text("Email:", font_weight="600"),
                    rx.text(AdminState.selected_contact.email),
                    spacing="2",
                ),
                rx.hstack(
                    rx.text("Empresa:", font_weight="600"),
                    rx.text(AdminState.selected_contact.company or "No especificada"),
                    spacing="2",
                ),
                rx.hstack(
                    rx.text("Estado:", font_weight="600"),
                    rx.badge(
                        AdminState.selected_contact.status,
                        background_color=COLORS["primary"],
                        color="white",
                    ),
                    spacing="2",
                ),
                rx.hstack(
                    rx.text("Fecha:", font_weight="600"),
                    rx.text(AdminState.selected_contact.created_at.strftime("%d/%m/%Y %H:%M")),
                    spacing="2",
                ),
                rx.vstack(
                    rx.text("Mensaje:", font_weight="600"),
                    rx.box(
                        rx.text(AdminState.selected_contact.message),
                        background_color=COLORS["surface"],
                        padding="1rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS['border']}",
                    ),
                    align_items="start",
                    width="100%",
                    spacing="2",
                ),
                align_items="start",
                spacing="4",
                width="100%",
            ),
            **card_style,
        ),
        rx.box(
            rx.text(
                "Selecciona un contacto para ver los detalles",
                color=COLORS["text_light"],
                text_align="center",
                font_style="italic",
            ),
            padding="2rem",
        ),
    )


def admin_dashboard() -> rx.Component:
    """Dashboard principal de administración."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading(
                        "Panel de Administración - PyEnterprise",
                        size="xl",
                        color=COLORS["text"],
                    ),
                    rx.button(
                        "Recargar Contactos",
                        on_click=AdminState.load_contacts,
                        background_color=COLORS["primary"],
                        color="white",
                    ),
                    justify_content="space-between",
                    align_items="center",
                    width="100%",
                    margin_bottom="2rem",
                ),
                
                # Estadísticas rápidas
                rx.grid(
                    rx.box(
                        rx.heading(str(len(AdminState.contacts)), size="lg", color=COLORS["primary"]),
                        rx.text("Total Contactos", color=COLORS["text_light"]),
                        text_align="center",
                        **card_style,
                        padding="1.5rem",
                    ),
                    rx.box(
                        rx.heading(
                            str(len([c for c in AdminState.contacts if c.status == "pending"])),
                            size="lg",
                            color=COLORS["warning"]
                        ),
                        rx.text("Pendientes", color=COLORS["text_light"]),
                        text_align="center",
                        **card_style,
                        padding="1.5rem",
                    ),
                    rx.box(
                        rx.heading(
                            str(len([c for c in AdminState.contacts if c.status == "reviewed"])),
                            size="lg",
                            color=COLORS["primary"]
                        ),
                        rx.text("Revisados", color=COLORS["text_light"]),
                        text_align="center",
                        **card_style,
                        padding="1.5rem",
                    ),
                    rx.box(
                        rx.heading(
                            str(len([c for c in AdminState.contacts if c.status == "responded"])),
                            size="lg",
                            color=COLORS["success"]
                        ),
                        rx.text("Respondidos", color=COLORS["text_light"]),
                        text_align="center",
                        **card_style,
                        padding="1.5rem",
                    ),
                    columns="4",
                    spacing="4",
                    margin_bottom="2rem",
                ),
                
                # Layout principal
                rx.grid(
                    # Tabla de contactos
                    rx.box(
                        rx.heading(
                            "Lista de Contactos",
                            size="lg",
                            margin_bottom="1rem",
                            color=COLORS["text"],
                        ),
                        rx.box(
                            rx.table(
                                rx.thead(
                                    rx.tr(
                                        rx.th("Nombre", padding="12px"),
                                        rx.th("Email", padding="12px"),
                                        rx.th("Empresa", padding="12px"),
                                        rx.th("Estado", padding="12px"),
                                        rx.th("Fecha", padding="12px"),
                                        rx.th("Acciones", padding="12px"),
                                    ),
                                    background_color=COLORS["surface"],
                                ),
                                rx.tbody(
                                    rx.foreach(
                                        AdminState.contacts,
                                        contact_row,
                                    ),
                                ),
                                width="100%",
                                border=f"1px solid {COLORS['border']}",
                                border_radius="8px",
                            ),
                            overflow_x="auto",
                        ),
                        **card_style,
                    ),
                    
                    # Panel de detalle
                    contact_detail(),
                    
                    columns="2",  # Responsive
                    spacing="6",
                ),
                
                spacing="6",
                width="100%",
            ),
            **container_style,
        ),
        padding="2rem 0",
        on_mount=AdminState.load_contacts,  # Cargar contactos al montar
    )
