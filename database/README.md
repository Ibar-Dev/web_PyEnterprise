# 🗄️ Database - PyEnterprise

Este módulo contiene todos los modelos de datos, migraciones y configuración de la base de datos.

## 📁 Estructura

```
database/
├── models.py          # Modelos de datos (SQLAlchemy)
├── migrations/        # Migraciones de BD (futuro)
├── seeders/          # Datos de prueba (futuro)
├── config.py         # Configuración de BD
└── utils.py          # Utilidades de BD
```

## 📊 Modelos de Datos

### Contact
Almacena información de contactos de clientes.

```python
class Contact(rx.Model, table=True):
    id: Optional[int] = None
    name: str                    # Nombre del contacto
    email: str                   # Email del contacto
    company: Optional[str] = ""  # Empresa (opcional)
    message: str                 # Mensaje del contacto
    created_at: datetime         # Fecha de creación
    status: str = "pending"      # Estado: pending, reviewed, responded
```

#### Estados:
- `pending`: Pendiente de revisión
- `reviewed`: Revisado por el equipo
- `responded`: Respondido al cliente

### Service
Catálogo de servicios ofrecidos.

```python
class Service(rx.Model, table=True):
    id: Optional[int] = None
    name: str           # Nombre del servicio
    description: str    # Descripción detallada
    icon: str          # Icono (Font Awesome)
    features: str      # Características (JSON string)
    is_active: bool    # Servicio activo
    order: int         # Orden de visualización
```

### Project
Casos de éxito y portfolio.

```python
class Project(rx.Model, table=True):
    id: Optional[int] = None
    title: str              # Título del proyecto
    description: str        # Descripción del proyecto
    client_name: str        # Nombre del cliente
    technologies: str       # Tecnologías usadas
    image_url: Optional[str]  # URL de imagen
    project_url: Optional[str]  # URL del proyecto
    is_featured: bool       # Proyecto destacado
    created_at: datetime    # Fecha de creación
```

### BlogPost
Posts del blog técnico.

```python
class BlogPost(rx.Model, table=True):
    id: Optional[int] = None
    title: str              # Título del post
    slug: str              # URL slug
    content: str           # Contenido completo
    excerpt: str           # Resumen
    author: str            # Autor
    tags: str              # Tags separados por comas
    image_url: Optional[str]  # Imagen destacada
    is_published: bool     # Publicado
    created_at: datetime   # Fecha de creación
    updated_at: datetime   # Fecha de actualización
```

## 🔧 Configuración

### Base de Datos
```python
# Desarrollo
DATABASE_URL = "sqlite:///pyenterprise.db"

# Producción
DATABASE_URL = "postgresql://user:password@localhost/pyenterprise"
```

### Variables de Entorno
```bash
DATABASE_URL=sqlite:///pyenterprise.db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pyenterprise
DB_USER=admin
DB_PASSWORD=secret
```

## 📋 Migraciones (Futuro)

```bash
# Crear migración
python manage.py create-migration "add_user_table"

# Aplicar migraciones
python manage.py migrate

# Rollback
python manage.py rollback
```

## 🌱 Seeders

### Datos de Desarrollo
```python
# Poblar con datos de prueba
python seed_data.py

# Datos incluidos:
# - 5 contactos de ejemplo
# - 6 servicios predefinidos
# - 3 proyectos de muestra
# - 3 posts de blog
```

## 🔍 Consultas Comunes

### Contactos
```python
# Contactos pendientes
pending_contacts = session.exec(
    select(Contact).where(Contact.status == "pending")
).all()

# Contactos por fecha
recent_contacts = session.exec(
    select(Contact)
    .where(Contact.created_at >= last_week)
    .order_by(Contact.created_at.desc())
).all()
```

### Servicios
```python
# Servicios activos ordenados
active_services = session.exec(
    select(Service)
    .where(Service.is_active == True)
    .order_by(Service.order)
).all()
```

## 📊 Estadísticas

### Métricas de Contactos
```sql
-- Contactos por mes
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as total_contacts
FROM contact 
GROUP BY month 
ORDER BY month DESC;

-- Tasa de conversión por estado
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM contact), 2) as percentage
FROM contact 
GROUP BY status;
```

## 🔒 Backup y Restauración

```bash
# Backup
python manage.py backup-db

# Restaurar
python manage.py restore-db backup_20240922.db
```

## 🧪 Testing

```python
# Test de modelos
def test_contact_creation():
    contact = Contact(
        name="Test User",
        email="test@test.com",
        message="Test message"
    )
    assert contact.status == "pending"
    assert contact.name == "Test User"
```

## 📈 Índices Recomendados

```sql
-- Índices para optimizar consultas
CREATE INDEX idx_contact_status ON contact(status);
CREATE INDEX idx_contact_created_at ON contact(created_at);
CREATE INDEX idx_service_active_order ON service(is_active, order);
CREATE INDEX idx_project_featured ON project(is_featured);
CREATE INDEX idx_blogpost_published ON blogpost(is_published);
```

---
**Database Team** - PyEnterprise 🗄️
