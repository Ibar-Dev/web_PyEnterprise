"""
Cliente de Supabase para PyLink
Maneja la conexión y operaciones con la base de datos
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional, Dict, List, Any
import bcrypt

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cliente global de Supabase
supabase: Optional[Client] = None


def get_supabase_client() -> Client:
    """Obtener o crear el cliente de Supabase."""
    global supabase
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL y SUPABASE_KEY deben estar definidas en .env"
            )
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase


def hash_password(password: str) -> str:
    """Hashear una contraseña con bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verificar si una contraseña coincide con su hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )


# ====================================================
# FUNCIONES DE AUTENTICACIÓN
# ====================================================

def login_empleado(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Autenticar un empleado con email y contraseña.
    Retorna los datos del empleado si es exitoso, None si falla.
    """
    try:
        client = get_supabase_client()
        
        # Buscar empleado por email
        response = client.table('empleados').select('*').eq('email', email).eq('activo', True).execute()
        
        if not response.data or len(response.data) == 0:
            return None
        
        empleado = response.data[0]
        
        # Verificar contraseña
        if verify_password(password, empleado['password_hash']):
            # No devolver el hash de contraseña
            empleado.pop('password_hash', None)
            return empleado
        
        return None
    except Exception as e:
        print(f"Error en login_empleado: {e}")
        return None


def crear_empleado(email: str, password: str, nombre: str, apellidos: str, rol: str) -> Optional[Dict[str, Any]]:
    """
    Crear un nuevo empleado.
    Solo debe ser usado por administradores.
    """
    try:
        client = get_supabase_client()
        
        # Hashear la contraseña
        password_hash = hash_password(password)
        
        # Crear empleado
        response = client.table('empleados').insert({
            'email': email,
            'password_hash': password_hash,
            'nombre': nombre,
            'apellidos': apellidos,
            'rol': rol,
            'activo': True
        }).execute()
        
        if response.data:
            empleado = response.data[0]
            empleado.pop('password_hash', None)
            return empleado
        
        return None
    except Exception as e:
        print(f"Error en crear_empleado: {e}")
        return None


# ====================================================
# FUNCIONES DE PROYECTOS
# ====================================================

def obtener_proyectos_empleado(empleado_id: str) -> List[Dict[str, Any]]:
    """Obtener todos los proyectos asignados a un empleado."""
    try:
        client = get_supabase_client()
        
        # Consulta con JOIN
        response = client.table('proyecto_empleado').select(
            'proyectos(*), rol_en_proyecto'
        ).eq('empleado_id', empleado_id).eq('activo', True).execute()
        
        if response.data:
            proyectos = []
            for item in response.data:
                proyecto = item['proyectos']
                proyecto['rol_en_proyecto'] = item['rol_en_proyecto']
                proyectos.append(proyecto)
            return proyectos
        
        return []
    except Exception as e:
        print(f"Error en obtener_proyectos_empleado: {e}")
        return []


def obtener_todos_proyectos() -> List[Dict[str, Any]]:
    """Obtener todos los proyectos (para admin)."""
    try:
        client = get_supabase_client()
        response = client.table('proyectos').select('*').order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_todos_proyectos: {e}")
        return []


def crear_proyecto(nombre: str, descripcion: str, cliente: str, 
                   fecha_inicio: str, presupuesto: float = 0.0) -> Optional[Dict[str, Any]]:
    """Crear un nuevo proyecto con presupuesto en euros."""
    try:
        client = get_supabase_client()
        
        # Validar formato de fecha (YYYY-MM-DD)
        from datetime import datetime
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Error: Formato de fecha inválido. Use YYYY-MM-DD (ej: 2024-12-31)")
            return None
        
        response = client.table('proyectos').insert({
            'nombre': nombre,
            'descripcion': descripcion,
            'cliente': cliente,
            'fecha_inicio': fecha_inicio,
            'presupuesto_horas': int(presupuesto),  # Guardar en el campo existente por compatibilidad
            'estado': 'activo',
            'progreso': 0
        }).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en crear_proyecto: {e}")
        return None


# ====================================================
# FUNCIONES DE JORNADAS
# ====================================================

def registrar_jornada(empleado_id: str, proyecto_id: Optional[str], fecha: str,
                     hora_inicio: str, hora_fin: str, descripcion: str) -> Optional[Dict[str, Any]]:
    """Registrar una jornada laboral. proyecto_id puede ser None si no hay proyecto asignado."""
    try:
        # Validar que empleado_id sea UUID válido
        if not empleado_id or empleado_id == "default" or len(empleado_id) < 30:
            print(f"❌ Error: empleado_id inválido: {empleado_id}")
            return None
        
        # Validar proyecto_id solo si se proporciona (puede ser None)
        if proyecto_id and (proyecto_id == "default" or len(proyecto_id) < 30):
            print(f"❌ Error: proyecto_id inválido: {proyecto_id}")
            return None
        
        # Calcular horas trabajadas
        from datetime import datetime
        inicio = datetime.fromisoformat(hora_inicio)
        fin = datetime.fromisoformat(hora_fin)
        horas_trabajadas = (fin - inicio).total_seconds() / 3600
        
        client = get_supabase_client()
        jornada_data = {
            'empleado_id': empleado_id,
            'fecha': fecha,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'horas_trabajadas': round(horas_trabajadas, 2),
            'descripcion': descripcion,
            'estado': 'completada'
        }
        
        # Solo incluir proyecto_id si existe
        if proyecto_id:
            jornada_data['proyecto_id'] = proyecto_id
        
        response = client.table('jornadas').insert(jornada_data).execute()
        
        print(f"✅ Jornada registrada: {horas_trabajadas:.2f} horas{' (sin proyecto)' if not proyecto_id else ''}")
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en registrar_jornada: {e}")
        return None


def obtener_jornadas_empleado(empleado_id: str, fecha_inicio: Optional[str] = None, 
                               fecha_fin: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtener jornadas de un empleado con filtros opcionales."""
    try:
        client = get_supabase_client()
        
        query = client.table('jornadas').select(
            '*, proyectos(nombre)'
        ).eq('empleado_id', empleado_id)
        
        if fecha_inicio:
            query = query.gte('fecha', fecha_inicio)
        if fecha_fin:
            query = query.lte('fecha', fecha_fin)
        
        response = query.order('fecha', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_jornadas_empleado: {e}")
        return []


def calcular_horas_totales_empleado(empleado_id: str, fecha_inicio: Optional[str] = None,
                                    fecha_fin: Optional[str] = None) -> float:
    """Calcular las horas totales trabajadas por un empleado."""
    try:
        jornadas = obtener_jornadas_empleado(empleado_id, fecha_inicio, fecha_fin)
        total_horas = sum(j.get('horas_trabajadas', 0) for j in jornadas)
        return round(total_horas, 2)
    except Exception as e:
        print(f"Error en calcular_horas_totales_empleado: {e}")
        return 0.0


# ====================================================
# FUNCIONES DE TAREAS
# ====================================================

def obtener_tareas_empleado(empleado_id: str) -> List[Dict[str, Any]]:
    """Obtener todas las tareas asignadas a un empleado."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').select(
            '*, proyectos(nombre)'
        ).eq('empleado_asignado_id', empleado_id).order('fecha_creacion', desc=True).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_tareas_empleado: {e}")
        return []


def crear_tarea(proyecto_id: str, empleado_asignado_id: str, titulo: str,
                descripcion: str, prioridad: str, fecha_vencimiento: str) -> Optional[Dict[str, Any]]:
    """Crear una nueva tarea."""
    try:
        client = get_supabase_client()
        
        # Validar formato de fecha (YYYY-MM-DD)
        from datetime import datetime
        try:
            datetime.strptime(fecha_vencimiento, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Error: Formato de fecha inválido. Use YYYY-MM-DD (ej: 2024-12-31)")
            return None
        
        # Validar UUIDs
        if not proyecto_id or len(proyecto_id) < 30:
            print(f"❌ Error: ID de proyecto inválido")
            return None
        
        if not empleado_asignado_id or len(empleado_asignado_id) < 30:
            print(f"❌ Error: ID de empleado inválido")
            return None
        
        response = client.table('tareas').insert({
            'proyecto_id': proyecto_id,
            'empleado_asignado_id': empleado_asignado_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'prioridad': prioridad,
            'estado': 'pendiente',
            'fecha_vencimiento': fecha_vencimiento,
            'horas_estimadas': 0
        }).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en crear_tarea: {e}")
        return None


def actualizar_estado_tarea(tarea_id: str, nuevo_estado: str) -> bool:
    """Actualizar el estado de una tarea."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').update({
            'estado': nuevo_estado
        }).eq('id', tarea_id).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"Error en actualizar_estado_tarea: {e}")
        return False


# ====================================================
# FUNCIONES DE ADMINISTRACIÓN
# ====================================================

def obtener_todos_empleados() -> List[Dict[str, Any]]:
    """Obtener todos los empleados (para admin)."""
    try:
        client = get_supabase_client()
        response = client.table('empleados').select(
            'id, email, nombre, apellidos, rol, activo, fecha_ingreso'
        ).order('nombre').execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_todos_empleados: {e}")
        return []


def asignar_empleado_proyecto(empleado_id: str, proyecto_id: str, 
                               rol_en_proyecto: str = "colaborador") -> Optional[Dict[str, Any]]:
    """Asignar un empleado a un proyecto."""
    try:
        client = get_supabase_client()
        response = client.table('proyecto_empleado').insert({
            'empleado_id': empleado_id,
            'proyecto_id': proyecto_id,
            'rol_en_proyecto': rol_en_proyecto,
            'activo': True
        }).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en asignar_empleado_proyecto: {e}")
        return None


def eliminar_proyecto(proyecto_id: str) -> bool:
    """Eliminar un proyecto completamente (hard delete)."""
    try:
        client = get_supabase_client()
        
        # Primero eliminar relaciones en proyecto_empleado
        client.table('proyecto_empleado').delete().eq('proyecto_id', proyecto_id).execute()
        
        # Luego eliminar el proyecto
        response = client.table('proyectos').delete().eq('id', proyecto_id).execute()
        
        print(f"✅ Proyecto eliminado completamente")
        return True
    except Exception as e:
        print(f"Error en eliminar_proyecto: {e}")
        return False


def eliminar_empleado(empleado_id: str) -> bool:
    """Eliminar un empleado completamente (hard delete)."""
    try:
        client = get_supabase_client()
        
        # Primero eliminar relaciones en proyecto_empleado
        client.table('proyecto_empleado').delete().eq('empleado_id', empleado_id).execute()
        
        # Luego eliminar el empleado
        response = client.table('empleados').delete().eq('id', empleado_id).execute()
        
        print(f"✅ Empleado eliminado completamente")
        return True
    except Exception as e:
        print(f"Error en eliminar_empleado: {e}")
        return False


def eliminar_tarea(tarea_id: str) -> bool:
    """Eliminar una tarea completamente (hard delete)."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').delete().eq('id', tarea_id).execute()
        
        print(f"✅ Tarea eliminada completamente")
        return True
    except Exception as e:
        print(f"Error en eliminar_tarea: {e}")
        return False


def obtener_tareas_proyecto(proyecto_id: str) -> List[Dict[str, Any]]:
    """Obtener todas las tareas de un proyecto específico."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').select(
            '*, empleados(nombre, email)'
        ).eq('proyecto_id', proyecto_id).order('fecha_creacion', desc=True).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_tareas_proyecto: {e}")
        return []


def obtener_todas_tareas() -> List[Dict[str, Any]]:
    """Obtener todas las tareas del sistema (para admin)."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').select(
            '*, proyectos(nombre), empleados(nombre)'
        ).order('fecha_creacion', desc=True).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_todas_tareas: {e}")
        return []


def obtener_estadisticas_sistema() -> Dict[str, Any]:
    """Obtener estadísticas generales del sistema."""
    try:
        client = get_supabase_client()
        
        # Contar proyectos activos
        proyectos = client.table('proyectos').select('id', count='exact').eq('estado', 'activo').execute()
        total_proyectos = proyectos.count if proyectos.count else 0
        
        # Contar empleados activos
        empleados = client.table('empleados').select('id', count='exact').eq('activo', True).execute()
        total_empleados = empleados.count if empleados.count else 0
        
        # Contar tareas
        tareas = client.table('tareas').select('id', count='exact').execute()
        total_tareas = tareas.count if tareas.count else 0
        
        # Calcular horas totales
        jornadas = client.table('jornadas').select('horas_trabajadas').execute()
        horas_totales = sum(j.get('horas_trabajadas', 0) for j in (jornadas.data or []))
        
        return {
            'total_proyectos': total_proyectos,
            'total_empleados': total_empleados,
            'total_tareas': total_tareas,
            'horas_totales': round(horas_totales, 2)
        }
    except Exception as e:
        print(f"Error en obtener_estadisticas_sistema: {e}")
        return {
            'total_proyectos': 0,
            'total_empleados': 0,
            'total_tareas': 0,
            'horas_totales': 0.0
        }


def obtener_todas_jornadas(fecha_inicio: Optional[str] = None, 
                           fecha_fin: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtener todas las jornadas del sistema (para admin)."""
    try:
        client = get_supabase_client()
        
        query = client.table('jornadas').select(
            '*, empleados(nombre, email), proyectos(nombre)'
        )
        
        if fecha_inicio:
            query = query.gte('fecha', fecha_inicio)
        if fecha_fin:
            query = query.lte('fecha', fecha_fin)
        
        response = query.order('fecha', desc=True).limit(100).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error en obtener_todas_jornadas: {e}")
        return []


def actualizar_proyecto(proyecto_id: str, datos: Dict[str, Any]) -> bool:
    """Actualizar información de un proyecto."""
    try:
        client = get_supabase_client()
        response = client.table('proyectos').update(datos).eq('id', proyecto_id).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"Error en actualizar_proyecto: {e}")
        return False


def actualizar_tarea(tarea_id: str, datos: Dict[str, Any]) -> bool:
    """Actualizar información de una tarea."""
    try:
        client = get_supabase_client()
        response = client.table('tareas').update(datos).eq('id', tarea_id).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"Error en actualizar_tarea: {e}")
        return False


def obtener_proyecto_por_id(proyecto_id: str) -> Optional[Dict[str, Any]]:
    """Obtener un proyecto específico por su ID."""
    try:
        client = get_supabase_client()
        response = client.table('proyectos').select('*').eq('id', proyecto_id).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en obtener_proyecto_por_id: {e}")
        return None


def obtener_empleado_por_id(empleado_id: str) -> Optional[Dict[str, Any]]:
    """Obtener un empleado específico por su ID."""
    try:
        client = get_supabase_client()
        response = client.table('empleados').select(
            'id, email, nombre, apellidos, rol, activo, fecha_ingreso'
        ).eq('id', empleado_id).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en obtener_empleado_por_id: {e}")
        return None


def calcular_horas_mensuales_empleado(empleado_id: str, año: int, mes: int) -> float:
    """
    Calcular horas trabajadas por un empleado en un mes específico.
    
    Args:
        empleado_id: ID del empleado
        año: Año (ej: 2024)
        mes: Mes (1-12)
    
    Returns:
        Total de horas trabajadas en el mes
    """
    try:
        from datetime import datetime
        
        # Calcular primer y último día del mes
        if mes == 12:
            fecha_inicio = f"{año}-{mes:02d}-01"
            fecha_fin = f"{año + 1}-01-01"
        else:
            fecha_inicio = f"{año}-{mes:02d}-01"
            fecha_fin = f"{año}-{mes + 1:02d}-01"
        
        client = get_supabase_client()
        response = client.table('jornadas').select('horas_trabajadas').eq(
            'empleado_id', empleado_id
        ).gte('fecha', fecha_inicio).lt('fecha', fecha_fin).execute()
        
        total_horas = sum(j.get('horas_trabajadas', 0) for j in (response.data or []))
        return round(total_horas, 2)
    except Exception as e:
        print(f"Error en calcular_horas_mensuales_empleado: {e}")
        return 0.0


def obtener_empleados_con_estadisticas(año: Optional[int] = None, mes: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Obtener todos los empleados con sus estadísticas de horas trabajadas.
    
    Args:
        año: Año opcional para filtrar (default: año actual)
        mes: Mes opcional para filtrar (default: mes actual)
    
    Returns:
        Lista de empleados con sus estadísticas
    """
    try:
        from datetime import datetime
        
        if año is None or mes is None:
            now = datetime.now()
            año = now.year if año is None else año
            mes = now.month if mes is None else mes
        
        empleados = obtener_todos_empleados()
        
        empleados_con_stats = []
        for emp in empleados:
            horas_mes = calcular_horas_mensuales_empleado(emp['id'], año, mes)
            
            # Contar proyectos asignados
            proyectos = obtener_proyectos_empleado(emp['id'])
            
            # Contar tareas asignadas
            tareas = obtener_tareas_empleado(emp['id'])
            tareas_pendientes = len([t for t in tareas if t.get('estado') == 'pendiente'])
            tareas_completadas = len([t for t in tareas if t.get('estado') == 'completada'])
            
            empleados_con_stats.append({
                **emp,
                'horas_mes_actual': horas_mes,
                'total_proyectos': len(proyectos),
                'total_tareas': len(tareas),
                'tareas_pendientes': tareas_pendientes,
                'tareas_completadas': tareas_completadas,
            })
        
        return empleados_con_stats
    except Exception as e:
        print(f"Error en obtener_empleados_con_estadisticas: {e}")
        return []


def obtener_estadisticas_proyecto(proyecto_id: str) -> Dict[str, Any]:
    """
    Obtener estadísticas detalladas de un proyecto.
    
    Returns:
        Diccionario con estadísticas del proyecto
    """
    try:
        client = get_supabase_client()
        
        # Obtener proyecto
        proyecto = obtener_proyecto_por_id(proyecto_id)
        if not proyecto:
            return {}
        
        # Contar tareas por estado
        tareas = obtener_tareas_proyecto(proyecto_id)
        tareas_pendientes = len([t for t in tareas if t.get('estado') == 'pendiente'])
        tareas_en_progreso = len([t for t in tareas if t.get('estado') == 'en_progreso'])
        tareas_completadas = len([t for t in tareas if t.get('estado') == 'completada'])
        
        # Calcular horas trabajadas en el proyecto
        jornadas = client.table('jornadas').select('horas_trabajadas').eq(
            'proyecto_id', proyecto_id
        ).execute()
        horas_trabajadas = sum(j.get('horas_trabajadas', 0) for j in (jornadas.data or []))
        
        # Contar empleados asignados
        asignaciones = client.table('proyecto_empleado').select('empleado_id', count='exact').eq(
            'proyecto_id', proyecto_id
        ).eq('activo', True).execute()
        total_empleados = asignaciones.count if asignaciones.count else 0
        
        # Calcular progreso basado en tareas
        total_tareas = len(tareas)
        progreso = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
        
        return {
            'proyecto_id': proyecto_id,
            'nombre': proyecto['nombre'],
            'cliente': proyecto.get('cliente', 'N/A'),
            'estado': proyecto.get('estado', 'activo'),
            'total_tareas': total_tareas,
            'tareas_pendientes': tareas_pendientes,
            'tareas_en_progreso': tareas_en_progreso,
            'tareas_completadas': tareas_completadas,
            'horas_trabajadas': round(horas_trabajadas, 2),
            'presupuesto_horas': proyecto.get('presupuesto_horas', 0),
            'total_empleados': total_empleados,
            'progreso': round(progreso, 1),
        }
    except Exception as e:
        print(f"Error en obtener_estadisticas_proyecto: {e}")
        return {}


def obtener_resumen_dashboard_admin() -> Dict[str, Any]:
    """
    Obtener resumen completo para el dashboard de administrador.
    
    Returns:
        Diccionario con todos los datos para el dashboard
    """
    try:
        from datetime import datetime
        
        client = get_supabase_client()
        now = datetime.now()
        
        # Proyectos activos
        proyectos_activos = client.table('proyectos').select('id', count='exact').eq(
            'estado', 'activo'
        ).execute()
        
        # Empleados activos
        empleados_activos = client.table('empleados').select('id', count='exact').eq(
            'activo', True
        ).execute()
        
        # Total tareas
        tareas = client.table('tareas').select('id, estado', count='exact').execute()
        tareas_pendientes = len([t for t in (tareas.data or []) if t.get('estado') == 'pendiente'])
        tareas_completadas = len([t for t in (tareas.data or []) if t.get('estado') == 'completada'])
        
        # Horas este mes
        fecha_inicio_mes = f"{now.year}-{now.month:02d}-01"
        if now.month == 12:
            fecha_fin_mes = f"{now.year + 1}-01-01"
        else:
            fecha_fin_mes = f"{now.year}-{now.month + 1:02d}-01"
        
        jornadas_mes = client.table('jornadas').select('horas_trabajadas').gte(
            'fecha', fecha_inicio_mes
        ).lt('fecha', fecha_fin_mes).execute()
        horas_mes = sum(j.get('horas_trabajadas', 0) for j in (jornadas_mes.data or []))
        
        # Horas totales
        jornadas_totales = client.table('jornadas').select('horas_trabajadas').execute()
        horas_totales = sum(j.get('horas_trabajadas', 0) for j in (jornadas_totales.data or []))
        
        return {
            'total_proyectos': proyectos_activos.count if proyectos_activos.count else 0,
            'total_empleados': empleados_activos.count if empleados_activos.count else 0,
            'total_tareas': tareas.count if tareas.count else 0,
            'tareas_pendientes': tareas_pendientes,
            'tareas_completadas': tareas_completadas,
            'horas_mes_actual': round(horas_mes, 2),
            'horas_totales': round(horas_totales, 2),
            'mes_actual': now.strftime('%B %Y'),
        }
    except Exception as e:
        print(f"Error en obtener_resumen_dashboard_admin: {e}")
        return {
            'total_proyectos': 0,
            'total_empleados': 0,
            'total_tareas': 0,
            'tareas_pendientes': 0,
            'tareas_completadas': 0,
            'horas_mes_actual': 0.0,
            'horas_totales': 0.0,
            'mes_actual': '',
        }
