"""
Configuración de Seguridad para PyLink
Headers de seguridad, CSP, CORS, etc.
"""

# Headers de seguridad HTTP
SECURITY_HEADERS = {
    # Content Security Policy - Protege contra XSS
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https: blob:; "
        "connect-src 'self' https://api.pylink.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    ),
    
    # HSTS - Fuerza HTTPS
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    
    # Previene clickjacking
    "X-Frame-Options": "DENY",
    
    # Previene MIME-sniffing
    "X-Content-Type-Options": "nosniff",
    
    # Referrer Policy
    "Referrer-Policy": "strict-origin-when-cross-origin",
    
    # Permissions Policy (antes Feature Policy)
    "Permissions-Policy": (
        "geolocation=(), "
        "microphone=(), "
        "camera=(), "
        "payment=(), "
        "usb=(), "
        "magnetometer=()"
    ),
    
    # Cross-Origin Policies
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
}


# Configuración CORS
CORS_CONFIG = {
    "allow_origins": [
        "https://pylink.com",
        "https://www.pylink.com",
    ],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": [
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    "max_age": 3600,  # 1 hora
}


# Rate Limiting - Previene ataques de fuerza bruta
RATE_LIMIT_CONFIG = {
    "default": "100/hour",  # Límite general
    "contact_form": "5/hour",  # Formulario de contacto
    "api": "1000/hour",  # Endpoints API
}


# Configuración de sesiones seguras
SESSION_CONFIG = {
    "cookie_secure": True,  # Solo HTTPS
    "cookie_httponly": True,  # No accesible desde JavaScript
    "cookie_samesite": "Strict",  # Protección CSRF
    "session_lifetime": 3600,  # 1 hora
    "regenerate_on_login": True,  # Regenerar ID de sesión
}


# Lista negra de IPs (ejemplo - usar base de datos real)
IP_BLACKLIST = [
    # "192.168.1.100",  # Ejemplo
]


# Validación de inputs
INPUT_VALIDATION = {
    "email": {
        "max_length": 254,
        "pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    },
    "phone": {
        "max_length": 20,
        "pattern": r'^\+?[0-9\s\-\(\)]+$',
    },
    "name": {
        "max_length": 100,
        "pattern": r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\'-]+$',
    },
    "message": {
        "max_length": 5000,
        "min_length": 10,
    },
}


# Configuración de logging de seguridad
SECURITY_LOGGING = {
    "log_failed_logins": True,
    "log_suspicious_activity": True,
    "log_file": "security.log",
    "alert_threshold": 5,  # Alertar después de 5 intentos fallidos
}


def sanitize_input(text: str, input_type: str = "default") -> str:
    """
    Sanitiza input del usuario para prevenir XSS e inyecciones.
    
    Args:
        text: Texto a sanitizar
        input_type: Tipo de input (email, name, message, etc.)
    
    Returns:
        Texto sanitizado
    """
    import html
    import re
    
    # Escape HTML básico
    text = html.escape(text)
    
    # Remover caracteres peligrosos
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', '[', ']']
    for char in dangerous_chars:
        if char not in ['@', '.', '+', '-']:  # Permitir en emails
            text = text.replace(char, '')
    
    # Validar según tipo
    if input_type in INPUT_VALIDATION:
        config = INPUT_VALIDATION[input_type]
        
        # Longitud
        if 'max_length' in config:
            text = text[:config['max_length']]
        
        # Patrón
        if 'pattern' in config and not re.match(config['pattern'], text):
            return ""
    
    return text.strip()


def validate_csrf_token(token: str, session_token: str) -> bool:
    """
    Valida token CSRF contra ataques.
    
    Args:
        token: Token recibido
        session_token: Token de sesión
    
    Returns:
        True si es válido
    """
    import secrets
    return secrets.compare_digest(token, session_token)


def generate_csrf_token() -> str:
    """
    Genera un token CSRF seguro.
    
    Returns:
        Token aleatorio
    """
    import secrets
    return secrets.token_urlsafe(32)


def is_ip_blacklisted(ip: str) -> bool:
    """
    Verifica si una IP está en la lista negra.
    
    Args:
        ip: Dirección IP
    
    Returns:
        True si está bloqueada
    """
    return ip in IP_BLACKLIST


def log_security_event(event_type: str, details: dict):
    """
    Registra evento de seguridad.
    
    Args:
        event_type: Tipo de evento (failed_login, suspicious_activity, etc.)
        details: Detalles del evento
    """
    import logging
    from datetime import datetime
    
    logger = logging.getLogger('security')
    logger.warning(f"[{datetime.now()}] {event_type}: {details}")
