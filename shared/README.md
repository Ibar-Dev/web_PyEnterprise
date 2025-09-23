# 🤝 Shared - PyEnterprise

Este módulo contiene recursos compartidos entre frontend y backend: estilos, utilidades, constantes y configuraciones comunes.

## 📁 Estructura

```
shared/
├── styles.py          # Estilos globales de Reflex
├── constants.py       # Constantes de la aplicación
├── utils.py          # Utilidades compartidas
└── config.py         # Configuración global
```

## 🎨 Estilos (`styles.py`)

### Paleta de Colores
```python
COLORS = {
    "primary": "#2563eb",      # Azul empresarial
    "secondary": "#1e40af",    # Azul más oscuro
    "accent": "#3b82f6",       # Azul claro
    "background": "#ffffff",   # Blanco
    "surface": "#f8fafc",      # Gris muy claro
    "text": "#1f2937",         # Gris oscuro
    "text_light": "#6b7280",  # Gris medio
    "border": "#e5e7eb",       # Gris claro
    "success": "#10b981",      # Verde
    "warning": "#f59e0b",      # Naranja
    "error": "#ef4444",        # Rojo
}
```

### Estilos de Componentes
- `base_style`: Estilo base de la aplicación
- `button_primary_style`: Botones principales
- `button_secondary_style`: Botones secundarios
- `card_style`: Tarjetas con sombra
- `navbar_style`: Barra de navegación
- `hero_style`: Sección hero
- `section_style`: Secciones generales
- `container_style`: Contenedores responsivos
- `input_style`: Campos de formulario

### Uso
```python
from shared.styles import COLORS, card_style, section_style

def my_component():
    return rx.box(
        "Contenido",
        **card_style,
        background_color=COLORS["primary"]
    )
```

## 📊 Constantes (`constants.py`)

### Estados de Contacto
```python
CONTACT_STATUS = {
    "PENDING": "pending",
    "REVIEWED": "reviewed", 
    "RESPONDED": "responded"
}

CONTACT_STATUS_LABELS = {
    "pending": "Pendiente",
    "reviewed": "Revisado",
    "responded": "Respondido"
}
```

### Configuración de Email
```python
EMAIL_TEMPLATES = {
    "CONTACT_NOTIFICATION": "contact_notification.html",
    "CONTACT_CONFIRMATION": "contact_confirmation.html"
}
```

### Límites y Validaciones
```python
FIELD_LIMITS = {
    "CONTACT_NAME_MAX": 100,
    "CONTACT_EMAIL_MAX": 150,
    "CONTACT_COMPANY_MAX": 100,
    "CONTACT_MESSAGE_MAX": 2000
}
```

## 🛠️ Utilidades (`utils.py`)

### Validadores
```python
def validate_email(email: str) -> bool:
    """Validar formato de email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str) -> str:
    """Sanitizar entrada de usuario."""
    return text.strip().replace('<', '&lt;').replace('>', '&gt;')
```

### Formatters
```python
def format_date(date: datetime) -> str:
    """Formatear fecha para display."""
    return date.strftime("%d/%m/%Y %H:%M")

def format_phone(phone: str) -> str:
    """Formatear número de teléfono."""
    # Lógica de formateo
    pass
```

### Helpers
```python
def generate_slug(title: str) -> str:
    """Generar slug URL-friendly."""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')
```

## ⚙️ Configuración (`config.py`)

### Variables de Entorno
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pyenterprise.db")
    
    # Email
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # Aplicación
    APP_NAME = os.getenv("APP_NAME", "PyEnterprise")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "change-in-production")
```

## 🎯 Responsive Breakpoints

```python
BREAKPOINTS = {
    "mobile": "768px",
    "tablet": "1024px",
    "desktop": "1200px",
    "xl": "1440px"
}

# Uso en componentes
columns=["1", "2", "3", "4"]  # [mobile, tablet, desktop, xl]
```

## 🔧 Mixins de Estilo

### Animaciones
```python
ANIMATIONS = {
    "fade_in": {
        "animation": "fadeIn 0.5s ease-in-out",
    },
    "slide_up": {
        "animation": "slideUp 0.3s ease-out",
    },
    "bounce": {
        "animation": "bounce 0.6s ease-in-out",
    }
}
```

### Transiciones
```python
TRANSITIONS = {
    "smooth": "all 0.3s ease",
    "fast": "all 0.15s ease",
    "slow": "all 0.5s ease"
}
```

## 📱 Media Queries

```python
def responsive_style(mobile, tablet=None, desktop=None):
    """Crear estilos responsivos."""
    return {
        # Mobile first
        **mobile,
        # Tablet
        f"@media (min-width: {BREAKPOINTS['mobile']})": tablet or {},
        # Desktop  
        f"@media (min-width: {BREAKPOINTS['tablet']})": desktop or {}
    }
```

## 🧪 Testing Utilities

```python
def create_test_contact():
    """Crear contacto de prueba."""
    return {
        "name": "Test User",
        "email": "test@test.com",
        "company": "Test Co",
        "message": "Test message"
    }
```

---
**Shared Resources** - PyEnterprise 🤝
