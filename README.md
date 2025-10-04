# 🚀 PyLink - Sistema de Gestión Empresarial

Sistema completo de gestión de proyectos, tareas y empleados desarrollado con Python, Reflex y Supabase.

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
├── docs/                          # 📄 Documentación
│   ├── CAMBIOS_REALIZADOS.md      # Registro de cambios recientes
│   ├── database_schema.md         # Esquema de la base de datos
│   ├── DOCUMENTACION_COMPLETA.md  # Documentación completa del sistema
│   ├── ESTRUCTURA.md              # Estructura del proyecto
│   ├── GETTING_STARTED.md         # Guía de inicio rápido
│   └── GUIA_RAPIDA.md             # Guía de uso rápida
│
├── pyenterprise/                  # 💻 Código principal
│   ├── components/                # 🎨 Componentes del frontend
│   │   ├── admin_panel_profesional.py
│   │   ├── employee_auth.py
│   │   ├── employee_dashboard_integrated.py
│   │   └── ...
│   ├── database/                  # 🗄️ Backend y acceso a datos
│   │   ├── __init__.py
│   │   └── supabase_client.py
│   ├── pyenterprise.py            # App principal
│   └── styles.py                  # Estilos globales
│
├── tests/                         # 🧪 Tests del sistema
│   ├── test_backend_completo.py
│   ├── test_login.py
│   ├── test_sistema_completo.py
│   └── test_supabase.py
│
├── scripts/                       # 🛠️ Scripts auxiliares
│   ├── agregar_datos_prueba.py    # Agregar datos de prueba
│   ├── asignar_admin_proyecto.py  # Asignar admin a proyecto
│   ├── fix_passwords.py           # Actualizar contraseñas
│   ├── seed_data.py               # Seed de datos iniciales
│   └── manage.py                  # Script de gestión
│
├── .web/                          # 📦 Build de Reflex (generado)
├── assets/                        # 🖼️ Assets estáticos
├── .env                           # 🔐 Variables de entorno
├── .env.example                   # 📋 Ejemplo de variables de entorno
├── .gitignore                     # 🚫 Archivos ignorados por Git
├── app.py                         # 🚀 Entry point de la aplicación
├── LICENSE                        # 📜 Licencia
├── requirements.txt               # 📦 Dependencias de Python
├── rxconfig.py                    # ⚙️ Configuración de Reflex
└── setup.py                       # 📦 Setup de instalación
```

## 🚀 Inicio Rápido

### 1. **Clonar el repositorio**
```bash
git clone <url-del-repo>
cd web_PyEnterprise
```

### 2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 3. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tus credenciales de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-publica
```

### 4. **Ejecutar la aplicación**
```bash
reflex run
```

La aplicación estará disponible en: **http://localhost:3000**

## 🔑 Credenciales de Prueba

### Administrador
```
Email: admin@pylink.com
Contraseña: admin123
URL: http://localhost:3000/admin
```

### Empleados
```
Juan (Desarrollador):
Email: juan@pylink.com
Contraseña: emp123

María (Diseñadora):
Email: maria@pylink.com
Contraseña: emp123
```

## 📚 Documentación

- **[Documentación Completa](docs/DOCUMENTACION_COMPLETA.md)** - Guía completa del sistema
- **[Guía Rápida](docs/GUIA_RAPIDA.md)** - Guía de uso rápida
- **[Cambios Realizados](docs/CAMBIOS_REALIZADOS.md)** - Registro de cambios recientes
- **[Estructura](docs/ESTRUCTURA.md)** - Estructura del proyecto
- **[Getting Started](docs/GETTING_STARTED.md)** - Guía de inicio rápido

## 🧪 Testing

### Ejecutar todos los tests
```bash
# Test completo del backend
python tests/test_backend_completo.py

# Test de autenticación
python tests/test_login.py

# Test del sistema completo
python tests/test_sistema_completo.py

# Test de Supabase
python tests/test_supabase.py
```

## 🛠️ Scripts Auxiliares

### Agregar datos de prueba
```bash
python scripts/agregar_datos_prueba.py
```

### Asignar admin a un proyecto
```bash
python scripts/asignar_admin_proyecto.py
```

### Actualizar contraseñas
```bash
python scripts/fix_passwords.py
```

## 🎯 Características Principales

### Panel de Administración
- ✅ Gestión completa de proyectos
- ✅ Gestión de empleados con estadísticas
- ✅ Creación y asignación de tareas
- ✅ Vista de jornadas laborales
- ✅ Reportes y estadísticas en tiempo real

### Dashboard de Empleados
- ✅ Vista de proyectos asignados
- ✅ Vista de tareas pendientes
- ✅ Registro de jornadas laborales
- ✅ Historial de horas trabajadas

### Características Técnicas
- ✅ Autenticación segura con bcrypt
- ✅ Base de datos PostgreSQL en Supabase
- ✅ Interfaz moderna con Reflex
- ✅ Validación de formularios
- ✅ Eliminación completa (hard delete)
- ✅ Presupuestos en euros
- ✅ Responsive design

## 🏗️ Tecnologías Utilizadas

- **Frontend:** Reflex (Python)
- **Backend:** Python 3.11+
- **Base de Datos:** Supabase (PostgreSQL)
- **Autenticación:** bcrypt
- **Estilos:** CSS personalizado + Reflex Components

## 📝 Licencia

[Especificar licencia aquí]

## 👨‍💻 Autor

[Tu nombre/organización]

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📧 Contacto

[Tu información de contacto]

---

**🎉 ¡Sistema completamente funcional y listo para producción!**

Desarrollado con ❤️ usando Python, Reflex y Supabase.
