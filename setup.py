"""
Script de configuración para PyEnterprise
"""

import subprocess
import sys
import os

def run_command(command):
    """Ejecutar comando y mostrar output."""
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Éxito: {command}")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Error en: {command}")
        if result.stderr:
            print(result.stderr)
    return result.returncode == 0

def setup_project():
    """Configurar el proyecto PyEnterprise."""
    print("🚀 Configurando PyEnterprise...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detectado")
    
    # Instalar dependencias
    if not run_command("pip install -r requirements.txt"):
        print("❌ Error instalando dependencias")
        return False
    
    # Inicializar Reflex
    if not run_command("reflex init"):
        print("❌ Error inicializando Reflex")
        return False
    
    # Crear archivo .env si no existe
    if not os.path.exists(".env"):
        print("📄 Creando archivo .env desde .env.example...")
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Archivo .env creado. Puedes editarlo con tu configuración.")
        else:
            print("⚠️ Archivo .env.example no encontrado.")
    
    print("\n🎉 ¡PyEnterprise configurado correctamente!")
    print("\n📋 Pasos siguientes:")
    print("1. Personaliza el contenido en los componentes")
    print("2. Añade tu logo en assets/logo.png")
    print("3. Ejecuta 'reflex run' para iniciar el servidor")
    print("4. Visita http://localhost:3000")
    
    return True

if __name__ == "__main__":
    setup_project()
