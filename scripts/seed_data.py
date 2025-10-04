"""
Script para poblar la base de datos con datos de prueba
"""

import reflex as rx
from datetime import datetime, timedelta
from pyenterprise.models.contact import Contact, Service, Project, BlogPost
from pyenterprise.utils.database import init_database


def create_sample_contacts():
    """Crear contactos de muestra."""
    sample_contacts = [
        {
            "name": "María García",
            "email": "maria.garcia@empresa.com",
            "company": "Innovación Tech SL",
            "message": "Estamos interesados en desarrollar una aplicación web para gestión de inventarios. ¿Podrían enviarnos una cotización?",
            "status": "pending",
            "created_at": datetime.now() - timedelta(days=2)
        },
        {
            "name": "Carlos Rodriguez",
            "email": "carlos.r@startup.es",
            "company": "StartupLab",
            "message": "Necesitamos automatizar nuestros procesos de facturación y contabilidad. ¿Qué soluciones pueden ofrecer?",
            "status": "reviewed",
            "created_at": datetime.now() - timedelta(days=5)
        },
        {
            "name": "Ana López",
            "email": "ana.lopez@comercial.com",
            "company": "Comercial Madrid",
            "message": "Queremos implementar un sistema de análisis de datos para nuestras ventas. ¿Pueden ayudarnos?",
            "status": "responded",
            "created_at": datetime.now() - timedelta(days=10)
        },
        {
            "name": "David Martín",
            "email": "d.martin@consulting.es",
            "company": "Martín Consulting",
            "message": "Estamos buscando migrar nuestra infraestructura a la nube. ¿Ofrecen servicios de consultoría en este área?",
            "status": "pending",
            "created_at": datetime.now() - timedelta(days=1)
        },
        {
            "name": "Laura Sánchez",
            "email": "laura.sanchez@retail.com",
            "company": "RetailPlus",
            "message": "Necesitamos desarrollar una aplicación móvil para nuestros clientes. ¿Cuál sería el proceso y los tiempos?",
            "status": "reviewed",
            "created_at": datetime.now() - timedelta(days=7)
        }
    ]
    
    try:
        with rx.session() as session:
            for contact_data in sample_contacts:
                contact = Contact(**contact_data)
                session.add(contact)
            
            session.commit()
            print(f"✅ {len(sample_contacts)} contactos de muestra creados")
            
    except Exception as e:
        print(f"❌ Error creando contactos de muestra: {e}")


def create_sample_blog_posts():
    """Crear posts de blog de muestra."""
    blog_posts = [
        {
            "title": "Las Mejores Prácticas en Desarrollo Web con Python",
            "slug": "mejores-practicas-desarrollo-web-python",
            "content": "En este artículo exploramos las mejores prácticas para desarrollar aplicaciones web robustas y escalables utilizando Python y frameworks modernos como Django, Flask y FastAPI...",
            "excerpt": "Descubre las mejores prácticas para desarrollar aplicaciones web profesionales con Python.",
            "author": "Equipo PyEnterprise",
            "tags": "python,desarrollo web,django,flask,fastapi",
            "is_published": True,
            "created_at": datetime.now() - timedelta(days=15)
        },
        {
            "title": "Automatización de Procesos Empresariales: Guía Completa",
            "slug": "automatizacion-procesos-empresariales-guia",
            "content": "La automatización de procesos empresariales puede revolucionar la eficiencia de tu empresa. En esta guía completa, te mostramos cómo identificar procesos candidatos para automatización...",
            "excerpt": "Una guía completa sobre cómo automatizar procesos empresariales para mejorar la eficiencia.",
            "author": "Equipo PyEnterprise",
            "tags": "automatización,procesos,eficiencia,rpa",
            "is_published": True,
            "created_at": datetime.now() - timedelta(days=30)
        },
        {
            "title": "Machine Learning para Análisis de Datos Empresariales",
            "slug": "machine-learning-analisis-datos-empresariales",
            "content": "El machine learning está transformando la manera en que las empresas analizan sus datos. Descubre cómo implementar soluciones de ML en tu organización...",
            "excerpt": "Aprende cómo implementar machine learning para obtener insights valiosos de tus datos empresariales.",
            "author": "Equipo PyEnterprise",
            "tags": "machine learning,datos,análisis,inteligencia artificial",
            "is_published": False,
            "created_at": datetime.now() - timedelta(days=5)
        }
    ]
    
    try:
        with rx.session() as session:
            for post_data in blog_posts:
                blog_post = BlogPost(**post_data)
                session.add(blog_post)
            
            session.commit()
            print(f"✅ {len(blog_posts)} posts de blog de muestra creados")
            
    except Exception as e:
        print(f"❌ Error creando posts de blog: {e}")


def main():
    """Función principal para poblar la base de datos."""
    print("🌱 Poblando base de datos con datos de muestra...")
    
    # Inicializar base de datos primero
    init_database()
    
    # Crear datos de muestra
    create_sample_contacts()
    create_sample_blog_posts()
    
    print("\n🎉 ¡Base de datos poblada exitosamente!")
    print("\n📋 Datos creados:")
    print("- Contactos de muestra")
    print("- Posts de blog de muestra")
    print("- Servicios predefinidos")
    print("- Proyectos de ejemplo")
    print("\n🔗 Visita http://localhost:3000/admin para ver el panel de administración")


if __name__ == "__main__":
    main()
