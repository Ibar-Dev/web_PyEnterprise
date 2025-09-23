# 🎨 Frontend - PyEnterprise

Este módulo contiene todos los componentes de la interfaz de usuario (UI) desarrollados con Reflex.

## 📁 Estructura

```
frontend/
├── components/          # Componentes UI reutilizables
│   ├── navbar.py       # Barra de navegación
│   ├── hero.py         # Sección principal/hero
│   ├── about.py        # Sección sobre nosotros
│   ├── services.py     # Sección de servicios
│   ├── contact.py      # Formulario de contacto
│   └── footer.py       # Pie de página
└── pages/              # Páginas completas (futuro)
    └── admin.py        # Panel de administración
```

## 🧩 Componentes

### Navbar (`navbar.py`)
- **Función**: Navegación principal fija
- **Características**: Logo, menú responsive, botón CTA
- **Estado**: Sin estado (componente puro)

### Hero (`hero.py`)
- **Función**: Sección de presentación principal
- **Características**: Título, descripción, botones de acción, estadísticas
- **Estado**: Sin estado

### About (`about.py`)
- **Función**: Información de la empresa
- **Características**: Misión, visión, ventajas, estadísticas
- **Estado**: Sin estado

### Services (`services.py`)
- **Función**: Catálogo de servicios
- **Características**: 6 tarjetas de servicios, CTA
- **Estado**: Sin estado

### Contact (`contact.py`)
- **Función**: Formulario de contacto y información
- **Características**: Formulario con validación, información de contacto
- **Estado**: `ContactState` (maneja formulario)

### Footer (`footer.py`)
- **Función**: Pie de página con enlaces
- **Características**: Enlaces, redes sociales, información legal
- **Estado**: Sin estado

## 🎨 Estilos

Los estilos se importan desde `shared/styles.py`:

```python
from shared.styles import COLORS, card_style, section_style
```

### Variables de Color
- `COLORS["primary"]`: Azul empresarial (#2563eb)
- `COLORS["secondary"]`: Azul oscuro (#1e40af)
- `COLORS["success"]`: Verde (#10b981)
- `COLORS["error"]`: Rojo (#ef4444)

## 📱 Responsive Design

- **Mobile**: 1 columna
- **Tablet**: 2 columnas
- **Desktop**: 3-4 columnas (según componente)

```python
columns=["1", "2", "3", "3"]  # [mobile, tablet, desktop, xl]
```

## 🔄 Estados

### ContactState
Maneja el formulario de contacto:
- `name`, `email`, `company`, `message`: Campos del formulario
- `is_submitted`: Estado de envío exitoso
- `error_message`: Mensajes de error

## 🚀 Uso

```python
from frontend.components.navbar import navbar
from frontend.components.hero import hero_section

def my_page():
    return rx.box(
        navbar(),
        hero_section(),
        # ... más componentes
    )
```

## 🛠️ Desarrollo

### Añadir Nuevo Componente
1. Crear archivo en `components/`
2. Importar estilos desde `shared/styles.py`
3. Exportar función del componente
4. Importar en `app.py`

### Modificar Estilos
- Colores: Editar `shared/styles.py`
- Estilos específicos: Crear en el componente

---
**Frontend Team** - PyEnterprise 🎨
