#!/usr/bin/env python3
"""
Script para asignar al administrador a un proyecto
"""

import sys
from pathlib import Path
# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyenterprise.database import *

print("🔧 Asignando administrador a proyectos...")

# Obtener admin
admin = login_empleado("admin@pylink.com", "admin123")
if not admin:
    print("❌ No se encontró el admin")
    exit(1)

admin_id = admin['id']
print(f"✅ Admin encontrado: {admin['nombre']} ({admin_id})")

# Obtener o crear proyecto para admin
proyectos = obtener_todos_proyectos()
if not proyectos or len(proyectos) == 0:
    print("📁 Creando proyecto de administración...")
    proyecto = crear_proyecto(
        nombre="Administración del Sistema",
        descripcion="Proyecto para tareas administrativas",
        cliente="PyLink Interno",
        fecha_inicio="2024-01-01",
        presupuesto_horas=1000
    )
    if proyecto:
        print(f"✅ Proyecto creado: {proyecto['nombre']}")
        proyecto_id = proyecto['id']
    else:
        print("❌ Error creando proyecto")
        exit(1)
else:
    # Usar el primer proyecto disponible
    proyecto = proyectos[0]
    proyecto_id = proyecto['id']
    print(f"✅ Usando proyecto existente: {proyecto['nombre']}")

# Asignar admin al proyecto
resultado = asignar_empleado_proyecto(
    empleado_id=admin_id,
    proyecto_id=proyecto_id,
    rol_en_proyecto="administrador"
)

if resultado:
    print(f"✅ Admin asignado al proyecto correctamente")
    print(f"\n🎉 El administrador ahora puede:")
    print(f"   - Iniciar jornadas en el proyecto: {proyecto['nombre']}")
    print(f"   - Registrar horas de trabajo")
else:
    print("❌ Error al asignar admin al proyecto")

# Verificar
proyectos_admin = obtener_proyectos_empleado(admin_id)
print(f"\n📊 Proyectos del admin: {len(proyectos_admin)}")
for p in proyectos_admin:
    print(f"   - {p['nombre']}")
