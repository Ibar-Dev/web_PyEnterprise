# 🚀 PyLink - Sistema Completo de Gestión Empresarial

## 📋 Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Funcionalidades Completas](#funcionalidades-completas)
5. [Panel de Administración](#panel-de-administración)
6. [Dashboard de Empleados](#dashboard-de-empleados)
7. [Base de Datos](#base-de-datos)
8. [API y Backend](#api-y-backend)
9. [Guía de Uso](#guía-de-uso)
10. [Credenciales de Prueba](#credenciales-de-prueba)

---

## 🎯 Descripción General

**PyLink** es un sistema completo de gestión empresarial desarrollado con **Python** y **Reflex**, integrado con **Supabase** (PostgreSQL) para gestión de datos en tiempo real.

### Características Principales:
- ✅ **Autenticación segura** con bcrypt
- ✅ **Panel de administración completo**
- ✅ **Dashboard para empleados**
- ✅ **Gestión de proyectos, tareas y jornadas**
- ✅ **Reportes y estadísticas en tiempo real**
- ✅ **Interfaz moderna y responsive**
- ✅ **Base de datos PostgreSQL en la nube**

---

## 🏗️ Arquitectura del Sistema

### **Stack Tecnológico:**
```
Frontend:  Reflex (Python framework web)
Backend:   Python 3.11+
Base de Datos: Supabase (PostgreSQL)
Autenticación: bcrypt
Estilo: CSS personalizado + Reflex Components
```

### **Estructura del Proyecto:**
```
web_PyEnterprise/
├── pyenterprise/
│   ├── pyenterprise.py          # App principal
│   ├── styles.py                # Estilos globales
│   ├── components/
│   │   ├── employee_auth.py     # Sistema de autenticación
│   │   ├── employee_dashboard_integrated.py  # Dashboard empleados
│   │   ├── admin_panel_profesional.py        # Panel admin completo
│   │   ├── navbar.py, hero.py, about.py, etc.
│   └── database/
│       ├── __init__.py
│       └── supabase_client.py   # Cliente de BD con todas las funciones
├── .env                         # Variables de entorno (Supabase)
├── requirements.txt
├── database_schema.sql          # Esquema completo de la BD
└── README.md
```

---

## 🔧 Instalación y Configuración

### **1. Requisitos Previos:**
```bash
Python 3.11+
pip (gestor de paquetes)
Cuenta en Supabase (gratis)
```

### **2. Instalación:**
```bash
# Clonar o descargar el proyecto
cd web_PyEnterprise

# Instalar dependencias
pip install -r requirements.txt
```

### **3. Configurar Variables de Entorno:**
Crear archivo `.env` en la raíz:
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-publica
```

### **4. Configurar Base de Datos:**
```bash
# Ejecutar el script SQL en Supabase
# Ir a: https://supabase.com > SQL Editor
# Copiar y ejecutar: database_schema.sql
```

### **5. Agregar Datos de Prueba:**
```bash
python agregar_datos_prueba.py
```

### **6. Ejecutar la Aplicación:**
```bash
reflex run
```

La aplicación estará disponible en: **http://localhost:3000**

---

## 🎨 Funcionalidades Completas

### **SISTEMA DE AUTENTICACIÓN**
- ✅ Login seguro con email y contraseña
- ✅ Hash de contraseñas con bcrypt
- ✅ Validación de credenciales
- ✅ Sesiones persistentes
- ✅ Roles de usuario (admin, desarrollador, diseñador, gerente, qa)

### **GESTIÓN DE PROYECTOS**
- ✅ Crear proyectos con: nombre, cliente, descripción, presupuesto
- ✅ Ver lista completa de proyectos
- ✅ Editar información de proyectos
- ✅ Eliminar proyectos (soft delete)
- ✅ Asignar empleados a proyectos
- ✅ Seguimiento de progreso
- ✅ Control de presupuesto de horas

### **GESTIÓN DE EMPLEADOS**
- ✅ Crear empleados con email, contraseña, rol
- ✅ Ver lista de todos los empleados
- ✅ **Horas trabajadas por mes de cada empleado**
- ✅ Estadísticas: proyectos asignados, tareas completadas
- ✅ Desactivar empleados
- ✅ Roles personalizables

### **GESTIÓN DE TAREAS**
- ✅ Crear tareas asignadas a proyectos y empleados
- ✅ Prioridades: alta, media, baja
- ✅ Estados: pendiente, en_progreso, completada
- ✅ Fechas de vencimiento
- ✅ Estimación de horas
- ✅ Descripción detallada

### **CONTROL DE JORNADAS LABORALES**
- ✅ Empleados pueden iniciar/finalizar jornadas
- ✅ Registro de horas trabajadas por día
- ✅ Descripción de actividades realizadas
- ✅ Cálculo automático de horas totales
- ✅ Historial completo de jornadas
- ✅ Reportes mensuales de horas

### **REPORTES Y ESTADÍSTICAS**
- ✅ Dashboard con métricas en tiempo real
- ✅ Total de proyectos activos
- ✅ Total de empleados activos
- ✅ Tareas pendientes vs completadas
- ✅ Horas trabajadas este mes
- ✅ Horas totales del sistema
- ✅ Estadísticas por empleado

---

## 🔧 Panel de Administración

**URL:** `http://localhost:3000/admin`  
**Credenciales:** `admin@pylink.com` / `admin123`

### **Tabs Disponibles:**

#### **1️⃣ Resumen (Overview)**
Dashboard con estadísticas generales:
- 📁 Total de proyectos activos
- 👥 Total de empleados activos
- ✅ Total de tareas (pendientes/completadas)
- ⏰ Horas trabajadas este mes
- 📊 Visualización del mes actual

#### **2️⃣ Proyectos**
**Funciones:**
- Crear nuevos proyectos
- Ver lista completa de proyectos
- Editar información
- Eliminar proyectos
- Ver estado y presupuesto

**Formulario de Creación:**
- Nombre del proyecto
- Cliente
- Descripción
- Fecha de inicio
- Presupuesto de horas

#### **3️⃣ Empleados**
**Funciones:**
- Crear nuevos empleados
- Ver lista con estadísticas completas
- **Ver horas trabajadas del mes actual por empleado**
- Ver proyectos asignados por empleado
- Ver tareas asignadas
- Desactivar empleados

**Estadísticas Mostradas por Empleado:**
- ⏰ Horas trabajadas este mes
- 📁 Número de proyectos asignados
- ✅ Número de tareas asignadas
- Email y rol

#### **4️⃣ Tareas**
**Funciones:**
- Crear nuevas tareas
- Asignar a proyectos y empleados
- Establecer prioridades
- Definir fechas de vencimiento
- Ver lista completa de tareas
- Filtrar por estado

#### **5️⃣ Jornadas**
**Funciones:**
- Ver historial completo de jornadas
- Filtrar por fecha
- Ver empleado y proyecto de cada jornada
- Ver horas trabajadas por jornada
- Descripción de actividades

---

## 👤 Dashboard de Empleados

**URL:** `http://localhost:3000/empleados/dashboard`  
**Credenciales:** `juan@pylink.com` / `emp123`

### **Funcionalidades:**

#### **1️⃣ Control de Tiempo**
- 🟢 Iniciar jornada laboral
- 🔴 Finalizar jornada
- Agregar descripción de actividades
- Ver horas trabajadas hoy
- Ver horas trabajadas esta semana

#### **2️⃣ Mis Proyectos**
- Ver proyectos asignados
- Información del cliente
- Estado del proyecto
- Navegación intuitiva

#### **3️⃣ Mis Tareas**
- Ver tareas asignadas
- Estado de cada tarea
- Prioridad visual
- Fechas de vencimiento

#### **4️⃣ Historial de Jornadas**
- Ver últimas jornadas registradas
- Horas trabajadas por día
- Descripción de actividades
- Total de jornadas

---

## 💾 Base de Datos

### **Tablas Principales:**

#### **empleados**
```sql
- id (UUID, PK)
- email (TEXT, UNIQUE)
- password_hash (TEXT)
- nombre (TEXT)
- apellidos (TEXT)
- rol (TEXT)
- activo (BOOLEAN)
- fecha_ingreso (DATE)
- created_at (TIMESTAMP)
```

#### **proyectos**
```sql
- id (UUID, PK)
- nombre (TEXT)
- descripcion (TEXT)
- cliente (TEXT)
- fecha_inicio (DATE)
- fecha_fin (DATE)
- estado (TEXT)
- presupuesto_horas (INTEGER)
- progreso (INTEGER)
- created_at (TIMESTAMP)
```

#### **tareas**
```sql
- id (UUID, PK)
- proyecto_id (UUID, FK)
- empleado_asignado_id (UUID, FK)
- titulo (TEXT)
- descripcion (TEXT)
- estado (TEXT)
- prioridad (TEXT)
- fecha_creacion (TIMESTAMP)
- fecha_vencimiento (DATE)
- horas_estimadas (DECIMAL)
```

#### **jornadas**
```sql
- id (UUID, PK)
- empleado_id (UUID, FK)
- proyecto_id (UUID, FK)
- fecha (DATE)
- hora_inicio (TIMESTAMP)
- hora_fin (TIMESTAMP)
- horas_trabajadas (DECIMAL)
- descripcion (TEXT)
- estado (TEXT)
```

#### **proyecto_empleado**
```sql
- id (UUID, PK)
- proyecto_id (UUID, FK)
- empleado_id (UUID, FK)
- rol_en_proyecto (TEXT)
- activo (BOOLEAN)
- fecha_asignacion (TIMESTAMP)
```

---

## 🔌 API y Backend

### **Funciones Principales del Backend:**

```python
# Autenticación
login_empleado(email, password)
crear_empleado(email, password, nombre, apellidos, rol)

# Proyectos
obtener_todos_proyectos()
obtener_proyectos_empleado(empleado_id)
crear_proyecto(nombre, descripcion, cliente, fecha_inicio, presupuesto_horas)
eliminar_proyecto(proyecto_id)
actualizar_proyecto(proyecto_id, datos)
obtener_proyecto_por_id(proyecto_id)

# Empleados
obtener_todos_empleados()
obtener_empleados_con_estadisticas(año, mes)
obtener_empleado_por_id(empleado_id)
eliminar_empleado(empleado_id)

# Tareas
crear_tarea(proyecto_id, empleado_asignado_id, titulo, descripcion, prioridad, fecha_vencimiento, horas_estimadas)
obtener_tareas_empleado(empleado_id)
obtener_tareas_proyecto(proyecto_id)
obtener_todas_tareas()
actualizar_estado_tarea(tarea_id, nuevo_estado)
actualizar_tarea(tarea_id, datos)

# Jornadas
registrar_jornada(empleado_id, proyecto_id, fecha, hora_inicio, hora_fin, descripcion)
obtener_jornadas_empleado(empleado_id, fecha_inicio, fecha_fin)
obtener_todas_jornadas(fecha_inicio, fecha_fin)
calcular_horas_totales_empleado(empleado_id, fecha_inicio, fecha_fin)
calcular_horas_mensuales_empleado(empleado_id, año, mes)

# Estadísticas
obtener_estadisticas_sistema()
obtener_resumen_dashboard_admin()
obtener_estadisticas_proyecto(proyecto_id)

# Asignaciones
asignar_empleado_proyecto(empleado_id, proyecto_id, rol_en_proyecto)
```

---

## 📖 Guía de Uso

### **Para Administradores:**

1. **Iniciar Sesión:**
   - Ir a `http://localhost:3000/empleados`
   - Usar credenciales de administrador
   - Automáticamente redirige al panel admin

2. **Crear Nuevo Proyecto:**
   - Tab "Proyectos" → Formulario de creación
   - Llenar: nombre, cliente, descripción, fecha, presupuesto
   - Click en "Crear Proyecto"
   - El proyecto aparecerá en la lista inmediatamente

3. **Crear Nuevo Empleado:**
   - Tab "Empleados" → Formulario de creación
   - Llenar: email, contraseña, nombre, apellidos
   - Seleccionar rol
   - Click en "Crear Empleado"

4. **Crear Nueva Tarea:**
   - Tab "Tareas" → Formulario de creación
   - Copiar ID del proyecto (desde tab Proyectos)
   - Copiar ID del empleado (desde tab Empleados)
   - Llenar información de la tarea
   - Click en "Crear Tarea"

5. **Ver Estadísticas:**
   - Tab "Resumen" → Ver métricas en tiempo real
   - Tab "Empleados" → Ver horas mensuales de cada empleado
   - Tab "Jornadas" → Ver historial completo

### **Para Empleados:**

1. **Iniciar Sesión:**
   - Ir a `http://localhost:3000/empleados`
   - Usar credenciales de empleado
   - Automáticamente redirige al dashboard

2. **Registrar Jornada:**
   - Click en "🟢 Iniciar Jornada"
   - Trabajar en el proyecto
   - Agregar descripción de actividades
   - Click en "🔴 Finalizar Jornada"
   - Las horas se calculan automáticamente

3. **Ver Proyectos y Tareas:**
   - Sección "Mis Proyectos" → Ver proyectos asignados
   - Sección "Mis Tareas" → Ver tareas pendientes
   - Revisar prioridades y fechas

4. **Consultar Historial:**
   - Sección "Historial de Jornadas"
   - Ver todas las jornadas registradas
   - Ver horas trabajadas por día

---

## 🔑 Credenciales de Prueba

### **Administrador:**
```
Email: admin@pylink.com
Contraseña: admin123
Acceso: Panel completo de administración
```

### **Empleados:**
```
Email: juan@pylink.com
Contraseña: emp123
Rol: Desarrollador

Email: maria@pylink.com
Contraseña: emp123
Rol: Diseñadora
```

---

## 🚀 Próximas Mejoras (Opcional)

- [ ] Sistema de notificaciones
- [ ] Exportar reportes a PDF
- [ ] Gráficos avanzados con Chart.js
- [ ] Calendario de tareas
- [ ] Sistema de comentarios en tareas
- [ ] Upload de archivos
- [ ] API REST completa
- [ ] Aplicación móvil

---

## 📞 Soporte

Para dudas o problemas:
- Revisar logs en consola
- Verificar variables de entorno (.env)
- Comprobar conexión a Supabase
- Ejecutar `python test_backend_completo.py` para verificar backend

---

## 📜 Licencia

Este proyecto es de uso educativo y demostrativo.

---

**🎉 ¡Sistema Completamente Funcional y Listo para Producción!**

Desarrollado con ❤️ usando Python, Reflex y Supabase.
