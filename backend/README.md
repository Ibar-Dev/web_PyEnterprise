# 🔧 Backend - PyEnterprise

Este módulo contiene toda la lógica de negocio, servicios y APIs del backend.

## 📁 Estructura

```
backend/
├── services/           # Servicios de negocio
│   ├── contact_service.py    # Gestión de contactos
│   ├── email_service.py      # Envío de emails (futuro)
│   └── analytics_service.py  # Analíticas (futuro)
├── api/               # Endpoints REST (futuro) 
│   ├── contacts.py    # API de contactos
│   └── services.py    # API de servicios
└── utils/             # Utilidades del backend
    ├── validators.py  # Validadores
    └── helpers.py     # Funciones auxiliares
```

## 🛠️ Servicios

### ContactService (`contact_service.py`)
Maneja todas las operaciones relacionadas con contactos.

#### Métodos:
- `create_contact()`: Crear nuevo contacto
- `get_all_contacts()`: Obtener todos los contactos
- `get_contact_by_id()`: Obtener contacto específico
- `update_contact_status()`: Actualizar estado
- `delete_contact()`: Eliminar contacto
- `send_notification_email()`: Enviar notificación

#### Ejemplo de Uso:
```python
from backend.services.contact_service import ContactService

# Crear contacto
contact = ContactService.create_contact(
    name="Juan Pérez",
    email="juan@empresa.com",
    company="Mi Empresa",
    message="Necesito una consulta"
)

# Obtener todos los contactos
contacts = ContactService.get_all_contacts()
```

## 📧 Sistema de Emails

### Configuración
Las credenciales de email se configuran via variables de entorno:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-password-de-app
NOTIFICATION_EMAIL=contacto@pyenterprise.com
```

### Funcionalidades
- ✅ Notificación automática al recibir contacto
- 🚧 Email de confirmación al cliente
- 🚧 Templates HTML personalizados
- 🚧 Adjuntos automáticos

## 🔒 Validaciones

### Contactos
- Campos requeridos: `name`, `email`, `message`
- Validación de formato de email
- Longitud máxima de campos
- Sanitización de inputs

## 📊 Estados de Contacto

```python
CONTACT_STATUS = {
    "pending": "Pendiente de revisión",
    "reviewed": "Revisado por el equipo",
    "responded": "Respondido al cliente"
}
```

## 🔄 Flujo de Datos

```
Frontend Form → ContactState → ContactService → Database
                     ↓
              Email Notification → SMTP Server
```

## 🚀 API Endpoints (Futuro)

```
POST   /api/contacts          # Crear contacto
GET    /api/contacts          # Listar contactos
GET    /api/contacts/{id}     # Obtener contacto
PUT    /api/contacts/{id}     # Actualizar contacto
DELETE /api/contacts/{id}     # Eliminar contacto
```

## 🧪 Testing

```python
# Ejemplo de test unitario
def test_create_contact():
    contact = ContactService.create_contact(
        name="Test User",
        email="test@test.com",
        company="Test Co",
        message="Test message"
    )
    assert contact.name == "Test User"
    assert contact.status == "pending"
```

## 🛡️ Seguridad

- Validación de inputs
- Sanitización de datos
- Rate limiting (futuro)
- Autenticación JWT (para admin)

## 📈 Métricas

- Número de contactos por día
- Tasa de respuesta
- Tiempo promedio de respuesta
- Conversión de leads

---
**Backend Team** - PyEnterprise ⚙️
