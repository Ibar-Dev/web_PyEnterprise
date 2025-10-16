"""
Componente About Section moderno para PyLink
"""

import reflex as rx
from ..styles import COLORS


def feature_card(title: str, description: str) -> rx.Component:
    """Tarjeta de característica con efecto de expansión circular exacto."""
    return rx.box(
        # Título
        rx.text(
            title,
            class_name="card-title",
        ),
        # Descripción
        rx.text(
            description,
            class_name="small-desc",
        ),
        # Esquina decorativa
        rx.box(
            rx.box(
                "→",
                class_name="go-arrow",
            ),
            class_name="go-corner",
        ),
        
        # Aplicar la clase CSS principal
        class_name="card",
    )


def about_section() -> rx.Component:
    """Sección sobre PyLink - Presentación moderna de la empresa."""
    return rx.box(
        rx.container(
            rx.vstack(
                # Título principal
                rx.heading(
                    "Sobre PyLink",
                    size="8",
                    color="white",
                    font_weight="800",
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Una empresa joven con grandes ambiciones",
                    font_size="1.2rem",
                    color=COLORS["primary"],
                    text_align="center",
                    margin_bottom="4rem",
                ),
                
                # Historia de la empresa
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Nuestra Historia",
                            size="6",
                            color="white",
                            font_weight="700",
                            margin_bottom="2rem",
                        ),
                        rx.text(
                            "PyLink nace de la pasión por la tecnología y la innovación. Somos una empresa "
                            "joven especializada en el desarrollo de software, con un enfoque fresco y moderno "
                            "hacia las soluciones digitales. Aunque estamos comenzando nuestro camino, nuestro "
                            "equipo cuenta con la experiencia y la determinación necesarias para crear productos "
                            "excepcionales que marquen la diferencia.",
                            font_size="1.1rem",
                            color="rgba(255, 255, 255, 0.8)",
                            line_height="1.7",
                            text_align="center",
                            max_width="800px",
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    background="rgba(255, 255, 255, 0.05)",
                    backdrop_filter="blur(10px)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="25px",
                    padding="3rem",
                    margin_bottom="5rem",
                ),
                
                # Características principales - Responsive grid
                rx.box(
                    # Versión móvil - 1 columna
                    rx.vstack(
                        feature_card(
                            "Innovación",
                            "Utilizamos las últimas tecnologías y metodologías para crear soluciones modernas y eficientes que marquen la diferencia en tu industria."
                        ),
                        feature_card(
                            "Agilidad",
                            "Nuestro enfoque ágil nos permite adaptarnos rápidamente a los cambios y entregar resultados de calidad en tiempos record."
                        ),
                        feature_card(
                            "Precisión",
                            "Cada proyecto es único y trabajamos con precisión quirúrgica para cumplir exactamente los objetivos específicos de tu negocio."
                        ),
                        feature_card(
                            "Creatividad",
                            "Pensamos fuera de la caja para encontrar soluciones creativas e innovadoras a los problemas más complejos del desarrollo."
                        ),
                        spacing="5",
                        width="100%",
                        display=["flex", "flex", "none", "none"],  # Solo móvil y tablet pequeño
                    ),
                    
                    # Versión desktop - 2 columnas
                    rx.grid(
                        feature_card(
                            "Innovación",
                            "Utilizamos las últimas tecnologías y metodologías para crear soluciones modernas y eficientes que marquen la diferencia en tu industria."
                        ),
                        feature_card(
                            "Agilidad",
                            "Nuestro enfoque ágil nos permite adaptarnos rápidamente a los cambios y entregar resultados de calidad en tiempos record."
                        ),
                        feature_card(
                            "Precisión",
                            "Cada proyecto es único y trabajamos con precisión quirúrgica para cumplir exactamente los objetivos específicos de tu negocio."
                        ),
                        feature_card(
                            "Creatividad",
                            "Pensamos fuera de la caja para encontrar soluciones creativas e innovadoras a los problemas más complejos del desarrollo."
                        ),
                        columns="2",
                        spacing="6",
                        width="100%",
                        display=["none", "none", "grid", "grid"],  # Solo desktop
                    ),
                    
                    width="100%",
                    margin_bottom="5rem",
                ),
                
                # Llamada a la acción
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "¿Listo para trabajar con nosotros?",
                            size="6",
                            color="white",
                            font_weight="700",
                            text_align="center",
                            margin_bottom="1rem",
                        ),
                        rx.text(
                            "Conectemos y hagamos realidad tu próximo proyecto digital",
                            font_size="1.1rem",
                            color="rgba(255, 255, 255, 0.8)",
                            text_align="center",
                            margin_bottom="2rem",
                        ),
                        rx.button(
                            "Hablemos",
                            background=f"linear-gradient(45deg, {COLORS['primary']}, #00d4ff)",
                            color="white",
                            font_weight="700",
                            padding="16px 32px",
                            border_radius="50px",
                            font_size="1.1rem",
                            border="none",
                            box_shadow="0 10px 30px rgba(59, 130, 246, 0.5)",
                            transition="all 0.3s ease",
                            _hover={
                                "transform": "translateY(-3px) scale(1.05)",
                                "box_shadow": "0 20px 40px rgba(59, 130, 246, 0.7)",
                            },
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    background=f"linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(0, 212, 255, 0.1))",
                    border="1px solid rgba(59, 130, 246, 0.3)",
                    border_radius="25px",
                    padding="3rem",
                    text_align="center",
                ),
                
                align_items="center",
                spacing="6",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="6rem 2rem",
        ),
        
        id="about",
        background=f"""
            radial-gradient(circle at 70% 30%, rgba(120, 119, 198, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 30% 70%, rgba(255, 119, 198, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)
        """,
    )
