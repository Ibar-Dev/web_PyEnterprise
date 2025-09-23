import reflex as rx

config = rx.Config(
    app_name="pyenterprise",  # Usar la estructura original que funcionaba
    db_url="sqlite:///pyenterprise.db",
    env=rx.Env.DEV,
    port=3000,
    # Deshabilitar el plugin sitemap para evitar warnings
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"]
)
