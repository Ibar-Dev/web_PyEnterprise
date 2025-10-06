# 👤 Guía de Usuario - PyLink

Guía completa para usar el sistema de gestión PyLink.

---

## 📋 Contenido

1. [Panel de Administración](#panel-de-administración)
2. [Dashboard de Empleados](#dashboard-de-empleados)
3. [Formatos y Validaciones](#formatos-y-validaciones)
4. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 👨‍💼 Panel de Administración

**Acceso:** `http://localhost:3000/empleados`  
**Credenciales:** admin@pylink.com / admin123

### **5 Secciones Principales:**

---

### **1. 📊 RESUMEN**

Vista general del sistema con:
- Total de proyectos activos
- Total de empleados
- Total de tareas
- Horas trabajadas del mes

---

### **2. 📁 PROYECTOS**

#### **Crear Proyecto:**
```
1. Llenar formulario:
   - Nombre: "Desarrollo Web"
   - Cliente: "Empresa ABC"
   - Descripción: "Proyecto de desarrollo"
   - Fecha inicio: 2024-12-31 (formato AAAA-MM-DD)
   - Presupuesto: 5000 (en euros €)

2. Click "Crear Proyecto"

3. ✅ Aparece en la lista automáticamente
```

#### **Eliminar Proyecto:**
```
- Click en el botón 🗑️ junto al proyecto
- Se elimina completamente de la base de datos
```

**Validaciones:**
- ❌ Fecha incorrecta → "Formato de fecha inválido. Use AAAA-MM-DD"
- ✅ Presupuesto en € (permite decimales)

---

### **3. 👥 EMPLEADOS**

#### **Crear Empleado:**
```
1. Llenar formulario:
   - Email: nuevo@empresa.com
   - Contraseña: password123
   - Nombre: Juan
   - Apellidos: Pérez
   - Rol: desarrollador / diseñador / admin

2. Click "Crear Empleado"
```

#### **Ver Información del Empleado:**

Cada tarjeta muestra:
- 📧 Email
- 👔 Rol
- ⏰ **Horas este mes** (en grande, color destacado)
- 📁 Proyectos asignados
- ✅ Tareas totales

#### **Eliminar Empleado:**
```
- Click en botón 🗑️
- Se elimina completamente de la BD
```

---

### **4. ✅ TAREAS**

#### **Crear Tarea:**

**Paso 1:** Copiar IDs de las listas
```
📁 Proyectos Disponibles
   Nombre - Cliente
   ID: abc123... (copiar este ID)

👥 Empleados Disponibles
   Juan Pérez (desarrollador)
   ID: xyz789... (copiar este ID)
```

**Paso 2:** Crear la tarea
```
1. Pegar ID del proyecto
2. Pegar ID del empleado
3. Título: "Implementar login"
4. Descripción: "Crear sistema de autenticación"
5. Prioridad: alta / media / baja
6. Fecha vencimiento: 2024-12-31 (AAAA-MM-DD)
7. Click "Crear Tarea"
```

#### **Eliminar Tarea:**
```
- Click en botón 🗑️ junto a la tarea
- Se elimina completamente
```

**Validaciones:**
- ❌ ID inválido → "ID de proyecto/empleado inválido"
- ❌ Fecha incorrecta → "Formato de fecha inválido"

---

### **5. ⏰ JORNADAS**

Vista de todas las jornadas laborales:
- Empleado que registró
- Proyecto asociado
- Fecha y horas trabajadas
- Descripción de actividades

---

## 👷 Dashboard de Empleados

**Acceso:** `http://localhost:3000/empleados`  
**Credenciales:** juan@pylink.com / emp123

### **4 Secciones:**

---

### **1. 📊 RESUMEN**

Muestra:
- Proyectos asignados
- Tareas pendientes
- Horas trabajadas este mes

---

### **2. 📁 MIS PROYECTOS**

Lista de proyectos asignados con:
- Nombre del proyecto
- Cliente
- Estado
- Descripción

---

### **3. ✅ MIS TAREAS**

Lista de tareas asignadas:
- Título
- Estado (pendiente/en progreso/completada)
- Prioridad (alta/media/baja)
- Fecha de vencimiento
- Proyecto asociado

**Cambiar estado:**
```
- Click en el botón de estado
- Cambia: pendiente → en progreso → completada
```

---

### **4. ⏰ REGISTRAR JORNADA**

#### **Iniciar Jornada:**
```
1. Si hay proyectos asignados → Click "Iniciar Jornada"
2. Se registra la hora de inicio
3. El botón cambia a "Finalizar Jornada"
```

#### **Finalizar Jornada:**
```
1. Agregar descripción de actividades
2. Click "Finalizar Jornada"
3. Se calcula automáticamente las horas trabajadas
4. Aparece en el historial
```

#### **Historial:**
Lista de jornadas previas con:
- Fecha
- Horas trabajadas
- Proyecto
- Descripción

---

## 📝 Formatos y Validaciones

### **Formato de Fechas**
```
✅ Correcto: 2024-12-31
✅ Correcto: 2025-01-15

❌ Incorrecto: 31/12/2024
❌ Incorrecto: 12-31-2024
❌ Incorrecto: 31-12-2024
```

**Formato requerido:** `AAAA-MM-DD`
- AAAA = Año (4 dígitos)
- MM = Mes (01-12)
- DD = Día (01-31)

### **Presupuestos**
```
✅ Correcto: 5000 (entero)
✅ Correcto: 5000.50 (con decimales)
✅ Correcto: 15000

Unidad: Euros (€)
```

### **IDs de Proyecto/Empleado**
```
Los IDs son UUIDs generados automáticamente:
- Formato: abc12345-6789-0123-4567-890abcdef123
- Copiar desde las listas mostradas en el formulario
- No editar manualmente
```

---

## ❓ Preguntas Frecuentes

### **¿Cómo agrego un empleado a un proyecto?**
```
Actualmente se hace automáticamente al:
1. Crear una tarea asignada a ese empleado en ese proyecto
2. El empleado verá el proyecto en su dashboard
```

### **¿Puedo recuperar algo eliminado?**
```
No. Las eliminaciones son permanentes (hard delete).
- No hay papelera de reciclaje
- No se puede deshacer
- Asegúrate antes de eliminar
```

### **¿Cómo cambio la contraseña de un empleado?**
```
Actualmente no hay UI para esto.
Usa el script: python scripts/fix_passwords.py
```

### **¿Puedo ver las horas de un empleado específico?**
```
Sí, en el panel de administración:
1. Tab "Empleados"
2. Busca el empleado
3. Verás "⏰ Horas este mes: X.Xh"
```

### **¿Qué pasa si pongo una fecha en formato incorrecto?**
```
El sistema mostrará un error:
"❌ Formato de fecha inválido. Use AAAA-MM-DD (ej: 2024-12-31)"

No se creará el proyecto/tarea hasta corregir el formato.
```

### **¿Puedo asignar múltiples empleados a un proyecto?**
```
Sí:
1. Crea tareas en el proyecto para cada empleado
2. Cada empleado verá el proyecto en su dashboard
```

### **¿Cómo veo todas las jornadas de un empleado?**
```
Panel Admin → Tab "Jornadas"
→ Filtra por empleado (muestra nombre en cada registro)
```

---

## 🎯 Flujo de Trabajo Recomendado

### **Para Administradores:**

```
1. Crear Empleados
   ↓
2. Crear Proyectos (con presupuesto en €)
   ↓
3. Crear Tareas (asignar empleados)
   ↓
4. Monitorear progreso en "Resumen"
   ↓
5. Ver horas trabajadas en "Empleados"
```

### **Para Empleados:**

```
1. Login
   ↓
2. Ver proyectos y tareas asignadas
   ↓
3. Iniciar jornada
   ↓
4. Trabajar en tareas
   ↓
5. Finalizar jornada con descripción
   ↓
6. Actualizar estado de tareas
```

---

## 💡 Consejos y Buenas Prácticas

### **Al crear proyectos:**
- ✅ Usa nombres descriptivos
- ✅ Asegúrate del presupuesto correcto (en €)
- ✅ Verifica la fecha de inicio

### **Al crear tareas:**
- ✅ Copia el ID completo (no edites)
- ✅ Usa prioridades coherentes
- ✅ Establece fechas realistas
- ✅ Describe bien la tarea

### **Al registrar jornadas:**
- ✅ Describe las actividades realizadas
- ✅ Registra cada día trabajado
- ✅ Finaliza la jornada antes de cerrar

---

## 🆘 Solución de Problemas

### **"No puedo crear una tarea"**
```
Verifica:
- ✅ Has copiado el ID completo del proyecto
- ✅ Has copiado el ID completo del empleado
- ✅ La fecha está en formato AAAA-MM-DD
- ✅ Todos los campos obligatorios están llenos
```

### **"No veo mis proyectos"**
```
Verifica:
- ✅ Has iniciado sesión con tus credenciales
- ✅ El admin te ha asignado tareas en proyectos
- ✅ Los proyectos no están eliminados
```

### **"No puedo iniciar jornada"**
```
Verifica:
- ✅ Tienes al menos un proyecto asignado
- ✅ No tienes otra jornada activa
```

---

## 📞 Soporte

Para problemas técnicos o dudas:
- Consulta [GUIA_DESARROLLADOR.md](GUIA_DESARROLLADOR.md) para información técnica
- Consulta [CHANGELOG.md](CHANGELOG.md) para cambios recientes

---

**✨ ¡Disfruta usando PyLink!**
