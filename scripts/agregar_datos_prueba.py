#!/usr/bin/env python3
"""
Script para agregar datos de prueba al sistema
"""

import sys
from pathlib import Path
# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyenterprise.database.supabase_client import (
    crear_proyecto,
    crear_tarea,
    asignar_empleado_proyecto,
    get_supabase_client
)

print("🚀 Agregando datos de prueba al sistema...")
print("=" * 50)

# Obtener IDs de empleados existentes
client = get_supabase_client()
empleados = client.table('empleados').select('id, nombre, email').execute()

if not empleados.data:
    print("❌ No hay empleados en la base de datos")
    exit(1)

print(f"\n📋 Empleados encontrados: {len(empleados.data)}")
for emp in empleados.data:
    print(f"   - {emp['nombre']} ({emp['email']}): {emp['id']}")

# Crear proyectos de prueba
print("\n📁 Creando proyectos de prueba...")

proyectos_prueba = [
    {
        "nombre": "Sistema de Gestión Empresarial",
        "descripcion": "Desarrollo de sistema completo de gestión para empresa",
        "cliente": "Empresa ABC",
        "fecha_inicio": "2024-01-01",
        "presupuesto": 15000.0
    },
    {
        "nombre": "Aplicación Móvil de Ventas",
        "descripcion": "App móvil para gestión de ventas en campo",
        "cliente": "Comercial XYZ",
        "fecha_inicio": "2024-02-01",
        "presupuesto": 12000.0
    },
    {
        "nombre": "Portal Web Corporativo",
        "descripcion": "Sitio web corporativo con CMS integrado",
        "cliente": "Corporación 123",
        "fecha_inicio": "2024-03-01",
        "presupuesto": 8000.0
    }
]

proyectos_creados = []
for proyecto in proyectos_prueba:
    resultado = crear_proyecto(**proyecto)
    if resultado:
        proyectos_creados.append(resultado)
        print(f"   ✅ Proyecto creado: {proyecto['nombre']}")
    else:
        print(f"   ⚠️ No se pudo crear: {proyecto['nombre']} (puede que ya exista)")

# Obtener proyectos creados
proyectos_db = client.table('proyectos').select('id, nombre').execute()
print(f"\n📊 Proyectos en la base de datos: {len(proyectos_db.data)}")

# Asignar empleados a proyectos
if proyectos_db.data and empleados.data:
    print("\n👥 Asignando empleados a proyectos...")
    
    # Asignar cada empleado al primer proyecto
    for empleado in empleados.data:
        if empleado['email'] != 'admin@pylink.com':  # No asignar al admin
            for proyecto in proyectos_db.data[:2]:  # Asignar a los primeros 2 proyectos
                resultado = asignar_empleado_proyecto(empleado['id'], proyecto['id'])
                if resultado:
                    print(f"   ✅ {empleado['nombre']} asignado a '{proyecto['nombre']}'")

# Crear tareas de prueba
if proyectos_db.data and empleados.data:
    print("\n✅ Creando tareas de prueba...")
    
    tareas_prueba = [
        {
            "proyecto_id": proyectos_db.data[0]['id'],
            "empleado_asignado_id": empleados.data[1]['id'] if len(empleados.data) > 1 else empleados.data[0]['id'],
            "titulo": "Diseño de base de datos",
            "descripcion": "Crear el modelo de datos y esquema de BD",
            "prioridad": "alta",
            "fecha_vencimiento": "2024-12-31"
        },
        {
            "proyecto_id": proyectos_db.data[0]['id'],
            "empleado_asignado_id": empleados.data[1]['id'] if len(empleados.data) > 1 else empleados.data[0]['id'],
            "titulo": "Desarrollo de API REST",
            "descripcion": "Implementar endpoints de la API",
            "prioridad": "alta",
            "fecha_vencimiento": "2024-12-31"
        },
        {
            "proyecto_id": proyectos_db.data[1]['id'] if len(proyectos_db.data) > 1 else proyectos_db.data[0]['id'],
            "empleado_asignado_id": empleados.data[2]['id'] if len(empleados.data) > 2 else empleados.data[0]['id'],
            "titulo": "Diseño de interfaz de usuario",
            "descripcion": "Crear mockups y prototipos de la UI",
            "prioridad": "media",
            "fecha_vencimiento": "2024-12-31"
        },
    ]
    
    for tarea in tareas_prueba:
        resultado = crear_tarea(**tarea)
        if resultado:
            print(f"   ✅ Tarea creada: {tarea['titulo']}")
        else:
            print(f"   ⚠️ No se pudo crear: {tarea['titulo']}")

print("\n🎉 ¡Datos de prueba agregados exitosamente!")
print("\n💡 Ahora puedes:")
print("   1. Ver proyectos en el dashboard de empleados")
print("   2. Ver tareas asignadas")
print("   3. Registrar jornadas laborales")
print("   4. Gestionar todo desde el panel de admin")
print("\n🌐 Accede a: http://localhost:3000/empleados")
