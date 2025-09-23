"""
Modelos de datos para PyEnterprise
"""

import reflex as rx
from datetime import datetime
from typing import Optional


class Contact(rx.Model, table=True):
    """Modelo para almacenar contactos de clientes."""
    
    id: Optional[int] = None
    name: str
    email: str
    company: Optional[str] = ""
    message: str
    created_at: datetime = datetime.now()
    status: str = "pending"  # pending, reviewed, responded
    
    def __str__(self):
        return f"Contact from {self.name} ({self.email})"


class Service(rx.Model, table=True):
    """Modelo para servicios ofrecidos."""
    
    id: Optional[int] = None
    name: str
    description: str
    icon: str
    features: str  # JSON string
    is_active: bool = True
    order: int = 0
    
    def __str__(self):
        return self.name


class Project(rx.Model, table=True):
    """Modelo para proyectos/casos de éxito."""
    
    id: Optional[int] = None
    title: str
    description: str
    client_name: str
    technologies: str  # Separado por comas
    image_url: Optional[str] = ""
    project_url: Optional[str] = ""
    is_featured: bool = False
    created_at: datetime = datetime.now()
    
    def __str__(self):
        return self.title


class BlogPost(rx.Model, table=True):
    """Modelo para posts del blog."""
    
    id: Optional[int] = None
    title: str
    slug: str
    content: str
    excerpt: str
    author: str
    tags: str  # Separado por comas
    image_url: Optional[str] = ""
    is_published: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def __str__(self):
        return self.title
