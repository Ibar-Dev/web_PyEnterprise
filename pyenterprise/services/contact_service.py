"""
Servicios para manejo de contactos
"""

import reflex as rx
from datetime import datetime
from typing import List, Optional
from ..models.contact import Contact
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
        try:
            # Configuración de email (se puede configurar con variables de entorno)
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER", "")
            smtp_password = os.getenv("SMTP_PASSWORD", "")
            to_email = os.getenv("NOTIFICATION_EMAIL", "contacto@pyenterprise.com")
            
            if not smtp_user or not smtp_password:
                print("Configuración de email no encontrada. Saltando notificación.")
                return
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = f"Nuevo contacto desde la web: {contact.name}"
            
            body = f"""
            Nuevo contacto recibido desde la página web:
            
            Nombre: {contact.name}
            Email: {contact.email}
            Empresa: {contact.company}
            Mensaje: {contact.message}
            Fecha: {contact.created_at}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_user, to_email, text)
            server.quit()
            
            print(f"Email de notificación enviado para contacto: {contact.name}")
            
        except Exception as e:
            print(f"Error enviando email de notificación: {e}")
    
    @staticmethod
    def get_contacts_by_status(status: str) -> List[Contact]:
        """Obtener contactos por estado."""
        with rx.session() as session:
            return session.exec(
                rx.select(Contact)
                .where(Contact.status == status)
                .order_by(Contact.created_at.desc())
            ).all()
    
    @staticmethod
    def delete_contact(contact_id: int) -> bool:
        """Eliminar contacto."""
        try:
            with rx.session() as session:
                contact = session.get(Contact, contact_id)
                if contact:
                    session.delete(contact)
                    session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Error eliminando contacto: {e}")
            return False
