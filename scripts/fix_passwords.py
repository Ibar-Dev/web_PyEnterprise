#!/usr/bin/env python3
"""
Script para actualizar las contraseñas de los empleados en Supabase
"""

import bcrypt
from pyenterprise.database.supabase_client import get_supabase_client, hash_password

# Contraseñas que queremos usar
passwords = {
    "juan@pylink.com": "emp123",
    "maria@pylink.com": "emp123",
    "admin@pylink.com": "admin123"
}

print("🔐 Generando hashes de contraseñas...")
print()

# Generar y mostrar los hashes
for email, password in passwords.items():
    hashed = hash_password(password)
    print(f"📧 {email}")
    print(f"🔑 Contraseña: {password}")
    print(f"🔒 Hash: {hashed}")
    print()

# Actualizar en la base de datos
print("📝 Actualizando contraseñas en Supabase...")
client = get_supabase_client()

for email, password in passwords.items():
    hashed = hash_password(password)
    
    try:
        response = client.table('empleados').update({
            'password_hash': hashed
        }).eq('email', email).execute()
        
        if response.data:
            print(f"✅ Contraseña actualizada para {email}")
        else:
            print(f"❌ No se pudo actualizar {email}")
    except Exception as e:
        print(f"❌ Error actualizando {email}: {e}")

print("\n🎉 ¡Contraseñas actualizadas! Ahora puedes usar:")
print("   - juan@pylink.com / emp123")
print("   - maria@pylink.com / emp123")
print("   - admin@pylink.com / admin123")
