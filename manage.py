#!/usr/bin/env python3
"""
Script de gestión para PyEnterprise
"""

import sys
import argparse
from pyenterprise.utils.database import init_database, reset_database, backup_database


def run_server():
    """Ejecutar el servidor de desarrollo."""
    import subprocess
    print("🚀 Iniciando servidor PyEnterprise...")
    subprocess.run(["reflex", "run"], check=True)


def init_db():
    """Inicializar base de datos."""
    print("🔧 Inicializando base de datos...")
    init_database()


def reset_db():
    """Resetear base de datos."""
    print("⚠️ Reseteando base de datos...")
    confirm = input("¿Estás seguro? Esta acción eliminará todos los datos (y/N): ")
    if confirm.lower() in ['y', 'yes', 's', 'si']:
        reset_database()
    else:
        print("❌ Operación cancelada")


def backup_db():
    """Crear backup de la base de datos."""
    print("💾 Creando backup de la base de datos...")
    backup_database()


def install_deps():
    """Instalar dependencias."""
    import subprocess
    print("📦 Instalando dependencias...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)


def upgrade_reflex():
    """Actualizar Reflex."""
    import subprocess
    print("⬆️ Actualizando Reflex...")
    subprocess.run([sys.executable, "-m", "pip", "install", "reflex", "--upgrade"], check=True)


def main():
    parser = argparse.ArgumentParser(description="Gestor de PyEnterprise")
    parser.add_argument("command", choices=[
        "runserver", "init-db", "reset-db", "backup-db", 
        "install", "upgrade-reflex"
    ], help="Comando a ejecutar")
    
    args = parser.parse_args()
    
    commands = {
        "runserver": run_server,
        "init-db": init_db,
        "reset-db": reset_db,
        "backup-db": backup_db,
        "install": install_deps,
        "upgrade-reflex": upgrade_reflex,
    }
    
    try:
        commands[args.command]()
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
