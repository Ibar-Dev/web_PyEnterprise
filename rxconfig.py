import reflex as rx

config = rx.Config(
    app_name="pyenterprise",
    db_url="sqlite:///pyenterprise.db",
    env=rx.Env.DEV,
    port=3000,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    # Configuración de viewport para responsive design
    meta=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"},
        {"name": "theme-color", "content": "#3B82F6"},
        {"name": "apple-mobile-web-app-capable", "content": "yes"},
        {"name": "apple-mobile-web-app-status-bar-style", "content": "black-translucent"},
    ]
)
