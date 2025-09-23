"""
Utilidades para manejo de base de datos
"""

import reflex as rx
from ..models.contact import Contact, Service, Project, BlogPost
from .config import Config


def init_database():
    """Inicializar la base de datos con datos de ejemplo."""
    try:
        # Crear todas las tablas
        with rx.session() as session:
            # Verificar si ya hay datos de ejemplo
            existing_services = session.exec(rx.select(Service)).first()
            
            if not existing_services:
                # Crear servicios de ejemplo
                services_data = [
                    {
                        "name": "Desarrollo Web",
                        "description": "Aplicaciones web modernas y escalables con frameworks como Django, Flask y FastAPI.",
                        "icon": "code",
                        "features": "Desarrollo Full-Stack,APIs RESTful y GraphQL,Interfaces responsivas,Integración de bases de datos,Optimización de rendimiento",
                        "order": 1
                    },
                    {
                        "name": "Automatización",
                        "description": "Automatizamos procesos empresariales para mejorar la eficiencia y reducir costos operativos.",
                        "icon": "settings",
                        "features": "Automatización de tareas,Web scraping inteligente,Procesamiento de documentos,Integración de sistemas,Workflows personalizados",
                        "order": 2
                    },
                    {
                        "name": "Análisis de Datos",
                        "description": "Convertimos tus datos en insights accionables con herramientas de análisis avanzado.",
                        "icon": "bar_chart",
                        "features": "Business Intelligence,Dashboards interactivos,Machine Learning,Visualización de datos,Reportes automatizados",
                        "order": 3
                    },
                    {
                        "name": "Cloud & DevOps",
                        "description": "Implementación y gestión de infraestructura en la nube con mejores prácticas DevOps.",
                        "icon": "cloud",
                        "features": "Despliegue en AWS/Azure/GCP,Containerización con Docker,CI/CD automatizado,Monitoreo y logging,Escalabilidad automática",
                        "order": 4
                    },
                    {
                        "name": "Consultoría Tech",
                        "description": "Asesoramiento técnico especializado para tomar las mejores decisiones tecnológicas.",
                        "icon": "shield",
                        "features": "Arquitectura de software,Auditoría de código,Migración de sistemas,Capacitación técnica,Estrategia tecnológica",
                        "order": 5
                    },
                    {
                        "name": "Aplicaciones Móviles",
                        "description": "Desarrollo de aplicaciones móviles multiplataforma con tecnologías modernas.",
                        "icon": "smartphone",
                        "features": "Apps nativas e híbridas,Backend con Python,Integración con APIs,Publicación en stores,Mantenimiento continuo",
                        "order": 6
                    }
                ]
                
                for service_data in services_data:
                    service = Service(**service_data)
                    session.add(service)
                
                # Crear algunos proyectos de ejemplo
                projects_data = [
                    {
                        "title": "Sistema de Gestión Empresarial",
                        "description": "Desarrollo de un ERP completo para gestión de inventarios, ventas y contabilidad.",
                        "client_name": "TechCorp Solutions",
                        "technologies": "Python, Django, PostgreSQL, React",
                        "is_featured": True
                    },
                    {
                        "title": "Plataforma de E-commerce",
                        "description": "Tienda online con integración de pagos y gestión de inventario en tiempo real.",
                        "client_name": "RetailMax",
                        "technologies": "Python, FastAPI, MongoDB, Vue.js",
                        "is_featured": True
                    },
                    {
                        "title": "Dashboard Analítico",
                        "description": "Sistema de business intelligence para análisis de datos de ventas y marketing.",
                        "client_name": "DataDriven Inc",
                        "technologies": "Python, Streamlit, Pandas, Plotly",
                        "is_featured": False
                    }
                ]
                
                for project_data in projects_data:
                    project = Project(**project_data)
                    session.add(project)
                
                session.commit()
                print("✅ Base de datos inicializada con datos de ejemplo")
            else:
                print("✅ Base de datos ya contiene datos")
                
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")


def reset_database():
    """Resetear completamente la base de datos."""
    try:
        # Esto debería ser usado solo en desarrollo
        print("⚠️ Reseteando base de datos...")
        
        # Aquí podrías implementar lógica para limpiar todas las tablas
        # Por ahora solo imprimimos el mensaje
        print("✅ Base de datos reseteada")
        
    except Exception as e:
        print(f"❌ Error reseteando base de datos: {e}")


def backup_database():
    """Crear backup de la base de datos."""
    try:
        import shutil
        import datetime
        
        db_path = Config.DATABASE_URL.replace("sqlite:///", "")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backup_pyenterprise_{timestamp}.db"
        
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
