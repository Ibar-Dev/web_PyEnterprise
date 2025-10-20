"""
Página de Servicios - Modelos de negocio y soluciones
"""

import reflex as rx
from ..styles import COLORS


class ServicesState(rx.State):
    """Estado para la página de servicios."""
    selected_service: str = ""
    
    def set_selected_service(self, service: str):
        """Selecciona un servicio."""
        self.selected_service = service


def service_card(
    title: str,
    description: str,
    image_url: str,
    features: list,
    color_gradient: str,
    service_id: str,
) -> rx.Component:
    """Tarjeta de servicio con información y botón de contacto."""
    return rx.box(
        rx.vstack(
            # Imagen representativa
            rx.box(
                rx.image(
                    src=image_url,
                    alt=title,
                    width="100%",
                    height="200px",
                    object_fit="cover",
                ),
                width="100%",
                height="200px",
                background=color_gradient,
                border_radius="12px 12px 0 0",
                overflow="hidden",
                position="relative",
                _before={
                    "content": '""',
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "right": "0",
                    "bottom": "0",
                    "background": color_gradient,
                    "opacity": "0.3",
                    "z_index": "1",
                },
            ),
            
            # Contenido
            rx.vstack(
                # Título
                rx.heading(
                    title,
                    size="6",
                    color="white",
                    font_weight="700",
                    margin_bottom="0.5rem",
                ),
                
                # Descripción
                rx.text(
                    description,
                    color="rgba(255, 255, 255, 0.8)",
                    font_size="0.95rem",
                    line_height="1.6",
                    margin_bottom="1rem",
                ),
                
                # Características
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.text(
                                "✓",
                                color=COLORS["primary"],
                                font_weight="700",
                                font_size="1.2rem",
                            ),
                            rx.text(
                                feature,
                                color="rgba(255, 255, 255, 0.85)",
                                font_size="0.9rem",
                            ),
                            spacing="2",
                            align_items="start",
                        )
                        for feature in features
                    ],
                    spacing="1",
                    margin_bottom="1.5rem",
                ),
                
                # Botón de contacto
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="mail", margin_right="8px"),
                            rx.text("Solicitar Presupuesto"),
                            align_items="center",
                        ),
                        background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                        color="white",
                        font_weight="600",
                        padding="12px 24px",
                        border_radius="8px",
                        width="100%",
                        cursor="pointer",
                        _hover={
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 10px 25px rgba(59, 130, 246, 0.4)",
                        },
                        transition="all 0.3s ease",
                    ),
                    href=f"/contacto?servicio={service_id}",
                ),
                
                padding="1.5rem",
                spacing="0",
                width="100%",
            ),
            
            spacing="0",
            width="100%",
            background="rgba(30, 41, 59, 0.8)",
            border_radius="12px",
            overflow="hidden",
            border=f"1px solid {COLORS['primary']}",
            transition="all 0.3s ease",
            _hover={
                "transform": "translateY(-8px)",
                "box_shadow": f"0 20px 40px rgba(59, 130, 246, 0.3)",
            },
        ),
        width="100%",
    )


def services_page() -> rx.Component:
    """Página de servicios con todos los modelos de negocio."""
    return rx.box(
        # Navbar spacing
        rx.box(height="80px"),
        
        rx.container(
            rx.vstack(
                # Header moderno
                rx.vstack(
                    # Badge/Tag
                    rx.box(
                        rx.text(
                            "✨ Servicios Premium",
                            color=COLORS["primary"],
                            font_weight="600",
                            font_size="0.9rem",
                            letter_spacing="1px",
                        ),
                        padding="8px 20px",
                        background="rgba(59, 130, 246, 0.1)",
                        border=f"1px solid {COLORS['primary']}",
                        border_radius="50px",
                        margin_bottom="1.5rem",
                    ),
                    # Título principal con gradiente
                    rx.heading(
                        "Nuestros Servicios",
                        size="9",
                        color="white",
                        font_weight="900",
                        text_align="center",
                        background=f"linear-gradient(135deg, white, {COLORS['primary']}, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        margin_bottom="1rem",
                        letter_spacing="-1px",
                    ),
                    # Subtítulo con efecto
                    rx.text(
                        "Soluciones digitales innovadoras diseñadas para impulsar tu negocio",
                        font_size="1.25rem",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                        margin_bottom="1rem",
                        max_width="700px",
                        line_height="1.6",
                    ),
                    # Línea decorativa
                    rx.box(
                        width="80px",
                        height="4px",
                        background=f"linear-gradient(90deg, transparent, {COLORS['primary']}, transparent)",
                        border_radius="2px",
                        margin_bottom="3rem",
                    ),
                    align_items="center",
                    width="100%",
                ),
                
                # Servicios principales (Web & Apps)
                rx.vstack(
                    rx.heading(
                        "🌐 Desarrollo Web",
                        size="7",
                        color="white",
                        font_weight="700",
                        margin_bottom="2rem",
                    ),
                    rx.grid(
                        service_card(
                            title="Sitios Web Corporativos",
                            description="Presencia profesional en internet para tu empresa",
                            image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
                            features=[
                                "Diseño responsivo y moderno",
                                "Optimizado para SEO",
                                "Rápido y seguro",
                                "Panel de administración",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(94, 234, 212, 0.3))",
                            service_id="web-corporativo",
                        ),
                        service_card(
                            title="E-commerce",
                            description="Tienda online completa para vender tus productos",
                            image_url="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80",
                            features=[
                                "Carrito de compras inteligente",
                                "Pasarela de pagos integrada",
                                "Gestión de inventario",
                                "Análisis de ventas",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(59, 130, 246, 0.3))",
                            service_id="ecommerce",
                        ),
                        service_card(
                            title="Portales Web",
                            description="Plataformas complejas con múltiples funcionalidades",
                            image_url="https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80",
                            features=[
                                "Autenticación de usuarios",
                                "Gestión de contenidos",
                                "APIs integradas",
                                "Escalabilidad garantizada",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(59, 130, 246, 0.3))",
                            service_id="portal-web",
                        ),
                        service_card(
                            title="Landing Pages",
                            description="Páginas de conversión optimizadas para resultados",
                            image_url="https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&q=80",
                            features=[
                                "Diseño orientado a conversión",
                                "A/B Testing integrado",
                                "Formularios avanzados",
                                "Integración con CRM",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(59, 130, 246, 0.3))",
                            service_id="landing-page",
                        ),
                        min_child_width="300px",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="4rem",
                ),
                
                # Aplicaciones Móviles
                rx.vstack(
                    rx.heading(
                        "📱 Aplicaciones Móviles",
                        size="7",
                        color="white",
                        font_weight="700",
                        margin_bottom="2rem",
                    ),
                    rx.grid(
                        service_card(
                            title="Apps iOS & Android",
                            description="Aplicaciones nativas de alto rendimiento",
                            image_url="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&q=80",
                            features=[
                                "Desarrollo nativo optimizado",
                                "Interfaz intuitiva",
                                "Acceso a cámara y sensores",
                                "Publicación en tiendas",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(34, 197, 94, 0.3))",
                            service_id="app-nativa",
                        ),
                        service_card(
                            title="Apps Multiplataforma",
                            description="Una sola app para iOS, Android y Web",
                            image_url="https://images.unsplash.com/photo-1551650975-87deedd944c3?w=800&q=80",
                            features=[
                                "Código compartido",
                                "Menor tiempo de desarrollo",
                                "Mantenimiento centralizado",
                                "Actualizaciones simultáneas",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(34, 197, 94, 0.3))",
                            service_id="app-multiplataforma",
                        ),
                        service_card(
                            title="Apps Web Progresivas",
                            description="Apps web con experiencia nativa",
                            image_url="https://images.unsplash.com/photo-1551650975-87deedd944c3?w=800&q=80",
                            features=[
                                "Funciona sin conexión",
                                "Instalable en home",
                                "Notificaciones push",
                                "Sincronización automática",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(168, 85, 247, 0.3))",
                            service_id="pwa",
                        ),
                        service_card(
                            title="Apps de Gestión",
                            description="Soluciones internas para tu empresa",
                            image_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
                            features=[
                                "Gestión de proyectos",
                                "Control de inventario",
                                "Reportes en tiempo real",
                                "Sincronización de datos",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(236, 72, 153, 0.3))",
                            service_id="app-gestion",
                        ),
                        min_child_width="300px",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="4rem",
                ),
                
                # Software Personalizado
                rx.vstack(
                    rx.heading(
                        "💻 Software Personalizado",
                        size="7",
                        color="white",
                        font_weight="700",
                        margin_bottom="2rem",
                    ),
                    rx.grid(
                        service_card(
                            title="Sistemas de Escritorio",
                            description="Software robusto para tu negocio",
                            image_url="https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=80",
                            features=[
                                "Interfaz moderna",
                                "Base de datos integrada",
                                "Reportes personalizados",
                                "Soporte técnico incluido",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(168, 85, 247, 0.3))",
                            service_id="software-escritorio",
                        ),
                        service_card(
                            title="Automatización de Procesos",
                            description="Automatiza tareas repetitivas y ahorra tiempo",
                            image_url="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&q=80",
                            features=[
                                "RPA (Robotic Process Automation)",
                                "Integración con sistemas",
                                "Reducción de errores",
                                "Aumento de productividad",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(59, 130, 246, 0.3))",
                            service_id="automatizacion",
                        ),
                        service_card(
                            title="Inteligencia Artificial",
                            description="Soluciones con IA para optimizar tu negocio",
                            image_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
                            features=[
                                "Machine Learning",
                                "Análisis predictivo",
                                "Chatbots inteligentes",
                                "Visión por computadora",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(168, 85, 247, 0.3))",
                            service_id="ia",
                        ),
                        service_card(
                            title="APIs y Integraciones",
                            description="Conecta tus sistemas y herramientas",
                            image_url="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80",
                            features=[
                                "APIs REST personalizadas",
                                "Webhooks y eventos",
                                "Sincronización de datos",
                                "Documentación completa",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(236, 72, 153, 0.3))",
                            service_id="apis",
                        ),
                        min_child_width="300px",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="4rem",
                ),
                
                # Servicios Adicionales
                rx.vstack(
                    rx.heading(
                        "🎨 Servicios Adicionales",
                        size="7",
                        color="white",
                        font_weight="700",
                        margin_bottom="2rem",
                    ),
                    rx.grid(
                        service_card(
                            title="Diseño UI/UX",
                            description="Interfaces hermosas y funcionales",
                            image_url="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&q=80",
                            features=[
                                "Diseño responsivo",
                                "Prototipado interactivo",
                                "User research",
                                "Guías de estilo",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(34, 197, 94, 0.3))",
                            service_id="ui-ux",
                        ),
                        service_card(
                            title="Consultoría Tecnológica",
                            description="Asesoramiento experto para tu transformación digital",
                            image_url="https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",
                            features=[
                                "Análisis de necesidades",
                                "Recomendaciones tecnológicas",
                                "Roadmap de implementación",
                                "Capacitación del equipo",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(236, 72, 153, 0.3))",
                            service_id="consultoria",
                        ),
                        service_card(
                            title="Mantenimiento y Soporte",
                            description="Mantén tu software funcionando perfectamente",
                            image_url="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80",
                            features=[
                                "Monitoreo 24/7",
                                "Actualizaciones de seguridad",
                                "Soporte técnico prioritario",
                                "Backups automáticos",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(59, 130, 246, 0.3))",
                            service_id="mantenimiento",
                        ),
                        service_card(
                            title="Cloud & DevOps",
                            description="Infraestructura escalable y confiable",
                            image_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",
                            features=[
                                "Despliegue en la nube",
                                "CI/CD pipelines",
                                "Monitoreo de performance",
                                "Escalado automático",
                            ],
                            color_gradient="linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(168, 85, 247, 0.3))",
                            service_id="cloud-devops",
                        ),
                        min_child_width="300px",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    margin_bottom="4rem",
                ),
                
                # CTA Final
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "¿No encuentras lo que buscas?",
                            size="6",
                            color="white",
                            font_weight="700",
                            text_align="center",
                        ),
                        rx.text(
                            "Contáctanos para soluciones personalizadas adaptadas a tus necesidades específicas",
                            color="rgba(255, 255, 255, 0.8)",
                            text_align="center",
                            font_size="1.05rem",
                            margin_bottom="2rem",
                        ),
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="phone", margin_right="8px"),
                                    rx.text("Hablar con un Especialista"),
                                    align_items="center",
                                ),
                                background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                                color="white",
                                font_weight="700",
                                padding="16px 32px",
                                border_radius="50px",
                                font_size="1.1rem",
                                cursor="pointer",
                                _hover={
                                    "transform": "translateY(-3px) scale(1.05)",
                                    "box_shadow": "0 15px 35px rgba(59, 130, 246, 0.4)",
                                },
                                transition="all 0.3s ease",
                            ),
                            href="/contacto?servicio=consulta-general",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    padding="3rem",
                    background="linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(168, 85, 247, 0.1))",
                    border_radius="12px",
                    border=f"2px solid {COLORS['primary']}",
                    width="100%",
                    margin_bottom="2rem",
                ),
                
                spacing="6",
                padding=["3rem 1rem", "3rem 1.5rem", "6rem 2rem", "6rem 2rem"],
            ),
            max_width="1200px",
            margin="0 auto",
        ),
        
        min_height="100vh",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )
