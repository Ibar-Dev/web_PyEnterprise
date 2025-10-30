"""
Generar SECRET_KEY segura para producción
"""
import secrets

print("🔐 Generando SECRET_KEY segura...")
print("=" * 60)
print()

# Generar una clave segura de 32 bytes (256 bits)
secret_key = secrets.token_urlsafe(32)

print("✅ SECRET_KEY generada:")
print()
print(f"SECRET_KEY={secret_key}")
print()
print("=" * 60)
print("📝 Copia esta línea y reemplázala en tu archivo .env")
print("⚠️  NO COMPARTAS esta clave con nadie")
print()
