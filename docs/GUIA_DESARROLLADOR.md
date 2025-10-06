# 💻 Guía de Desarrollador - PyLink

Documentación técnica para desarrolladores trabajando en PyLink.

---

## 📋 Contenido

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Backend (supabase_client.py)](#backend)
3. [Frontend (Componentes Reflex)](#frontend)
4. [Base de Datos](#base-de-datos)
5. [Testing](#testing)
6. [Scripts Auxiliares](#scripts-auxiliares)
7. [Contribuir](#contribuir)

---

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
│
├── pyenterprise/                  # 💻 Código principal
│   │
│   ├── database/                  # 🗄️ BACKEND
│   │   ├── __init__.py            # Exports de funciones
│   │   └── supabase_client.py     # ⭐ ARCHIVO PRINCIPAL DEL BACKEND
│   │
│   ├── components/                # 🎨 FRONTEND (Componentes Reflex)
│   │   ├── admin_panel_profesional.py
│   │   │   └── AdminPanelState         # Estado del panel admin
│   │   │   └── admin_panel()           # Componente principal
│   │   │
│   │   ├── employee_dashboard_integrated.py
│   │   │   └── EmployeeDashboardState  # Estado del dashboard
│   │   │   └── employee_dashboard()    # Componente principal
│   │   │
│   │   ├── employee_auth.py
│   │   │   └── EmployeeAuthState       # Estado de autenticación
│   │   │   └── employee_login_page()   # Página de login
│   │   │
│   │   └── ... (otros componentes)
│   │
│   ├── services/                  # 🔧 Lógica de negocio (futuro)
│   ├── models/                    # 📊 Modelos de datos (futuro)
│   ├── utils/                     # 🛠️ Utilidades
│   │
│   ├── pyenterprise.py            # 🚀 App principal (Definición de rutas)
│   └── styles.py                  # 🎨 Estilos globales (COLORS, FONTS, etc.)
│
├── docs/                          # 📄 Documentación
├── tests/                         # 🧪 Tests
├── scripts/                       # 🛠️ Scripts auxiliares
│
├── app.py                         # Entry point
├── requirements.txt               # Dependencias
└── rxconfig.py                    # Config Reflex
```

---

## 🗄️ Backend

### **Archivo Principal: `pyenterprise/database/supabase_client.py`**

**Tamaño:** 27KB  
**Responsabilidad:** Toda la lógica de acceso a datos.

---

### **📦 Funciones por Categoría**

#### **🔐 Autenticación**
```python
def login_empleado(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Autentica un empleado con email y password.
    - Usa bcrypt para verificar password
    - Retorna datos del empleado si éxito
    - Retorna None si falla
    """

def crear_empleado(email: str, password: str, nombre: str, 
                   apellidos: str, rol: str) -> Optional[Dict[str, Any]]:
    """
    Crea un nuevo empleado.
    - Hash de password con bcrypt
    - Rol: 'admin', 'desarrollador', 'diseñador', etc.
    - Retorna empleado creado o None
    """
```

---

#### **📁 Proyectos**
```python
def crear_proyecto(nombre: str, descripcion: str, cliente: str,
                   fecha_inicio: str, presupuesto: float = 0.0) -> Optional[Dict[str, Any]]:
    """
    Crea un nuevo proyecto.
    - Valida formato de fecha (AAAA-MM-DD)
    - presupuesto en € (float)
    - Retorna proyecto creado o None si error
    """

def obtener_todos_proyectos() -> List[Dict[str, Any]]:
    """Retorna lista de todos los proyectos."""

def obtener_proyecto_por_id(proyecto_id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un proyecto específico por UUID."""

def actualizar_proyecto(proyecto_id: str, datos: Dict) -> bool:
    """Actualiza un proyecto existente."""

def eliminar_proyecto(proyecto_id: str) -> bool:
    """
    Elimina un proyecto COMPLETAMENTE (hard delete).
    - Elimina primero relaciones en proyecto_empleado
    - Luego elimina el proyecto
    """

def asignar_empleado_proyecto(empleado_id: str, proyecto_id: str,
                               rol_en_proyecto: str = "colaborador") -> Optional[Dict]:
    """Asigna un empleado a un proyecto."""
```

---

#### **✅ Tareas**
```python
def crear_tarea(proyecto_id: str, empleado_asignado_id: str, titulo: str,
                descripcion: str, prioridad: str, fecha_vencimiento: str) -> Optional[Dict]:
    """
    Crea una nueva tarea.
    - Valida formato de fecha (AAAA-MM-DD)
    - Valida UUIDs de proyecto y empleado
    - prioridad: 'alta', 'media', 'baja'
    - Retorna tarea creada o None
    """

def obtener_todas_tareas() -> List[Dict[str, Any]]:
    """Lista todas las tareas del sistema."""

def obtener_tareas_empleado(empleado_id: str) -> List[Dict[str, Any]]:
    """Tareas asignadas a un empleado específico."""

def actualizar_estado_tarea(tarea_id: str, nuevo_estado: str) -> bool:
    """
    Actualiza estado de tarea.
    - estados: 'pendiente', 'en_progreso', 'completada'
    """

def eliminar_tarea(tarea_id: str) -> bool:
    """Elimina tarea completamente (hard delete)."""
```

---

#### **👥 Empleados**
```python
def obtener_todos_empleados() -> List[Dict[str, Any]]:
    """Lista todos los empleados."""

def obtener_empleado_por_id(empleado_id: str) -> Optional[Dict[str, Any]]:
    """Obtiene empleado por UUID."""

def eliminar_empleado(empleado_id: str) -> bool:
    """
    Elimina empleado completamente (hard delete).
    - Elimina primero relaciones en proyecto_empleado
    """

def obtener_empleados_con_estadisticas() -> List[Dict[str, Any]]:
    """
    Retorna empleados con estadísticas:
    - horas_mes_actual
    - total_proyectos
    - total_tareas
    """
```

---

#### **⏰ Jornadas**
```python
def registrar_jornada(empleado_id: str, proyecto_id: str, fecha: str,
                     hora_inicio: str, hora_fin: str, descripcion: str) -> Optional[Dict]:
    """
    Registra una jornada laboral.
    - Valida UUIDs de empleado y proyecto
    - Calcula automáticamente horas_trabajadas
    - Formato hora: ISO 8601
    """

def obtener_jornadas_empleado(empleado_id: str, fecha_inicio: Optional[str] = None,
                               fecha_fin: Optional[str] = None) -> List[Dict]:
    """Jornadas de un empleado con filtro opcional de fechas."""

def obtener_todas_jornadas() -> List[Dict[str, Any]]:
    """Todas las jornadas del sistema con joins a empleados y proyectos."""

def calcular_horas_totales_empleado(empleado_id: str, fecha_inicio: Optional[str] = None,
                                    fecha_fin: Optional[str] = None) -> float:
    """Suma total de horas trabajadas."""

def calcular_horas_mensuales_empleado(empleado_id: str) -> float:
    """Horas trabajadas en el mes actual."""
```

---

#### **📊 Estadísticas**
```python
def obtener_estadisticas_sistema() -> Dict[str, Any]:
    """
    Estadísticas generales:
    - total_proyectos
    - total_empleados
    - total_tareas
    - horas_totales
    """

def obtener_resumen_dashboard_admin() -> Dict[str, Any]:
    """Resumen para el dashboard del admin."""

def obtener_estadisticas_proyecto(proyecto_id: str) -> Dict[str, Any]:
    """Estadísticas de un proyecto específico."""
```

---

### **🔧 Características Técnicas del Backend**

#### **Validaciones:**
```python
# Validación de fechas
try:
    datetime.strptime(fecha, '%Y-%m-%d')
except ValueError:
    print("❌ Error: Formato de fecha inválido")
    return None

# Validación de UUIDs
if not empleado_id or len(empleado_id) < 30:
    print("❌ Error: UUID inválido")
    return None
```

#### **Manejo de Errores:**
```python
try:
    # Operación de BD
    response = client.table('proyectos').insert(...).execute()
    return response.data[0]
except Exception as e:
    print(f"Error en crear_proyecto: {e}")
    return None
```

#### **Hard Delete (Eliminación Completa):**
```python
def eliminar_proyecto(proyecto_id: str) -> bool:
    # 1. Eliminar relaciones primero
    client.table('proyecto_empleado').delete().eq('proyecto_id', proyecto_id).execute()
    
    # 2. Eliminar el proyecto
    response = client.table('proyectos').delete().eq('id', proyecto_id).execute()
    
    return True
```

---

## 🎨 Frontend

### **Arquitectura de Componentes**

Los componentes de Reflex siguen este patrón:

```python
class MiComponenteState(rx.State):
    """Estado del componente."""
    
    # Variables de estado
    dato1: str = ""
    dato2: int = 0
    datos_lista: list = []
    
    # Métodos para modificar estado
    async def cargar_datos(self):
        """Cargar datos de backend."""
        from ..database import obtener_datos
        self.datos_lista = obtener_datos()
    
    def set_dato1(self, valor: str):
        """Setter para dato1."""
        self.dato1 = valor


def mi_componente() -> rx.Component:
    """Componente visual."""
    return rx.vstack(
        rx.input(value=MiComponenteState.dato1, on_change=MiComponenteState.set_dato1),
        rx.button("Cargar", on_click=MiComponenteState.cargar_datos),
        rx.foreach(MiComponenteState.datos_lista, lambda d: rx.text(d["nombre"]))
    )
```

---

### **Componentes Principales**

#### **1. Panel de Administración**
**Archivo:** `components/admin_panel_profesional.py`

```python
class AdminPanelState(rx.State):
    # Datos
    proyectos: list = []
    empleados: list = []
    tareas: list = []
    jornadas: list = []
    
    # Formularios
    proyecto_nombre: str = ""
    proyecto_cliente: str = ""
    proyecto_presupuesto: str = "0"
    # ... más campos
    
    # Métodos
    async def crear_nuevo_proyecto(self):
        """Crear proyecto llamando al backend."""
        resultado = crear_proyecto(
            nombre=self.proyecto_nombre,
            cliente=self.proyecto_cliente,
            presupuesto=float(self.proyecto_presupuesto),
            # ...
        )
        
        if resultado:
            self.success_message = "✅ Proyecto creado"
            await self.cargar_todos_datos()
```

#### **2. Dashboard de Empleados**
**Archivo:** `components/employee_dashboard_integrated.py`

```python
class EmployeeDashboardState(rx.State):
    empleado_actual: dict = {}
    proyectos: list = []
    tareas: list = []
    jornadas: list = []
    
    # Sistema de jornadas
    is_working: bool = False
    current_session: dict = {}
    
    async def start_work_session(self, proyecto_id: str = ""):
        """Iniciar jornada."""
        self.current_session = {
            "proyecto_id": proyecto_id,
            "start_time": datetime.now().isoformat(),
            "description": ""
        }
        self.is_working = True
```

#### **3. Sistema de Autenticación**
**Archivo:** `components/employee_auth.py`

```python
class EmployeeAuthState(rx.State):
    email: str = ""
    password: str = ""
    error_message: str = ""
    
    def login(self):
        """Login y redirección."""
        empleado = login_empleado(self.email, self.password)
        
        if empleado:
            # Redirigir según rol
            if empleado['rol'] == 'admin':
                return rx.redirect("/admin")
            else:
                return rx.redirect("/empleados/dashboard")
        else:
            self.error_message = "❌ Credenciales inválidas"
```

---

## 💾 Base de Datos

### **Esquema Principal**

```sql
-- Tabla: empleados
CREATE TABLE empleados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT,
    rol TEXT DEFAULT 'empleado',
    activo BOOLEAN DEFAULT true,
    fecha_ingreso TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: proyectos
CREATE TABLE proyectos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cliente TEXT,
    fecha_inicio DATE,
    presupuesto_horas INTEGER,  -- Usado para presupuesto en €
    estado TEXT DEFAULT 'activo',
    progreso INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: tareas
CREATE TABLE tareas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID REFERENCES proyectos(id),
    empleado_asignado_id UUID REFERENCES empleados(id),
    titulo TEXT NOT NULL,
    descripcion TEXT,
    prioridad TEXT DEFAULT 'media',
    estado TEXT DEFAULT 'pendiente',
    fecha_vencimiento DATE,
    horas_estimadas FLOAT DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Tabla: jornadas
CREATE TABLE jornadas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empleado_id UUID REFERENCES empleados(id),
    proyecto_id UUID REFERENCES proyectos(id),
    fecha DATE NOT NULL,
    hora_inicio TIMESTAMP,
    hora_fin TIMESTAMP,
    horas_trabajadas FLOAT,
    descripcion TEXT,
    estado TEXT DEFAULT 'completada',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: proyecto_empleado (relación muchos a muchos)
CREATE TABLE proyecto_empleado (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID REFERENCES proyectos(id),
    empleado_id UUID REFERENCES empleados(id),
    rol_en_proyecto TEXT DEFAULT 'colaborador',
    activo BOOLEAN DEFAULT true,
    fecha_asignacion TIMESTAMP DEFAULT NOW(),
    UNIQUE(proyecto_id, empleado_id)
);
```

---

## 🧪 Testing

### **Tests Disponibles**

**Ubicación:** `tests/`

#### **1. Test Completo del Backend**
```bash
python tests/test_backend_completo.py
```

**Prueba:**
- ✅ Autenticación
- ✅ CRUD de proyectos
- ✅ CRUD de empleados
- ✅ CRUD de tareas
- ✅ Registro de jornadas
- ✅ Estadísticas

#### **2. Test de Login**
```bash
python tests/test_login.py
```

**Prueba:**
- ✅ Login de admin
- ✅ Login de empleados
- ✅ Manejo de credenciales inválidas

#### **3. Test de Sistema Completo**
```bash
python tests/test_sistema_completo.py
```

**Prueba integración completa.**

---

### **Crear Nuevos Tests**

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyenterprise.database import *

# Test
print("🧪 Probando función...")
resultado = mi_funcion()
assert resultado is not None, "❌ Falló"
print("✅ Test exitoso")
```

---

## 🛠️ Scripts Auxiliares

**Ubicación:** `scripts/`

### **1. Agregar Datos de Prueba**
```bash
python scripts/agregar_datos_prueba.py
```

Crea:
- 3 proyectos de ejemplo
- Tareas asignadas
- Relaciones empleado-proyecto

### **2. Asignar Admin a Proyecto**
```bash
python scripts/asignar_admin_proyecto.py
```

Asigna al administrador a un proyecto para que pueda registrar jornadas.

### **3. Actualizar Contraseñas**
```bash
python scripts/fix_passwords.py
```

Actualiza passwords de empleados si es necesario.

---

## 🔄 Flujo de Desarrollo

### **Agregar Nueva Funcionalidad**

#### **1. Backend (Base de Datos)**
```python
# pyenterprise/database/supabase_client.py

def mi_nueva_funcion(param1: str) -> Optional[Dict]:
    """Descripción de la función."""
    try:
        client = get_supabase_client()
        response = client.table('mi_tabla').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error: {e}")
        return None
```

#### **2. Exportar Función**
```python
# pyenterprise/database/__init__.py

from .supabase_client import (
    # ... funciones existentes
    mi_nueva_funcion,  # Agregar aquí
)

__all__ = [
    # ... lista existente
    'mi_nueva_funcion',  # Agregar aquí
]
```

#### **3. Frontend (Componente)**
```python
# pyenterprise/components/mi_componente.py

from ..database import mi_nueva_funcion

class MiState(rx.State):
    datos: list = []
    
    async def cargar_datos(self):
        self.datos = mi_nueva_funcion()

def mi_componente():
    return rx.vstack(
        rx.button("Cargar", on_click=MiState.cargar_datos),
        rx.foreach(MiState.datos, lambda d: rx.text(d))
    )
```

#### **4. Ruta (App Principal)**
```python
# pyenterprise/pyenterprise.py

from .components.mi_componente import mi_componente

# Agregar ruta
app.add_page(mi_componente, route="/mi-ruta")
```

---

## 📦 Dependencias

**Archivo:** `requirements.txt`

```txt
reflex>=0.4.0
supabase>=2.0.0
bcrypt>=4.0.0
python-dotenv>=1.0.0
```

---

## 🚀 Comandos de Desarrollo

```bash
# Iniciar en modo desarrollo
reflex run

# Compilar para producción
reflex export

# Limpiar cache
rm -rf .web __pycache__ pyenterprise/__pycache__
```

---

## 📝 Estándares de Código

### **Nomenclatura:**
- **Funciones:** `snake_case` (ej: `obtener_proyectos`)
- **Classes:** `PascalCase` (ej: `AdminPanelState`)
- **Variables:** `snake_case` (ej: `proyecto_nombre`)
- **Constantes:** `UPPER_CASE` (ej: `COLORS`, `MAX_ITEMS`)

### **Documentación:**
```python
def mi_funcion(param1: str, param2: int) -> Optional[Dict]:
    """
    Descripción breve de la función.
    
    Args:
        param1: Descripción del parámetro
        param2: Descripción del parámetro
    
    Returns:
        Dict con datos o None si error
    """
    pass
```

### **Imports:**
```python
# Standard library
import sys
from pathlib import Path
from datetime import datetime

# Third party
import reflex as rx
from supabase import create_client

# Local
from ..database import obtener_datos
from ..styles import COLORS
```

---

## 🐛 Debugging

### **Ver logs de Reflex:**
```bash
# Los logs aparecen en la terminal donde ejecutaste reflex run
```

### **Debug de funciones de BD:**
```python
# Agregar prints en supabase_client.py
def mi_funcion():
    print(f"✅ Entrando a mi_funcion")
    resultado = ...
    print(f"📊 Resultado: {resultado}")
    return resultado
```

### **Inspeccionar estado en frontend:**
```python
# En el componente
rx.text(f"Debug: {MiState.mi_variable}")
```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📚 Recursos Adicionales

- **Reflex Docs:** https://reflex.dev/docs/
- **Supabase Docs:** https://supabase.com/docs
- **Python Docs:** https://docs.python.org/3/

---

**🎯 Happy Coding!**
