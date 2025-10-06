# 🚀 PyLink - Sistema de Gestión Empresarial

Sistema completo de gestión de proyectos, tareas y empleados desarrollado con **Python, Reflex y Supabase**.

---

## 📋 Contenido

1. [¿Qué es PyLink?](#qué-es-pylink)
2. [Instalación](#instalación)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Credenciales de Prueba](#credenciales-de-prueba)
5. [Documentación](#documentación)

---

## 🎯 ¿Qué es PyLink?

**PyLink** es un sistema de gestión empresarial que permite:

### Para Administradores:
- ✅ Gestionar proyectos con presupuestos en €
- ✅ Crear y asignar tareas a empleados
- ✅ Ver estadísticas de horas trabajadas
- ✅ Administrar empleados y sus roles
- ✅ Generar reportes en tiempo real

### Para Empleados:
- ✅ Ver proyectos asignados
- ✅ Gestionar tareas pendientes
- ✅ Registrar jornadas laborales
- ✅ Ver historial de horas trabajadas

---

## 🚀 Instalación

### **1. Clonar el repositorio**
```bash
git clone <url-del-repo>
cd web_PyEnterprise
```

### **2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **3. Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar credenciales de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-publica
```

### **4. Ejecutar la aplicación**
```bash
reflex run
```

La aplicación estará en: **http://localhost:3000**

---

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
│
├── pyenterprise/                  # 💻 Código principal de la aplicación
│   │
│   ├── database/                  # 🗄️ BACKEND - Acceso a base de datos
│   │   ├── __init__.py            # Exports de funciones
│   │   └── supabase_client.py     # ⭐ TODAS las funciones del backend
│   │
│   ├── components/                # 🎨 FRONTEND - Componentes de UI
│   │   ├── admin_panel_profesional.py     # Panel de administración
│   │   ├── employee_dashboard_integrated.py # Dashboard empleados
│   │   ├── employee_auth.py       # Sistema de autenticación
│   │   └── ...
│   │
│   ├── services/                  # 🔧 Lógica de negocio
│   ├── models/                    # 📊 Modelos de datos
│   ├── utils/                     # 🛠️ Utilidades
│   ├── pyenterprise.py            # 🚀 App principal (routes)
│   └── styles.py                  # 🎨 Estilos globales
│
├── docs/                          # 📄 Documentación
│   ├── README.md                  # 👈 Este archivo
│   ├── GUIA_USUARIO.md            # Guía de uso del sistema
│   ├── GUIA_DESARROLLADOR.md      # Guía técnica para desarrolladores
│   └── CHANGELOG.md               # Historial de cambios
│
├── tests/                         # 🧪 Tests del sistema
│   ├── test_backend_completo.py
│   ├── test_login.py
│   └── ...
│
├── scripts/                       # 🛠️ Scripts auxiliares
│   ├── agregar_datos_prueba.py    # Seed de datos de prueba
│   ├── asignar_admin_proyecto.py
│   └── ...
│
├── app.py                         # 🚀 Entry point de la aplicación
├── requirements.txt               # 📦 Dependencias Python
├── rxconfig.py                    # ⚙️ Configuración de Reflex
└── README.md                      # 📘 README principal del proyecto
```

---

## 📂 Backend - Estructura Detallada

### **Archivo Principal: `pyenterprise/database/supabase_client.py`**

Este archivo contiene **TODAS** las funciones del backend organizadas por categorías:

```python
# 🔐 AUTENTICACIÓN
- login_empleado()          # Login con email/password
- crear_empleado()          # Crear nuevo empleado

# 📁 PROYECTOS
- crear_proyecto()          # Crear proyecto con presupuesto en €
- obtener_todos_proyectos() # Listar todos los proyectos
- obtener_proyecto_por_id() # Obtener proyecto específico
- actualizar_proyecto()     # Actualizar proyecto
- eliminar_proyecto()       # Eliminar proyecto (hard delete)
- asignar_empleado_proyecto() # Asignar empleado a proyecto

# ✅ TAREAS
- crear_tarea()             # Crear tarea con validación de fecha
- obtener_todas_tareas()    # Listar todas las tareas
- obtener_tareas_empleado() # Tareas de un empleado
- actualizar_estado_tarea() # Cambiar estado de tarea
- eliminar_tarea()          # Eliminar tarea (hard delete)

# 👥 EMPLEADOS
- obtener_todos_empleados() # Listar empleados
- obtener_empleado_por_id() # Obtener empleado específico
- eliminar_empleado()       # Eliminar empleado (hard delete)
- obtener_empleados_con_estadisticas() # Empleados con horas mensuales

# ⏰ JORNADAS LABORALES
- registrar_jornada()       # Registrar jornada con validación UUID
- obtener_jornadas_empleado() # Jornadas de un empleado
- obtener_todas_jornadas()  # Todas las jornadas
- calcular_horas_totales_empleado() # Total de horas trabajadas
- calcular_horas_mensuales_empleado() # Horas del mes actual

# 📊 ESTADÍSTICAS Y REPORTES
- obtener_estadisticas_sistema() # Estadísticas generales
- obtener_resumen_dashboard_admin() # Resumen para admin
- obtener_estadisticas_proyecto() # Estadísticas por proyecto
```

**Características del Backend:**
- ✅ Validación de fechas (formato AAAA-MM-DD)
- ✅ Validación de UUIDs
- ✅ Hard delete (eliminación completa)
- ✅ Manejo de errores con mensajes descriptivos
- ✅ Queries optimizadas con joins
- ✅ Cálculos automáticos (horas, estadísticas)

---

## 🔑 Credenciales de Prueba

### **Administrador**
```
URL: http://localhost:3000/empleados
Email: admin@pylink.com
Contraseña: admin123
→ Redirige automáticamente a /admin
```

### **Empleados**
```
Juan (Desarrollador):
- Email: juan@pylink.com
- Contraseña: emp123

María (Diseñadora):
- Email: maria@pylink.com
- Contraseña: emp123
```

---

## 📚 Documentación

- **[GUIA_USUARIO.md](GUIA_USUARIO.md)** - Cómo usar el sistema (admin y empleados)
- **[GUIA_DESARROLLADOR.md](GUIA_DESARROLLADOR.md)** - Estructura técnica, backend, tests
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios y mejoras

---

## 🛠️ Tecnologías Utilizadas

- **Frontend:** Reflex (Python framework web)
- **Backend:** Python 3.11+
- **Base de Datos:** Supabase (PostgreSQL)
- **Autenticación:** bcrypt
- **Estilos:** CSS personalizado + Reflex Components

---

## 🚀 Comandos Rápidos

```bash
# Iniciar aplicación
reflex run

# Agregar datos de prueba
python scripts/agregar_datos_prueba.py

# Ejecutar tests
python tests/test_backend_completo.py
```

---

## 📧 Soporte

Para más información consulta:
- [Guía de Usuario](GUIA_USUARIO.md)
- [Guía de Desarrollador](GUIA_DESARROLLADOR.md)

---

**🎉 Sistema completamente funcional y listo para usar!**

Desarrollado con ❤️ usando Python, Reflex y Supabase.
