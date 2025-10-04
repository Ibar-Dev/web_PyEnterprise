#!/usr/bin/env python3
"""
Script para verificar la conexión con Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path para importar nuestros módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pyenterprise.database.supabase_client import get_supabase_client, login_empleado

    print("🔍 Verificando conexión con Supabase...")

    # Intentar obtener el cliente
    client = get_supabase_client()
    print("✅ Cliente de Supabase creado exitosamente")

    # Intentar hacer una consulta simple
    print("\n🔍 Probando consulta de empleados...")

    # Probar login con credenciales conocidas
    empleado = login_empleado("juan@pylink.com", "emp123")

    if empleado:
        print("✅ Login exitoso!")
        print(f"   👤 Empleado: {empleado['nombre']} {empleado.get('apellidos', '')}")
        print(f"   📧 Email: {empleado['email']}")
        print(f"   🏷️  Rol: {empleado['rol']}")
        print(f"   🆔 ID: {empleado['id']}")
    else:
        print("❌ Error en login - credenciales incorrectas o problema de conexión")

    # Probar consulta directa a la tabla empleados
    print("\n🔍 Probando consulta directa...")
    response = client.table('empleados').select('id, nombre, email, rol').limit(3).execute()

    if response.data:
        print("✅ Consulta directa exitosa!")
        print("   📊 Empleados en la base de datos:")
        for emp in response.data:
            print(f"      - {emp['nombre']} ({emp['email']}) - {emp['rol']}")
    else:
        print("❌ No se pudieron obtener empleados")

    print("\n🎉 ¡Conexión con Supabase verificada exitosamente!")

except Exception as e:
    print(f"❌ Error en la conexión: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    import traceback
    traceback.print_exc()
