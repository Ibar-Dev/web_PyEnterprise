"""
Configuración de la aplicación PyEnterprise
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración general de la aplicación."""
    
    # Base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pyenterprise.db")
    
    # Email
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "contacto@pyenterprise.com")
    
    # Aplicación
    APP_NAME = os.getenv("APP_NAME", "PyEnterprise")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-en-produccion")
    
    # URLs
    DOMAIN = os.getenv("DOMAIN", "localhost:3000")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Configuración de Reflex
    REFLEX_DB_URL = DATABASE_URL
