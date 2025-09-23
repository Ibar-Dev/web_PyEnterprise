"""
Servicios para manejo de contactos
"""

import reflex as rx
from datetime import datetime
from typing import List, Optional
from database.models import Contact
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class ContactService:
    """Servicio para manejo de contactos."""
    
    @staticmethod
    def create_contact(name: str, email: str, company: str, message: str) -> Contact:
        """Crear un nuevo contacto."""
        try:
            with rx.session() as session:
                contact = Contact(
                    name=name,
                    email=email,
                    company=company,
                    message=message,
                    created_at=datetime.now(),
                    status="pending"
                )
                session.add(contact)
                session.commit()
                session.refresh(contact)
                
                # Enviar notificación por email (opcional)
                ContactService.send_notification_email(contact)
                
                return contact
        except Exception as e:
            print(f"Error creando contacto: {e}")
            raise e
    
    @staticmethod
    def get_all_contacts() -> List[Contact]:
        """Obtener todos los contactos."""
        with rx.session() as session:
            return session.exec(rx.select(Contact).order_by(Contact.created_at.desc())).all()
    
    @staticmethod
    def get_contact_by_id(contact_id: int) -> Optional[Contact]:
        """Obtener contacto por ID."""
        with rx.session() as session:
            return session.get(Contact, contact_id)
    
    @staticmethod
    def update_contact_status(contact_id: int, status: str) -> bool:
        """Actualizar estado del contacto."""
        try:
            with rx.session() as session:
                contact = session.get(Contact, contact_id)
                if contact:
                    contact.status = status
                    session.add(contact)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Error actualizando contacto: {e}")
            return False
    
    @staticmethod
    def send_notification_email(contact: Contact):
        """Enviar email de notificación (configuración opcional)."""
        print(f"📧 Simulando envío de email para contacto: {contact.name}")
        # Aquí se implementaría el envío real de emails
