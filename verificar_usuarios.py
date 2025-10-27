"""
Script para verificar que los usuarios existen en Supabase
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
from pyenterprise.database import get_supabase_client

load_dotenv()

def verificar_usuarios():
    """Verificar usuarios en la base de datos"""
    
    print("🔍 Verificando usuarios en Supabase...")
    print("-" * 60)
    
    try:
        client = get_supabase_client()
        
        # Obtener todos los empleados
        response = client.table('empleados').select('email, nombre, apellidos, rol, activo').execute()
        
        if response.data:
            print(f"\n✅ {len(response.data)} usuarios encontrados:\n")
            
            for i, emp in enumerate(response.data, 1):
                estado = "🟢 ACTIVO" if emp['activo'] else "🔴 INACTIVO"
                print(f"{i}. {emp['email']}")
                print(f"   Nombre: {emp['nombre']} {emp.get('apellidos', '')}")
                print(f"   Rol: {emp['rol']}")
                print(f"   Estado: {estado}")
                print()
        else:
            print("❌ No se encontraron usuarios en la base de datos")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_usuarios()
