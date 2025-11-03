"""
Estilos compartidos para PyEnterprise
"""

import reflex as rx

# Colores principales
COLORS = {
    "primary": "#2563eb",      # Azul empresarial
    "secondary": "#1e40af",    # Azul más oscuro
    "accent": "#3b82f6",       # Azul claro
    "background": "#ffffff",   # Blanco
    "surface": "#f8fafc",      # Gris muy claro
    "text": "#1f2937",         # Gris oscuro
    "text_light": "#6b7280",  # Gris medio
    "border": "#e5e7eb",       # Gris claro
    "success": "#10b981",      # Verde
    "warning": "#f59e0b",      # Naranja
    "error": "#ef4444",        # Rojo
    "info": "#06b6d4",         # Cyan/Info
}

# Estilos base
base_style = {
    "font_family": "Inter, sans-serif",
    "background_color": COLORS["background"],
    "color": COLORS["text"],
    "line_height": "1.6",
}

# Estilos para botones
button_primary_style = {
    "background_color": COLORS["primary"],
    "color": "white",
    "border": "none",
    "border_radius": "8px",
    "padding": "12px 24px",
    "font_weight": "600",
    "cursor": "pointer",
    "transition": "all 0.3s ease",
    "_hover": {
        "background_color": COLORS["secondary"],
        "transform": "translateY(-2px)",
        "box_shadow": "0 4px 12px rgba(37, 99, 235, 0.3)",
    },
}

button_secondary_style = {
    "background_color": "transparent",
    "color": COLORS["primary"],
    "border": f"2px solid {COLORS['primary']}",
    "border_radius": "8px",
    "padding": "12px 24px",
    "font_weight": "600",
    "cursor": "pointer",
    "transition": "all 0.3s ease",
    "_hover": {
        "background_color": COLORS["primary"],
        "color": "white",
        "transform": "translateY(-2px)",
    },
}

# Estilos para secciones
section_style = {
    "padding": "80px 0",
    "width": "100%",
}

container_style = {
    "max_width": "1200px",
    "margin": "0 auto",
    "padding": "0 20px",
    "width": "100%",
}

# Estilos para el navbar
navbar_style = {
    "background_color": "rgba(255, 255, 255, 0.95)",
    "backdrop_filter": "blur(10px)",
    "border_bottom": f"1px solid {COLORS['border']}",
    "position": "fixed",
    "top": "0",
    "left": "0",
    "right": "0",
    "z_index": "1000",
    "padding": "16px 0",
}

# Estilos para tarjetas
card_style = {
    "background_color": COLORS["background"],
    "border_radius": "12px",
    "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.05)",
    "border": f"1px solid {COLORS['border']}",
    "padding": "24px",
    "transition": "all 0.3s ease",
    "_hover": {
        "box_shadow": "0 8px 25px rgba(0, 0, 0, 0.1)",
        "transform": "translateY(-4px)",
    },
}

# Estilos para títulos
title_style = {
    "font_size": "3rem",
    "font_weight": "700",
    "color": COLORS["text"],
    "margin_bottom": "1rem",
    "line_height": "1.2",
}

subtitle_style = {
    "font_size": "2rem",
    "font_weight": "600",
    "color": COLORS["text"],
    "margin_bottom": "1rem",
    "text_align": "center",
}

# Estilos para el hero
hero_style = {
    "background": f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%)",
    "color": "white",
    "padding": "120px 0 80px 0",
    "text_align": "center",
}

# Estilos para formularios
input_style = {
    "width": "100%",
    "padding": "12px 16px",
    "border": f"2px solid {COLORS['border']}",
    "border_radius": "8px",
    "font_size": "16px",
    "transition": "border-color 0.3s ease",
    "_focus": {
        "outline": "none",
        "border_color": COLORS["primary"],
        "box_shadow": f"0 0 0 3px rgba(37, 99, 235, 0.1)",
    },
}

# Estilos responsivos
mobile_breakpoint = "768px"
tablet_breakpoint = "1024px"