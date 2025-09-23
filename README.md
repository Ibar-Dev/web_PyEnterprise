# PyEnterprise - Página Web Empresarial

Una página web moderna y profesional para PyEnterprise, desarrollada con **Reflex** (Python).

## 🚀 Características

### Frontend
- **Diseño Moderno**: Interfaz limpia y profesional
- **Responsive**: Optimizada para todos los dispositivos
- **Componentes Modulares**: Arquitectura escalable y mantenible
- **SEO Optimizada**: Estructura pensada para motores de búsqueda
- **Performance**: Carga rápida y experiencia fluida

### Backend
- **Base de Datos**: SQLite/PostgreSQL con SQLAlchemy
- **API REST**: Endpoints para gestión de contactos y contenido
- **Panel Admin**: Dashboard para gestión de contactos y configuración
- **Email**: Sistema de notificaciones automático
- **Modelos**: Contact, Service, Project, BlogPost

## 📋 Secciones

- **Hero Section**: Presentación principal con CTAs
- **Sobre Nosotros**: Información de la empresa, misión y visión
- **Servicios**: Catálogo completo de servicios oferecidos
- **Contacto**: Formulario funcional y información de contacto
- **Footer**: Enlaces adicionales y redes sociales

## 🛠️ Tecnologías

### Frontend
- **Reflex**: Framework Python para aplicaciones web fullstack
- **CSS3**: Estilos modernos y animaciones
- **Font Awesome**: Iconografía profesional
- **Google Fonts**: Tipografía Inter

### Backend
- **Python 3.8+**: Lenguaje de programación
- **SQLAlchemy**: ORM para base de datos
- **SQLite/PostgreSQL**: Base de datos
- **SMTP**: Sistema de emails
- **python-dotenv**: Gestión de variables de entorno

## 📦 Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd web_PyEnterprise
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\\Scripts\\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar Reflex**:
   ```bash
   reflex init
   ```

5. **Ejecutar la aplicación**:
   ```bash
   reflex run
   ```

6. **Poblar con datos de muestra** (opcional):
   ```bash
   python seed_data.py
   ```

La aplicación estará disponible en:
- **Frontend**: `http://localhost:3000`
- **Admin Panel**: `http://localhost:3000/admin`

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
├── pyenterprise/
│   ├── __init__.py
│   ├── pyenterprise.py          # Aplicación principal
│   ├── styles.py               # Estilos globales
│   └── components/             # Componentes modulares
│       ├── __init__.py
│       ├── navbar.py           # Navegación
│       ├── hero.py             # Sección hero
│       ├── about.py            # Sobre nosotros
│       ├── services.py         # Servicios
│       ├── contact.py          # Contacto
│       └── footer.py           # Pie de página
├── assets/                     # Recursos estáticos
│   └── logo.png               # Logo de la empresa
├── requirements.txt            # Dependencias
├── rxconfig.py                # Configuración de Reflex
└── README.md                  # Este archivo
```

## 🎨 Personalización

### Colores y Estilos
Los colores principales se definen en `pyenterprise/styles.py`:
- Primario: `#2563eb` (Azul empresarial)
- Secundario: `#1e40af` (Azul oscuro)
- Accent: `#3b82f6` (Azul claro)

### Contenido
Cada componente es fácilmente personalizable:
- **Hero**: Editar `components/hero.py` para cambiar el mensaje principal
- **Servicios**: Modificar `components/services.py` para ajustar servicios oferecidos
- **Contacto**: Personalizar `components/contact.py` con tu información

### Logo y Assets
- Reemplaza `assets/logo.png` con tu logo empresarial
- Añade más imágenes en la carpeta `assets/`

## 🚀 Despliegue

### Desarrollo
```bash
reflex run --env dev
```

### Producción
```bash
reflex run --env prod
```

### Docker (Opcional)
```bash
# Construir imagen
docker build -t pyenterprise-web .

# Ejecutar contenedor
docker run -p 3000:3000 pyenterprise-web
```

## 📧 Contacto

Para soporte técnico o consultas sobre el desarrollo:
- **Email**: contacto@pyenterprise.com
- **Teléfono**: +34 900 123 456
- **Web**: [www.pyenterprise.com](https://www.pyenterprise.com)

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo `LICENSE`.

---

**PyEnterprise** - Soluciones Empresariales con Python 🐍✨
