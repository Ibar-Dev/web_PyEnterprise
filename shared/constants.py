"""
Constantes compartidas para PyEnterprise
"""

# URLs de la aplicación
APP_URL = "http://localhost:3000"
API_BASE_URL = "http://localhost:8000"

# Rutas de la aplicación
ROUTES = {
    "home": "/",
    "empleados": "/empleados",
    "empleado_dashboard": "/empleados/dashboard",
    "admin": "/admin",
    "services": "/servicios",
    "about": "/nosotros",
    "contact": "/contacto",
    "privacy": "/privacidad",
    "cookies": "/cookies",
    "terms": "/terminos"
}

# Mensajes de la aplicación
MESSAGES = {
    "login_success": "Inicio de sesión exitoso",
    "login_error": "Error en el inicio de sesión",
    "session_expired": "Tu sesión ha expirado",
    "access_denied": "Acceso denegado",
    "operation_success": "Operación realizada con éxito",
    "operation_error": "Error en la operación"
}

# Roles de usuario
ROLES = {
    "ADMIN": "admin",
    "DESARROLLADOR": "desarrollador",
    "DISENADOR": "disenadora",
    "PROJECT_MANAGER": "project_manager"
}

# Estados de proyectos
PROJECT_STATUSES = {
    "ACTIVO": "activo",
    "COMPLETADO": "completado",
    "PAUSADO": "pausado",
    "CANCELADO": "cancelado"
}

# Estados de tareas
TASK_STATUSES = {
    "PENDIENTE": "pendiente",
    "EN_PROGRESO": "en_progreso",
    "COMPLETADA": "completada",
    "CANCELADA": "cancelada"
}

# Prioridades de tareas
TASK_PRIORITIES = {
    "BAJA": "baja",
    "MEDIA": "media",
    "ALTA": "alta",
    "URGENTE": "urgente"
}