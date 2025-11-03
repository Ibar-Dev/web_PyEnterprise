"""
Components bridge - Importación de componentes desde la estructura correcta
"""

# Importar todos los componentes desde pyenterprise.components
from pyenterprise.components.navbar import navbar
from pyenterprise.components.hero import hero_section
from pyenterprise.components.about import about_section
from pyenterprise.components.services import services_section
from pyenterprise.components.contact import contact_section
from pyenterprise.components.footer import footer

# Exportar para compatibilidad con app.py
__all__ = [
    'navbar',
    'hero_section',
    'about_section',
    'services_section',
    'contact_section',
    'footer'
]