"""
Componente Team Section para PyLink - Perfiles del equipo
"""

import reflex as rx
from ..styles import COLORS


def team_flip_card(name: str, role: str, skills: list, photo_url: str = None) -> rx.Component:
    """Tarjeta flip 3D para miembros del equipo con foto."""
    return rx.box(
        rx.box(
            # Lado frontal
            rx.box(
                # Círculo para la foto del empleado
                rx.box(
                    rx.image(
                        src=photo_url if photo_url else "/default-avatar.png",
                        alt=f"Foto de {name}",
                        width="100%",
                        height="100%",
                        object_fit="cover",
                        border_radius="50%",
                    ) if photo_url else rx.text(
                        name[0],  # Primera letra del nombre si no hay foto
                        font_size="2.5rem",
                        font_weight="900",
                        color="white",
                    ),
                    class_name="employee-photo",
                ),
                rx.text(
                    name,
                    class_name="title",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    role,
                    font_size="1rem",
                    font_weight="600",
                    opacity="0.8",
                ),
                class_name="flip-card-front",
            ),
            
            # Lado trasero
            rx.box(
                rx.text(
                    "🚀 Especialidades",
                    font_weight="800",
                    font_size="1.3rem",
                    margin_bottom="1.5rem",
                ),
                rx.vstack(
                    *[
                        rx.text(
                            f"▸ {skill}",
                            font_size="0.95rem",
                            font_weight="500",
                            margin_bottom="0.5rem",
                            opacity="0.95",
                        ) for skill in skills[:6]  # Máximo 6 skills
                    ],
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                class_name="flip-card-back",
            ),
            
            class_name="flip-card-inner",
        ),
        class_name="flip-card",
    )


def team_section() -> rx.Component:
    """Sección del equipo de PyLink."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal
                rx.heading(
                    "Nuestro Equipo",
                    size="8",
                    color="white",
                    font_weight="800",
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Los profesionales que hacen realidad tus proyectos",
                    font_size="1.2rem",
                    color=COLORS["primary"],
                    text_align="center",
                    margin_bottom="5rem",
                ),
                
                # Grid del equipo
                rx.hstack(
                    # Ibar - CEO & Backend Developer
                    team_flip_card(
                        name="Ibar",
                        role="CEO & Backend Developer",
                        skills=[
                            "Python", "Django", "FastAPI", "PostgreSQL", 
                            "Redis", "Docker", "AWS", "Liderazgo"
                        ],
                        photo_url=None,  # Se puede añadir foto después
                    ),
                    
                    # Daniela - Administrativa de Ventas y Programadora
                    team_flip_card(
                        name="Daniela",
                        role="Admin. Ventas & Developer",
                        skills=[
                            "Gestión Comercial", "Python", "JavaScript", 
                            "CRM", "Marketing Digital", "Base de Datos"
                        ],
                        photo_url=None,  # Se puede añadir foto después
                    ),
                    
                    # José Manuel - Frontend Developer
                    team_flip_card(
                        name="José Manuel",
                        role="Frontend Developer",
                        skills=[
                            "React", "JavaScript", "TypeScript", "CSS3", 
                            "HTML5", "Reflex", "UI/UX Design"
                        ],
                        photo_url=None,  # Se puede añadir foto después
                    ),
                    
                    spacing="4",
                    justify_content="center",
                    wrap="wrap",
                    width="100%",
                ),
                
                # Valores del equipo
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Nuestros Valores",
                            size="6",
                            color="white",
                            font_weight="700",
                            margin_bottom="3rem",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("🤝", font_size="2.5rem", margin_bottom="1rem"),
                                rx.text("Colaboración", color="white", font_weight="600", font_size="1.1rem"),
                                rx.text("Trabajamos juntos", color="rgba(255, 255, 255, 0.7)", text_align="center"),
                                align_items="center",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("🎯", font_size="2.5rem", margin_bottom="1rem"),
                                rx.text("Excelencia", color="white", font_weight="600", font_size="1.1rem"),
                                rx.text("Calidad en todo", color="rgba(255, 255, 255, 0.7)", text_align="center"),
                                align_items="center",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("🚀", font_size="2.5rem", margin_bottom="1rem"),
                                rx.text("Innovación", color="white", font_weight="600", font_size="1.1rem"),
                                rx.text("Siempre adelante", color="rgba(255, 255, 255, 0.7)", text_align="center"),
                                align_items="center",
                                spacing="2",
                            ),
                            spacing="6",
                            justify_content="center",
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    background="rgba(255, 255, 255, 0.05)",
                    backdrop_filter="blur(10px)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="25px",
                    padding="3rem",
                    margin_top="5rem",
                ),
                
                align_items="center",
                spacing="6",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="6rem 2rem",
        ),
        
        id="team",
        background=f"""
            radial-gradient(circle at 30% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
        """,
    )
