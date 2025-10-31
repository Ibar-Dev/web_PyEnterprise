# 🚀 PyLink - Sistema de Gestión Empresarial

Sistema completo de gestión de proyectos, tareas y empleados desarrollado con Python, Reflex y Supabase.

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
├── pyenterprise/                  # 💻 Código principal
│   ├── components/                # 🎨 Componentes UI
│   │   ├── admin_panel_profesional.py
│   │   ├── employee_auth.py
│   │   ├── employee_dashboard_integrated.py
│   │   ├── navbar.py, hero.py, about.py
│   │   └── footer.py, contact.py, team.py
│   ├── database/                  # 🗄️ Backend y BD
│   │   ├── __init__.py
│   │   └── supabase_client.py
│   ├── pages/                     # 📄 Páginas
│   │   ├── contact.py, services.py
│   │   └── privacy.py, cookies.py, terms.py
│   ├── utils/                     # 🛠️ Utilidades
│   │   ├── rate_limiter.py
│   │   └── config.py
│   ├── pyenterprise.py            # 🚀 App principal
│   └── styles.py                  # 🎨 Estilos globales
│
├── tests/                         # 🧪 Tests
│   ├── unit/                      # Tests unitarios
│   │   ├── test_auth.py
│   │   └── test_rate_limiter.py
│   └── integration/               # Tests de integración
│
├── scripts/                       # 🛠️ Scripts auxiliares
│   └── (scripts de gestión)
│
├── assets/                        # 🖼️ Assets estáticos
├── .env                           # 🔐 Variables de entorno
├── .env.example                   # 📋 Template de config
├── CREDENCIALES.md                # 🔑 Credenciales (confidencial)
├── database_schema.sql            # 🗄️ Esquema de BD
├── requirements.txt               # 📦 Dependencias
├── rxconfig.py                    # ⚙️ Config de Reflex
├── setup_users.py                 # 👥 Script crear usuarios
└── README.md                      # 📖 Este archivo
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

## 🌐 URLs de Acceso

### Producción (Netlify):
```
https://pylink.netlify.app/
```

### Desarrollo Local:
```
http://localhost:3000
```

### Rutas:
- **Login Empleados:** `/empleados`
- **Dashboard Empleado:** `/empleados/dashboard` (requiere login)
- **Panel Admin:** `/admin` (requiere login como admin)

## 🔑 Credenciales

⚠️ **Para obtener las credenciales completas, consulta el archivo `CREDENCIALES.md`** (archivo confidencial no incluido en Git)

### Ejemplo de formato de cuentas:
- **Administradores:** `nombre.admin@pylink.com`
- **Trabajadores:** `nombre.trabajador@pylink.com`

## 📚 Documentación

- **[CREDENCIALES.md](CREDENCIALES.md)** - Credenciales de acceso (confidencial)
- **[database_schema.sql](database_schema.sql)** - Esquema de la base de datos
- **Tests:** Carpeta `tests/` con pruebas unitarias y de integración

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
