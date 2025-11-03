import reflex as rx
import os

# Obtener configuración de variables de entorno
supabase_url = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
supabase_key = os.getenv("SUPABASE_KEY", "your-anon-key")

config = rx.Config(
    app_name="pyenterprise",
    # Usar variables de entorno para la base de datos
    db_url=os.getenv("DATABASE_URL", "sqlite:///pyenterprise.db"),
    env=rx.Env.DEV,
    port=3000,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    # Configuración de viewport para responsive design
    meta=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"},
        {"name": "theme-color", "content": "#2563eb"},
        {"name": "apple-mobile-web-app-capable", "content": "yes"},
        {"name": "apple-mobile-web-app-status-bar-style", "content": "black-translucent"},
    ],
    # Configuración de frontend
    frontend_packages=[
        "tailwindcss",
    ],
)
