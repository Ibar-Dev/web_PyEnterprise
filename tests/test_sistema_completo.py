#!/usr/bin/env python3
"""
Test rápido del sistema completo
"""

from pyenterprise.database.supabase_client import login_empleado, crear_empleado, crear_proyecto

print("🚀 Test del Sistema PyLink Completo")
print("=" * 50)

# Test 1: Login existente
print("\n1️⃣ Probando login existente...")
admin = login_empleado("admin@pylink.com", "admin123")
if admin:
    print(f"   ✅ Login exitoso: {admin['nombre']} ({admin['rol']})")
else:
    print("   ❌ Error en login")

# Test 2: Crear nuevo empleado
print("\n2️⃣ Creando nuevo empleado de prueba...")
try:
    nuevo_empleado = crear_empleado(
        email="test@empresa.com",
        password="test123",
        nombre="Empleado",
        apellidos="de Prueba",
        rol="desarrollador"
    )
    if nuevo_empleado:
        print("   ✅ Empleado creado exitosamente")
    else:
        print("   ❌ Error creando empleado")
except Exception as e:
    print(f"   ⚠️ Error (esperado si ya existe): {e}")

# Test 3: Crear proyecto
print("\n3️⃣ Creando proyecto de prueba...")
try:
    nuevo_proyecto = crear_proyecto(
        nombre="Proyecto de Test",
        descripcion="Proyecto creado para pruebas",
        cliente="Cliente Test",
        fecha_inicio="2024-01-01",
        presupuesto_horas=100
    )
    if nuevo_proyecto:
        print("   ✅ Proyecto creado exitosamente")
    else:
        print("   ❌ Error creando proyecto")
except Exception as e:
    print(f"   ⚠️ Error (esperado si ya existe): {e}")

print("\n🎉 Tests completados!")
print("\n💡 URLs disponibles:")
print("   🌐 Página principal: http://localhost:3000")
print("   🔐 Login empleados: http://localhost:3000/empleados")
print("   👤 Dashboard empleados: http://localhost:3000/empleados/dashboard")
print("   🔧 Panel admin: http://localhost:3000/admin")
print("\n📋 Credenciales de prueba:")
print("   👑 Admin: admin@pylink.com / admin123")
print("   👨 Empleado: juan@pylink.com / emp123")
print("   👩 Empleada: maria@pylink.com / emp123")
