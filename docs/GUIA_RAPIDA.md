# 🚀 GUÍA RÁPIDA - PyLink Sistema de Gestión

## ✅ PROBLEMA SOLUCIONADO

Se han corregido dos problemas críticos:

1. **✅ Redirect de Administrador:** Ahora el admin (`admin@pylink.com`) es redirigido automáticamente al panel de administración `/admin` en lugar del dashboard de empleados.

2. **✅ Error UUID en Jornadas:** Se agregó validación para evitar el error `invalid input syntax for type uuid: "default"`.

---

## 🔑 CREDENCIALES DE ACCESO

### **Administrador**
```
URL: http://localhost:3000/empleados
Email: admin@pylink.com
Contraseña: admin123

Después del login → Redirige automáticamente a: /admin
```

### **Empleados**
```
URL: http://localhost:3000/empleados

Juan (Desarrollador):
Email: juan@pylink.com
Contraseña: emp123

María (Diseñadora):
Email: maria@pylink.com
Contraseña: emp123

Después del login → Redirige automáticamente a: /empleados/dashboard
```

---

## 🎯 PANEL DE ADMINISTRACIÓN

**URL Directa:** `http://localhost:3000/admin`

### **Tabs Disponibles:**

#### 1️⃣ **RESUMEN (Overview)**
Métricas del sistema en tiempo real:
- 📁 Total proyectos activos
- 👥 Total empleados activos
- ✅ Total tareas (pendientes/completadas)
- ⏰ Horas trabajadas este mes

#### 2️⃣ **PROYECTOS**
**Funciones:**
- ✅ Crear nuevos proyectos
- ✅ Ver lista completa
- ✅ Eliminar proyectos

**Formulario de Creación:**
- Nombre del proyecto
- Cliente
- Descripción
- Fecha de inicio
- Presupuesto de horas

**Ejemplo:**
```
Nombre: Sistema CRM
Cliente: Empresa XYZ
Descripción: Sistema de gestión de clientes
Fecha: 2024-01-01
Presupuesto: 200 horas
```

#### 3️⃣ **EMPLEADOS**
**Funciones:**
- ✅ Crear nuevos empleados
- ✅ Ver horas mensuales de cada empleado
- ✅ Ver proyectos y tareas asignadas
- ✅ Desactivar empleados

**Formulario de Creación:**
- Email
- Contraseña
- Nombre
- Apellidos
- Rol: desarrollador, diseñador, gerente, qa, admin

**Ejemplo:**
```
Email: carlos@pylink.com
Contraseña: emp123
Nombre: Carlos
Apellidos: García
Rol: desarrollador
```

**Vista de Empleados Muestra:**
- ⏰ Horas este mes: X.X h
- 📁 Proyectos asignados
- ✅ Tareas totales

#### 4️⃣ **TAREAS**
**Funciones:**
- ✅ Crear tareas
- ✅ Asignar a proyectos y empleados
- ✅ Establecer prioridades y fechas

**Formulario de Creación:**
- ID del proyecto (copiar de la lista de proyectos)
- ID del empleado (copiar de la lista de empleados)
- Título de la tarea
- Descripción
- Prioridad: alta, media, baja
- Fecha de vencimiento
- Horas estimadas

**Cómo Crear una Tarea:**
1. Ir a tab "Proyectos" → Copiar el ID del proyecto (el UUID largo)
2. Ir a tab "Empleados" → Copiar el ID del empleado
3. Ir a tab "Tareas" → Pegar los IDs en el formulario
4. Llenar resto de información
5. Click en "Crear Tarea"

**Ejemplo:**
```
ID Proyecto: abc123-456-789... (copiar del tab Proyectos)
ID Empleado: def456-789-012... (copiar del tab Empleados)
Título: Diseñar base de datos
Descripción: Crear esquema de BD para módulo de ventas
Prioridad: alta
Fecha vencimiento: 2024-12-31
Horas estimadas: 8
```

#### 5️⃣ **JORNADAS**
**Funciones:**
- ✅ Ver historial completo de jornadas
- ✅ Ver horas trabajadas por empleado
- ✅ Filtrar por fecha

---

## 👤 DASHBOARD DE EMPLEADOS

**URL:** `http://localhost:3000/empleados/dashboard`

### **Funcionalidades:**

#### 🕐 **Control de Tiempo**
- Iniciar jornada laboral
- Finalizar jornada
- Agregar descripción de actividades
- Ver horas trabajadas hoy/semana

**Proceso:**
1. Click en "🟢 Iniciar Jornada"
2. Trabajar en tu proyecto
3. Escribir descripción de lo que hiciste
4. Click en "🔴 Finalizar Jornada"
5. Las horas se calculan automáticamente

#### 📁 **Mis Proyectos**
Ver proyectos asignados con:
- Nombre del proyecto
- Cliente
- Estado

#### ✅ **Mis Tareas**
Ver tareas asignadas con:
- Título
- Estado
- Prioridad
- Fecha de vencimiento

#### 📈 **Historial de Jornadas**
Ver jornadas registradas con:
- Fecha
- Horas trabajadas
- Descripción de actividades

---

## 🔧 COMANDOS ÚTILES

### **Iniciar la Aplicación**
```bash
cd c:\Users\josem\Documents\web_PyEnterprise
reflex run
```
Luego abrir: `http://localhost:3000`

### **Probar el Backend**
```bash
python test_backend_completo.py
```

### **Agregar Datos de Prueba**
```bash
python agregar_datos_prueba.py
```

### **Asignar Admin a Proyecto** (ya ejecutado)
```bash
python asignar_admin_proyecto.py
```

---

## ⚠️ NOTAS IMPORTANTES

### **Para Administradores:**
- ✅ El admin ahora tiene un proyecto asignado: "Portal Web Corporativo"
- ✅ Puede registrar jornadas sin errores
- ✅ El redirect automático funciona correctamente
- ✅ Puede gestionar todo desde el panel de admin

### **Para Empleados:**
- ⚠️ Necesitan tener al menos UN proyecto asignado para poder registrar jornadas
- ⚠️ Si un empleado no tiene proyectos, no puede iniciar jornada

### **IDs de Proyectos y Empleados:**
- Son UUIDs largos (ejemplo: `abc123-456-789-...`)
- Copiarlos exactamente como aparecen en las listas
- No escribirlos manualmente, usar copiar/pegar

---

## 🐛 SOLUCIÓN A PROBLEMAS COMUNES

### **Error: "invalid input syntax for type uuid"**
✅ **SOLUCIONADO** - Se agregó validación de UUIDs

### **Admin ve dashboard de empleado**
✅ **SOLUCIONADO** - Ahora redirige a `/admin`

### **No puedo iniciar jornada**
Verifica que:
1. Tengas al menos un proyecto asignado
2. El proyecto tiene un ID válido

### **No puedo crear tarea**
Verifica que:
1. Hayas copiado correctamente el ID del proyecto
2. Hayas copiado correctamente el ID del empleado
3. Los IDs sean UUIDs válidos (largos)

---

## 📊 ESTRUCTURA DE ACCESO

```
┌─────────────────────────────────┐
│   http://localhost:3000         │
│   (Página Principal)            │
└────────────┬────────────────────┘
             │
             ├── /empleados (Login)
             │   │
             │   ├─ Admin → /admin (Panel Administración)
             │   │
             │   └─ Empleado → /empleados/dashboard
             │
             └── (Otros)
```

---

## 🎉 RESUMEN

**TODO FUNCIONA CORRECTAMENTE:**

✅ Panel de administración completo  
✅ Dashboard de empleados funcional  
✅ Sistema de autenticación con redirect correcto  
✅ Registro de jornadas sin errores  
✅ Gestión de proyectos, tareas y empleados  
✅ Estadísticas en tiempo real  
✅ Horas mensuales por empleado  
✅ Base de datos Supabase integrada  

**READY TO USE! 🚀**
