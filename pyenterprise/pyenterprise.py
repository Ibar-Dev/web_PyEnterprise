"""
PyLink - Página web empresarial desarrollada con Reflex
Empresa de desarrollo de software con enfoque moderno y tecnológico
"""

import reflex as rx
from .styles import *
from .components.navbar import navbar
from .components.hero import hero_section
from .components.about import about_section
from .components.team import team_section
from .components.footer import footer
from .components.employee_auth import employee_login_page, EmployeeAuthState
from .components.employee_dashboard_integrated import employee_dashboard
from .components.admin_panel_profesional import admin_panel
from .components.cookie_banner import cookie_banner
from .pages.privacy import privacy_policy
from .pages.cookies import cookies_policy
from .pages.terms import terms_page
from .pages.services import services_page
from .pages.contact import contact_page
from .performance import resource_hints
from .security import SECURITY_HEADERS




def index() -> rx.Component:
    """Página principal llamativa de PyLink."""
    return rx.box(
        # Resource hints para rendimiento
        resource_hints(),
        
        # Componentes principales
        navbar(),
        hero_section(), 
        about_section(),
        team_section(),
        footer(),
        
        # Banner de cookies (GDPR compliance)
        cookie_banner(),
        
        width="100%",
        margin="0",
        padding="0",
        # Efectos de background
        background=f"""
            linear-gradient(135deg, {COLORS['background']} 0%, {COLORS['surface']} 100%),
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%)
        """,
        background_attachment="fixed",
    )

def empleados_login() -> rx.Component:
    """Página de login para empleados."""
    return employee_login_page()


def admin_dashboard_page() -> rx.Component:
    """Página del panel de administración."""
    return admin_panel()



# Configuración de la aplicación
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "/cards.css",  # CSS personalizado para las tarjetas
        "/responsive.css",  # CSS responsive global
    ],
    head_components=[
        rx.el.link(
            rel="icon",
            type_="image/png",
            href="/logopylink.png",
        ),
    ],
)

# Rutas de la aplicación
app.add_page(index, route="/", title="PyLink - Conectando tu negocio con el futuro digital")
app.add_page(empleados_login, route="/empleados", title="PyLink - Login Empleados")
app.add_page(employee_dashboard, route="/empleados/dashboard", title="PyLink - Dashboard")
app.add_page(admin_dashboard_page, route="/admin", title="PyLink - Panel de Administración")

# Rutas de políticas legales
app.add_page(privacy_policy, route="/privacidad", title="PyLink - Política de Privacidad")
app.add_page(cookies_policy, route="/cookies", title="PyLink - Política de Cookies")
app.add_page(terms_page, route="/terminos", title="PyLink - Términos y Condiciones")

# Rutas de servicios
app.add_page(services_page, route="/servicios", title="PyLink - Nuestros Servicios")

# Rutas de contacto
app.add_page(contact_page, route="/contacto", title="PyLink - Contacto")

# La aplicación está lista para ejecutarse con seguridad y rendimiento optimizados
