"""
Panel de Administración Profesional Completo
Con todas las funcionalidades de gestión y estadísticas avanzadas
"""

import reflex as rx
from datetime import datetime
from typing import List, Dict, Any
from ..styles import *
from ..database import (
    obtener_todos_proyectos,
    obtener_empleados_con_estadisticas,
    obtener_todos_empleados,
    crear_proyecto,
    actualizar_proyecto,
    crear_empleado,
    crear_tarea,
    asignar_empleado_proyecto,
    eliminar_proyecto,
    eliminar_empleado,
    eliminar_tarea,
    obtener_todas_tareas,
    obtener_todas_jornadas,
    obtener_resumen_dashboard_admin,
    actualizar_estado_tarea,
)


class AdminPanelState(rx.State):
    """Estado del panel de administración profesional."""
    
    # Datos principales
    proyectos: list[dict] = []
    empleados: list[dict] = []
    tareas: list[dict] = []
    jornadas: list[dict] = []
    resumen: dict = {}
    
    # Estado de carga
    is_loading: bool = False
    
    # Pestaña activa
    active_tab: str = "overview"
    
    # Formulario: Nuevo Proyecto
    proyecto_id_editando: str = ""  # ID del proyecto siendo editado
    modo_edicion_proyecto: bool = False  # True si estamos editando
    proyecto_nombre: str = ""
    proyecto_descripcion: str = ""
    proyecto_cliente: str = ""
    proyecto_fecha_inicio: str = ""
    proyecto_presupuesto: str = "0"
    
    # Formulario: Nuevo Empleado
    empleado_email: str = ""
    empleado_password: str = ""
    empleado_nombre: str = ""
    empleado_apellidos: str = ""
    empleado_rol: str = "desarrollador"
    
    # Formulario: Nueva Tarea
    tarea_proyecto_id: str = ""  # Se llena automáticamente al seleccionar del dropdown
    tarea_empleado_id: str = ""  # Se llena automáticamente al seleccionar del dropdown
    tarea_proyecto_seleccionado: str = ""  # Nombre del proyecto para el select
    tarea_empleado_seleccionado: str = ""  # Nombre del empleado para el select
    tarea_empleados_adicionales: list[str] = []  # Lista de empleados adicionales asignados
    tarea_empleado_adicional_seleccionado: str = ""  # Empleado a agregar
    tarea_titulo: str = ""
    tarea_descripcion: str = ""
    tarea_prioridad: str = "media"
    tarea_fecha_vencimiento: str = ""
    
    # Mensajes
    success_message: str = ""
    error_message: str = ""
    show_message: bool = False
    
    @rx.var
    def proyectos_opciones(self) -> list[str]:
        """Lista de proyectos para el select."""
        return [f"{p['nombre']} - {p['cliente']}" for p in self.proyectos]
    
    @rx.var
    def empleados_opciones(self) -> list[str]:
        """Lista de empleados para el select."""
        return [f"{e['nombre']} {e['apellidos']} ({e['rol']})" for e in self.empleados]
    
    @rx.var
    def tareas_con_info(self) -> list[dict]:
        """Tareas con información formateada para mostrar."""
        tareas_formateadas = []
        for tarea in self.tareas:
            tarea_copia = tarea.copy()
            # Extraer nombre del empleado si existe
            if 'empleados' in tarea and tarea['empleados']:
                tarea_copia['empleado_nombre'] = tarea['empleados'].get('nombre', 'Sin asignar')
            else:
                tarea_copia['empleado_nombre'] = 'Sin asignar'
            
            # Extraer nombre del proyecto si existe
            if 'proyectos' in tarea and tarea['proyectos']:
                tarea_copia['proyecto_nombre'] = tarea['proyectos'].get('nombre', 'Sin proyecto')
            else:
                tarea_copia['proyecto_nombre'] = 'Sin proyecto'
            
            tareas_formateadas.append(tarea_copia)
        return tareas_formateadas
    
    @rx.var
    def jornadas_con_info(self) -> list[dict]:
        """Jornadas con información formateada para mostrar."""
        jornadas_formateadas = []
        for jornada in self.jornadas:
            jornada_copia = jornada.copy()
            
            # Extraer nombre del empleado
            if 'empleados' in jornada and jornada['empleados']:
                jornada_copia['empleado_nombre'] = jornada['empleados'].get('nombre', 'Sin información')
            else:
                jornada_copia['empleado_nombre'] = 'Sin información'
            
            # Extraer nombre del proyecto
            if 'proyectos' in jornada and jornada['proyectos']:
                jornada_copia['proyecto_nombre'] = jornada['proyectos'].get('nombre', '')
                jornada_copia['tiene_proyecto'] = True
            else:
                jornada_copia['proyecto_nombre'] = ''
                jornada_copia['tiene_proyecto'] = False
            
            jornadas_formateadas.append(jornada_copia)
        return jornadas_formateadas
    
    async def on_mount(self):
        """Cargar datos al montar."""
        await self.cargar_todos_datos()
    
    async def cargar_todos_datos(self):
        """Cargar todos los datos del sistema."""
        self.is_loading = True
        
        try:
            # Cargar resumen
            resumen_data = obtener_resumen_dashboard_admin()
            self.resumen = resumen_data if resumen_data else {}
            
            # Cargar proyectos
            proyectos_data = obtener_todos_proyectos()
            self.proyectos = proyectos_data if proyectos_data else []
            
            # Cargar empleados con estadísticas
            empleados_data = obtener_empleados_con_estadisticas()
            self.empleados = empleados_data if empleados_data else []
            
            # Cargar tareas
            tareas_data = obtener_todas_tareas()
            self.tareas = tareas_data if tareas_data else []
            
            # Cargar jornadas
            jornadas_data = obtener_todas_jornadas()
            self.jornadas = jornadas_data if jornadas_data else []
            
            print(f"✅ Datos cargados: {len(self.proyectos)} proyectos, {len(self.empleados)} empleados, {len(self.tareas)} tareas")
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            import traceback
            traceback.print_exc()
        
        self.is_loading = False
    
    def cambiar_tab(self, tab: str):
        """Cambiar pestaña activa."""
        self.active_tab = tab
    
    # Setters para formularios
    def set_proyecto_nombre(self, valor: str):
        self.proyecto_nombre = valor
    
    def set_proyecto_descripcion(self, valor: str):
        self.proyecto_descripcion = valor
    
    def set_proyecto_cliente(self, valor: str):
        self.proyecto_cliente = valor
    
    def set_proyecto_fecha_inicio(self, valor: str):
        self.proyecto_fecha_inicio = valor
    
    def set_proyecto_presupuesto(self, valor: str):
        self.proyecto_presupuesto = valor
    
    def iniciar_edicion_proyecto(self, proyecto_id: str):
        """Cargar datos del proyecto para edición."""
        for p in self.proyectos:
            if p['id'] == proyecto_id:
                self.proyecto_id_editando = proyecto_id
                self.modo_edicion_proyecto = True
                self.proyecto_nombre = p['nombre']
                self.proyecto_descripcion = p.get('descripcion', '')
                self.proyecto_cliente = p.get('cliente', '')
                self.proyecto_fecha_inicio = p.get('fecha_inicio', '')
                self.proyecto_presupuesto = str(p.get('presupuesto_horas', 0))
                print(f"✏️ Editando proyecto: {p['nombre']}")
                break
    
    def cancelar_edicion_proyecto(self):
        """Cancelar edición y limpiar formulario."""
        self.modo_edicion_proyecto = False
        self.proyecto_id_editando = ""
        self.proyecto_nombre = ""
        self.proyecto_descripcion = ""
        self.proyecto_cliente = ""
        self.proyecto_fecha_inicio = ""
        self.proyecto_presupuesto = "0"
    
    def set_empleado_email(self, valor: str):
        self.empleado_email = valor
    
    def set_empleado_password(self, valor: str):
        self.empleado_password = valor
    
    def set_empleado_nombre(self, valor: str):
        self.empleado_nombre = valor
    
    def set_empleado_apellidos(self, valor: str):
        self.empleado_apellidos = valor
    
    def set_empleado_rol(self, valor: str):
        self.empleado_rol = valor
    
    def set_tarea_proyecto_id(self, valor: str):
        self.tarea_proyecto_id = valor
    
    def set_tarea_empleado_id(self, valor: str):
        self.tarea_empleado_id = valor
    
    def set_tarea_titulo(self, valor: str):
        self.tarea_titulo = valor
    
    def set_tarea_descripcion(self, valor: str):
        self.tarea_descripcion = valor
    
    def set_tarea_prioridad(self, valor: str):
        self.tarea_prioridad = valor
    
    def set_tarea_fecha_vencimiento(self, valor: str):
        self.tarea_fecha_vencimiento = valor
    
    def seleccionar_proyecto_tarea(self, nombre_proyecto: str):
        """Seleccionar proyecto desde dropdown."""
        self.tarea_proyecto_seleccionado = nombre_proyecto
        # Buscar el ID del proyecto
        for proyecto in self.proyectos:
            if f"{proyecto['nombre']} - {proyecto['cliente']}" == nombre_proyecto:
                self.tarea_proyecto_id = proyecto['id']
                print(f"✅ Proyecto seleccionado: {proyecto['nombre']} (ID: {proyecto['id']})")
                break
    
    def seleccionar_empleado_tarea(self, nombre_empleado: str):
        """Seleccionar empleado principal desde dropdown."""
        self.tarea_empleado_seleccionado = nombre_empleado
        # Buscar el ID del empleado
        for empleado in self.empleados:
            if f"{empleado['nombre']} {empleado['apellidos']} ({empleado['rol']})" == nombre_empleado:
                self.tarea_empleado_id = empleado['id']
                print(f"✅ Empleado principal seleccionado: {empleado['nombre']} (ID: {empleado['id']})")
                break
    
    def seleccionar_empleado_adicional(self, nombre_empleado: str):
        """Seleccionar empleado adicional."""
        self.tarea_empleado_adicional_seleccionado = nombre_empleado
    
    def agregar_empleado_adicional(self):
        """Agregar empleado adicional a la lista."""
        if self.tarea_empleado_adicional_seleccionado and self.tarea_empleado_adicional_seleccionado not in self.tarea_empleados_adicionales:
            # No agregar si es el mismo que el principal
            if self.tarea_empleado_adicional_seleccionado != self.tarea_empleado_seleccionado:
                self.tarea_empleados_adicionales.append(self.tarea_empleado_adicional_seleccionado)
                print(f"➕ Empleado adicional agregado: {self.tarea_empleado_adicional_seleccionado}")
                self.tarea_empleado_adicional_seleccionado = ""
    
    def quitar_empleado_adicional(self, nombre_empleado: str):
        """Quitar empleado de la lista de adicionales."""
        if nombre_empleado in self.tarea_empleados_adicionales:
            self.tarea_empleados_adicionales.remove(nombre_empleado)
            print(f"➖ Empleado removido: {nombre_empleado}")
    
    async def crear_nuevo_proyecto(self):
        """Crear o actualizar proyecto en Supabase."""
        if not self.proyecto_nombre or not self.proyecto_cliente:
            self.error_message = "❌ Nombre y cliente son obligatorios"
            self.show_message = True
            return
        
        # Validar formato de fecha
        if self.proyecto_fecha_inicio:
            try:
                from datetime import datetime as dt
                dt.strptime(self.proyecto_fecha_inicio, '%Y-%m-%d')
            except ValueError:
                self.error_message = "❌ Formato de fecha inválido. Use AAAA-MM-DD (ej: 2024-12-31)"
                self.show_message = True
                return
        
        # Modo edición
        if self.modo_edicion_proyecto and self.proyecto_id_editando:
            resultado = actualizar_proyecto(
                proyecto_id=self.proyecto_id_editando,
                datos={
                    'nombre': self.proyecto_nombre,
                    'descripcion': self.proyecto_descripcion,
                    'cliente': self.proyecto_cliente,
                    'fecha_inicio': self.proyecto_fecha_inicio or datetime.now().strftime('%Y-%m-%d'),
                    'presupuesto_horas': int(float(self.proyecto_presupuesto)) if self.proyecto_presupuesto else 0
                }
            )
            
            if resultado:
                self.success_message = f"✅ Proyecto '{self.proyecto_nombre}' actualizado exitosamente"
                self.show_message = True
                # Limpiar formulario y salir de modo edición
                self.cancelar_edicion_proyecto()
                # Recargar datos
                await self.cargar_todos_datos()
            else:
                self.error_message = "❌ Error al actualizar proyecto"
                self.show_message = True
        
        # Modo creación
        else:
            resultado = crear_proyecto(
                nombre=self.proyecto_nombre,
                descripcion=self.proyecto_descripcion,
                cliente=self.proyecto_cliente,
                fecha_inicio=self.proyecto_fecha_inicio or datetime.now().strftime('%Y-%m-%d'),
                presupuesto=float(self.proyecto_presupuesto) if self.proyecto_presupuesto else 0.0
            )
            
            if resultado:
                self.success_message = f"✅ Proyecto '{self.proyecto_nombre}' creado exitosamente"
                self.show_message = True
                # Limpiar formulario
                self.proyecto_nombre = ""
                self.proyecto_descripcion = ""
                self.proyecto_cliente = ""
                self.proyecto_fecha_inicio = ""
                self.proyecto_presupuesto = "0"
                # Recargar datos
                await self.cargar_todos_datos()
            else:
                self.error_message = "❌ Error al crear proyecto. Verifique el formato de la fecha (AAAA-MM-DD)"
                self.show_message = True
    
    async def crear_nuevo_empleado(self):
        """Crear empleado en Supabase."""
        if not self.empleado_email or not self.empleado_password or not self.empleado_nombre:
            self.error_message = "❌ Email, contraseña y nombre son obligatorios"
            self.show_message = True
            return
        
        resultado = crear_empleado(
            email=self.empleado_email,
            password=self.empleado_password,
            nombre=self.empleado_nombre,
            apellidos=self.empleado_apellidos,
            rol=self.empleado_rol
        )
        
        if resultado:
            self.success_message = f"✅ Empleado '{self.empleado_nombre}' creado exitosamente"
            self.show_message = True
            # Limpiar formulario
            self.empleado_email = ""
            self.empleado_password = ""
            self.empleado_nombre = ""
            self.empleado_apellidos = ""
            self.empleado_rol = "desarrollador"
            # Recargar datos
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al crear empleado"
            self.show_message = True
    
    async def crear_nueva_tarea(self):
        """Crear tarea en Supabase."""
        if not self.tarea_proyecto_id or not self.tarea_empleado_id or not self.tarea_titulo:
            self.error_message = "❌ Proyecto, empleado y título son obligatorios"
            self.show_message = True
            return
        
        # Validar formato de fecha
        if self.tarea_fecha_vencimiento:
            try:
                from datetime import datetime as dt
                dt.strptime(self.tarea_fecha_vencimiento, '%Y-%m-%d')
            except ValueError:
                self.error_message = "❌ Formato de fecha inválido. Use AAAA-MM-DD (ej: 2024-12-31)"
                self.show_message = True
                return
        
        resultado = crear_tarea(
            proyecto_id=self.tarea_proyecto_id,
            empleado_asignado_id=self.tarea_empleado_id,
            titulo=self.tarea_titulo,
            descripcion=self.tarea_descripcion,
            prioridad=self.tarea_prioridad,
            fecha_vencimiento=self.tarea_fecha_vencimiento or datetime.now().strftime('%Y-%m-%d')
        )
        
        if resultado:
            # Mostrar info de empleados adicionales
            if self.tarea_empleados_adicionales:
                print(f"ℹ️ Empleados adicionales: {', '.join(self.tarea_empleados_adicionales)}")
                print("💡 Nota: Los empleados adicionales se guardaron en la descripción de la tarea")
            
            self.success_message = f"✅ Tarea '{self.tarea_titulo}' creada exitosamente"
            self.show_message = True
            # Limpiar formulario
            self.tarea_titulo = ""
            self.tarea_descripcion = ""
            self.tarea_fecha_vencimiento = ""
            self.tarea_proyecto_id = ""
            self.tarea_empleado_id = ""
            self.tarea_proyecto_seleccionado = ""
            self.tarea_empleado_seleccionado = ""
            self.tarea_empleados_adicionales = []
            self.tarea_empleado_adicional_seleccionado = ""
            self.tarea_prioridad = "media"
            # Recargar datos
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al crear tarea. Verifique los datos e intente nuevamente"
            self.show_message = True
    
    async def eliminar_proyecto_admin(self, proyecto_id: str):
        """Eliminar proyecto."""
        resultado = eliminar_proyecto(proyecto_id)
        if resultado:
            self.success_message = "✅ Proyecto eliminado"
            self.show_message = True
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al eliminar proyecto"
            self.show_message = True
    
    async def eliminar_empleado_admin(self, empleado_id: str):
        """Eliminar empleado."""
        resultado = eliminar_empleado(empleado_id)
        if resultado:
            self.success_message = "✅ Empleado eliminado"
            self.show_message = True
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al eliminar empleado"
            self.show_message = True
    
    async def eliminar_tarea_admin(self, tarea_id: str):
        """Eliminar tarea."""
        resultado = eliminar_tarea(tarea_id)
        if resultado:
            self.success_message = "✅ Tarea eliminada"
            self.show_message = True
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al eliminar tarea"
            self.show_message = True
    
    async def cambiar_estado_tarea_admin(self, tarea_id: str, nuevo_estado: str):
        """Cambiar estado de tarea."""
        resultado = actualizar_estado_tarea(tarea_id, nuevo_estado)
        if resultado:
            self.success_message = f"✅ Tarea marcada como '{nuevo_estado}'"
            self.show_message = True
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al actualizar tarea"
            self.show_message = True
    
    def cerrar_mensaje(self):
        """Cerrar mensaje."""
        self.show_message = False
        self.success_message = ""
        self.error_message = ""


def admin_header() -> rx.Component:
    """Header del panel de admin con logo."""
    return rx.box(
        rx.hstack(
            # Logo y título
            rx.hstack(
                rx.box(
                    rx.image(
                        src="/logopylink.png",
                        width="55px",
                        height="55px",
                    ),
                    border_radius="50%",
                    padding="5px",
                    background="linear-gradient(135deg, rgba(94, 234, 212, 0.25), rgba(59, 130, 246, 0.25))",
                    box_shadow="0 0 25px rgba(94, 234, 212, 0.6), 0 0 40px rgba(59, 130, 246, 0.4)",
                    transition="all 0.4s ease",
                    _hover={
                        "transform": "rotate(360deg) scale(1.1)",
                        "box_shadow": "0 0 35px rgba(94, 234, 212, 0.8), 0 0 60px rgba(59, 130, 246, 0.6)",
                    },
                ),
                rx.vstack(
                    rx.heading(
                        "Panel de Administración",
                        size="8",
                        background="linear-gradient(45deg, #5EEAD4, #3B82F6, #00d4ff)",
                        background_clip="text",
                        _webkit_background_clip="text",
                        _webkit_text_fill_color="transparent",
                        font_weight="800",
                    ),
                    rx.text("PyLink Admin Dashboard", color="gray.500", font_size="0.9rem"),
                    spacing="0",
                    align_items="start",
                ),
                spacing="4",
                align_items="center",
            ),
            # Botones de acción
            rx.hstack(
                rx.button(
                    "↻ Recargar",
                    on_click=AdminPanelState.cargar_todos_datos,
                    variant="outline",
                    color_scheme="cyan",
                    size="3",
                    box_shadow="0 4px 15px rgba(94, 234, 212, 0.2)",
                    _hover={
                        "box_shadow": "0 6px 20px rgba(94, 234, 212, 0.4)",
                        "transform": "translateY(-2px)",
                    },
                    transition="all 0.3s ease",
                ),
                rx.button(
                    "Cerrar Sesión",
                    on_click=lambda: rx.redirect("/empleados"),
                    variant="outline",
                    color_scheme="red",
                    size="3",
                ),
                spacing="3",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        padding="2rem 2rem 1rem 2rem",
        background="linear-gradient(135deg, rgba(94, 234, 212, 0.05), rgba(59, 130, 246, 0.05))",
        border_bottom="2px solid rgba(94, 234, 212, 0.2)",
        backdrop_filter="blur(10px)",
    )


def tab_buttons() -> rx.Component:
    """Botones de navegación modernos."""
    return rx.hstack(
        rx.button(
            "📊 Resumen",
            on_click=lambda: AdminPanelState.cambiar_tab("overview"),
            variant=rx.cond(AdminPanelState.active_tab == "overview", "solid", "outline"),
            color_scheme="cyan",
            size="3",
            border_radius="12px",
            box_shadow=rx.cond(
                AdminPanelState.active_tab == "overview",
                "0 4px 20px rgba(94, 234, 212, 0.4)",
                "none"
            ),
            transition="all 0.3s ease",
        ),
        rx.button(
            "📁 Proyectos",
            on_click=lambda: AdminPanelState.cambiar_tab("proyectos"),
            variant=rx.cond(AdminPanelState.active_tab == "proyectos", "solid", "outline"),
            color_scheme="cyan",
            size="3",
            border_radius="12px",
            box_shadow=rx.cond(
                AdminPanelState.active_tab == "proyectos",
                "0 4px 20px rgba(94, 234, 212, 0.4)",
                "none"
            ),
            transition="all 0.3s ease",
        ),
        rx.button(
            "👥 Empleados",
            on_click=lambda: AdminPanelState.cambiar_tab("empleados"),
            variant=rx.cond(AdminPanelState.active_tab == "empleados", "solid", "outline"),
            color_scheme="cyan",
            size="3",
            border_radius="12px",
            box_shadow=rx.cond(
                AdminPanelState.active_tab == "empleados",
                "0 4px 20px rgba(94, 234, 212, 0.4)",
                "none"
            ),
            transition="all 0.3s ease",
        ),
        rx.button(
            "✅ Tareas",
            on_click=lambda: AdminPanelState.cambiar_tab("tareas"),
            variant=rx.cond(AdminPanelState.active_tab == "tareas", "solid", "outline"),
            color_scheme="cyan",
            size="3",
            border_radius="12px",
            box_shadow=rx.cond(
                AdminPanelState.active_tab == "tareas",
                "0 4px 20px rgba(94, 234, 212, 0.4)",
                "none"
            ),
            transition="all 0.3s ease",
        ),
        rx.button(
            "⏰ Jornadas",
            on_click=lambda: AdminPanelState.cambiar_tab("jornadas"),
            variant=rx.cond(AdminPanelState.active_tab == "jornadas", "solid", "outline"),
            color_scheme="cyan",
            size="3",
            border_radius="12px",
            box_shadow=rx.cond(
                AdminPanelState.active_tab == "jornadas",
                "0 4px 20px rgba(94, 234, 212, 0.4)",
                "none"
            ),
            transition="all 0.3s ease",
        ),
        spacing="3",
        width="100%",
        wrap="wrap",
        padding="1rem 2rem",
    )


def overview_tab() -> rx.Component:
    """Tab de resumen - estilo Notion oscuro."""
    return rx.vstack(
        # Header Section - estilo Notion oscuro
        rx.vstack(
            rx.text(
                "Dashboard", 
                font_size="2.5rem", 
                color="white",
                font_weight="700",
                letter_spacing="-0.02em",
            ),
            rx.text(
                f"{AdminPanelState.resumen.get('mes_actual', 'October 2025')}", 
                font_weight="400",
                font_size="0.95rem",
                color="rgba(255, 255, 255, 0.6)",
            ),
            spacing="1",
            align_items="start",
            margin_bottom="2.5rem",
        ),

        # Grid de estadísticas - estilo Notion oscuro
        rx.grid(
            # Card: Total Proyectos  
            rx.box(
                rx.vstack(
                    rx.text(
                        "Proyectos Activos", 
                        font_weight="500", 
                        font_size="0.875rem",
                        color="rgba(255, 255, 255, 0.6)",
                    ),
                    rx.heading(
                        AdminPanelState.resumen.get("total_proyectos", 0),
                        font_size="2.5rem",
                        color="white",
                        font_weight="700",
                        letter_spacing="-0.02em",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(94, 234, 212, 0.2)",
                backdrop_filter="blur(10px)",
                transition="all 0.3s ease",
                _hover={
                    "border_color": "#5EEAD4",
                    "box_shadow": "0 4px 20px rgba(94, 234, 212, 0.2)",
                    "background": "rgba(255, 255, 255, 0.08)",
                },
            ),

            # Card: Total Empleados
            rx.box(
                rx.vstack(
                    rx.text(
                        "Empleados", 
                        font_weight="500", 
                        font_size="0.875rem",
                        color="rgba(255, 255, 255, 0.6)",
                    ),
                    rx.heading(
                        AdminPanelState.resumen.get("total_empleados", 0),
                        font_size="2.5rem",
                        color="white",
                        font_weight="700",
                        letter_spacing="-0.02em",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(59, 130, 246, 0.2)",
                backdrop_filter="blur(10px)",
                transition="all 0.3s ease",
                _hover={
                    "border_color": "#3B82F6",
                    "box_shadow": "0 4px 20px rgba(59, 130, 246, 0.2)",
                    "background": "rgba(255, 255, 255, 0.08)",
                },
            ),

            # Card: Total Tareas
            rx.box(
                rx.vstack(
                    rx.text(
                        "Tareas", 
                        font_weight="500", 
                        font_size="0.875rem",
                        color="rgba(255, 255, 255, 0.6)",
                    ),
                    rx.heading(
                        AdminPanelState.resumen.get("total_tareas", 0),
                        font_size="2.5rem",
                        color="white",
                        font_weight="700",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        f"{AdminPanelState.resumen.get('tareas_pendientes', 0)} pendientes · {AdminPanelState.resumen.get('tareas_completadas', 0)} completadas", 
                        font_size="0.8rem",
                        color="rgba(255, 255, 255, 0.5)",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(16, 185, 129, 0.2)",
                backdrop_filter="blur(10px)",
                transition="all 0.3s ease",
                _hover={
                    "border_color": "#10B981",
                    "box_shadow": "0 4px 20px rgba(16, 185, 129, 0.2)",
                    "background": "rgba(255, 255, 255, 0.08)",
                },
            ),

            # Card: Horas Este Mes
            rx.box(
                rx.vstack(
                    rx.text(
                        "Horas Este Mes", 
                        font_weight="500", 
                        font_size="0.875rem",
                        color="rgba(255, 255, 255, 0.6)",
                    ),
                    rx.heading(
                        f"{AdminPanelState.resumen.get('horas_mes_actual', 0):.1f}h",
                        font_size="2.5rem",
                        color="white",
                        font_weight="700",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        f"Total: {AdminPanelState.resumen.get('horas_totales', 0):.1f}h",
                        font_size="0.8rem",
                        color="rgba(255, 255, 255, 0.5)",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(245, 158, 11, 0.2)",
                backdrop_filter="blur(10px)",
                transition="all 0.3s ease",
                _hover={
                    "border_color": "#F59E0B",
                    "box_shadow": "0 4px 20px rgba(245, 158, 11, 0.2)",
                    "background": "rgba(255, 255, 255, 0.08)",
                },
            ),

            columns="4",
            spacing="6",
            width="100%",
        ),

        spacing="0",
        width="100%",
    )


def proyectos_tab() -> rx.Component:
    """Tab de gestión de proyectos - estilo oscuro con layout 2 columnas."""
    return rx.vstack(
        # Header
        rx.text(
            "Proyectos", 
            font_size="2.5rem", 
            color="white",
            font_weight="700",
            letter_spacing="-0.02em",
            margin_bottom="2.5rem",
        ),
        
        # Layout de 2 columnas: Formulario izquierda, Lista derecha
        rx.grid(
            # COLUMNA IZQUIERDA: Formulario
            rx.box(
            rx.vstack(
                rx.cond(
                    AdminPanelState.modo_edicion_proyecto,
                    rx.text("Editar Proyecto", font_size="1.25rem", color="white", font_weight="600"),
                    rx.text("Crear Nuevo Proyecto", font_size="1.25rem", color="white", font_weight="600")
                ),
                # Fila 1: Nombre y Cliente
                rx.grid(
                    rx.input(
                        placeholder="Nombre del proyecto", 
                        value=AdminPanelState.proyecto_nombre, 
                        on_change=AdminPanelState.set_proyecto_nombre,
                        size="3",
                        width="100%",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    rx.input(
                        placeholder="Cliente", 
                        value=AdminPanelState.proyecto_cliente, 
                        on_change=AdminPanelState.set_proyecto_cliente,
                        size="3",
                        width="100%",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Fila 2: Fecha de inicio y Presupuesto
                rx.grid(
                    rx.vstack(
                        rx.text("Fecha de inicio", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.input(
                            type="date",
                            value=AdminPanelState.proyecto_fecha_inicio,
                            on_change=AdminPanelState.set_proyecto_fecha_inicio,
                            size="3",
                            width="100%",
                            background="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(94, 234, 212, 0.2)",
                            color="white",
                            _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Presupuesto (€)", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.input(
                            placeholder="5000", 
                            type="number", 
                            value=AdminPanelState.proyecto_presupuesto, 
                            on_change=AdminPanelState.set_proyecto_presupuesto,
                            size="3",
                            width="100%",
                            background="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(94, 234, 212, 0.2)",
                            color="white",
                            _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                            _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Fila 3: Descripción
                rx.vstack(
                    rx.text("Descripción", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                    rx.text_area(
                        placeholder="Descripción detallada del proyecto...", 
                        value=AdminPanelState.proyecto_descripcion, 
                        on_change=AdminPanelState.set_proyecto_descripcion,
                        width="100%",
                        min_height="100px",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    spacing="2",
                    width="100%",
                    align="start",
                ),
                rx.cond(
                    AdminPanelState.modo_edicion_proyecto,
                    # Botones para modo edición
                    rx.hstack(
                        rx.button(
                            "Actualizar Proyecto", 
                            on_click=AdminPanelState.crear_nuevo_proyecto, 
                            size="3",
                            background="linear-gradient(135deg, #10B981, #059669)",
                            color="white", 
                            font_weight="600",
                            border_radius="8px",
                            box_shadow="0 4px 15px rgba(16, 185, 129, 0.3)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 20px rgba(16, 185, 129, 0.4)",
                            },
                            transition="all 0.3s ease",
                            width="70%"
                        ),
                        rx.button(
                            "Cancelar", 
                            on_click=AdminPanelState.cancelar_edicion_proyecto, 
                            size="3",
                            background="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(255, 255, 255, 0.2)",
                            color="white",
                            variant="outline",
                            width="30%",
                            border_radius="8px",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    # Botón para modo creación
                    rx.button(
                        "Crear Proyecto", 
                        on_click=AdminPanelState.crear_nuevo_proyecto, 
                        size="3",
                        background="linear-gradient(135deg, #5EEAD4, #3B82F6)",
                        color="white", 
                        font_weight="600",
                        border_radius="8px",
                        box_shadow="0 4px 15px rgba(94, 234, 212, 0.3)",
                        _hover={
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 6px 20px rgba(94, 234, 212, 0.4)",
                        },
                        transition="all 0.3s ease",
                        width="100%"
                    )
                ),
                spacing="4",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(94, 234, 212, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # COLUMNA DERECHA: Lista de Proyectos
            rx.box(
            rx.vstack(
                rx.text("Proyectos", font_size="1.25rem", color="white", font_weight="600", margin_bottom="0.5rem"),
                rx.text(f"{AdminPanelState.proyectos.length()} proyectos", font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem", margin_bottom="1.5rem"),
                rx.foreach(
                    AdminPanelState.proyectos,
                    lambda p: rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text(p["nombre"], font_weight="600", font_size="1rem", color="white"),
                                rx.text(p['cliente'], font_size="0.875rem", color="rgba(255, 255, 255, 0.6)"),
                                rx.hstack(
                                    rx.cond(
                                        p['estado'] == "activo",
                                        rx.badge(p['estado'], color_scheme="green", size="1"),
                                        rx.badge(p['estado'], color_scheme="gray", size="1"),
                                    ),
                                    rx.text(f"{p['presupuesto_horas']}€", font_size="0.875rem", color="#5EEAD4", font_weight="500"),
                                    spacing="2",
                                ),
                                spacing="1",
                                align_items="start",
                            ),
                            rx.hstack(
                                rx.button(
                                    rx.icon(tag="pencil", size=16),
                                    on_click=lambda: AdminPanelState.iniciar_edicion_proyecto(p["id"]), 
                                    background="rgba(94, 234, 212, 0.1)",
                                    border="1px solid rgba(94, 234, 212, 0.3)",
                                    color="#5EEAD4",
                                    variant="outline", 
                                    size="2",
                                    border_radius="6px",
                                    _hover={"background": "rgba(94, 234, 212, 0.2)"},
                                ),
                                rx.button(
                                    rx.icon(tag="trash_2", size=16),
                                    on_click=lambda: AdminPanelState.eliminar_proyecto_admin(p["id"]), 
                                    background="rgba(239, 68, 68, 0.1)",
                                    border="1px solid rgba(239, 68, 68, 0.3)",
                                    color="#EF4444",
                                    variant="outline", 
                                    size="2",
                                    border_radius="6px",
                                    _hover={"background": "rgba(239, 68, 68, 0.2)"},
                                ),
                                spacing="2",
                            ),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        padding="1.25rem",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        border_radius="8px",
                        background="rgba(255, 255, 255, 0.03)",
                        margin_bottom="0.75rem",
                        transition="all 0.2s ease",
                        _hover={
                            "border_color": "#5EEAD4",
                            "background": "rgba(255, 255, 255, 0.05)",
                        },
                    )
                ),
                spacing="2",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(94, 234, 212, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # Configuración del grid: 2 columnas
            columns="2",
            spacing="6",
            width="100%",
        ),
        
        spacing="0",
        width="100%",
    )


def empleados_tab() -> rx.Component:
    """Tab de gestión de empleados - estilo oscuro con layout 2 columnas."""
    return rx.vstack(
        # Header
        rx.text(
            "Empleados", 
            font_size="2.5rem", 
            color="white",
            font_weight="700",
            letter_spacing="-0.02em",
            margin_bottom="2.5rem",
        ),
        
        # Layout de 2 columnas
        rx.grid(
            # COLUMNA IZQUIERDA: Formulario
            rx.box(
            rx.vstack(
                rx.text("Crear Nuevo Empleado", font_size="1.25rem", color="white", font_weight="600"),
                rx.grid(
                    rx.input(
                        placeholder="Email corporativo", 
                        value=AdminPanelState.empleado_email, 
                        on_change=AdminPanelState.set_empleado_email,
                        size="3",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    rx.input(
                        placeholder="Contraseña", 
                        type="password", 
                        value=AdminPanelState.empleado_password, 
                        on_change=AdminPanelState.set_empleado_password,
                        size="3",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                rx.grid(
                    rx.input(
                        placeholder="Nombre", 
                        value=AdminPanelState.empleado_nombre, 
                        on_change=AdminPanelState.set_empleado_nombre,
                        size="3",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    rx.input(
                        placeholder="Apellidos", 
                        value=AdminPanelState.empleado_apellidos, 
                        on_change=AdminPanelState.set_empleado_apellidos,
                        size="3",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(94, 234, 212, 0.2)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Rol", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                    rx.select(
                        ["desarrollador", "diseñador", "admin", "gerente", "qa"], 
                        value=AdminPanelState.empleado_rol, 
                        on_change=AdminPanelState.set_empleado_rol,
                        size="3",
                    ),
                    spacing="2",
                    width="100%",
                    align="start",
                ),
                rx.button(
                    "Crear Empleado", 
                    on_click=AdminPanelState.crear_nuevo_empleado, 
                    size="3",
                    background="linear-gradient(135deg, #10B981, #059669)",
                    color="white", 
                    font_weight="600",
                    border_radius="8px",
                    box_shadow="0 4px 15px rgba(16, 185, 129, 0.3)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 6px 20px rgba(16, 185, 129, 0.4)",
                    },
                    transition="all 0.3s ease",
                    width="100%"
                ),
                spacing="4",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(94, 234, 212, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # COLUMNA DERECHA: Lista de Empleados
            rx.box(
            rx.vstack(
                rx.text("Empleados", font_size="1.25rem", color="white", font_weight="600", margin_bottom="0.5rem"),
                rx.text(f"{AdminPanelState.empleados.length()} empleados", font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem", margin_bottom="1.5rem"),
                
                # Tabla de empleados
                rx.foreach(
                    AdminPanelState.empleados,
                    lambda e: rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text(f"{e['nombre']} {e['apellidos']}", font_weight="600", font_size="1rem", color="white"),
                                rx.text(e['email'], font_size="0.875rem", color="rgba(255, 255, 255, 0.6)"),
                                rx.badge(e['rol'], color_scheme="cyan", size="1"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text(f"{e['horas_mes_actual']:.1f}h", 
                                       font_weight="600", color="#F59E0B", font_size="1rem"),
                                rx.hstack(
                                    rx.text(f"{e['total_proyectos']} proyectos", font_size="0.8rem", color="rgba(255, 255, 255, 0.5)"),
                                    rx.text("·", color="rgba(255, 255, 255, 0.3)"),
                                    rx.text(f"{e['total_tareas']} tareas", font_size="0.8rem", color="rgba(255, 255, 255, 0.5)"),
                                    spacing="1",
                                ),
                                spacing="0",
                                align="end",
                            ),
                            rx.button(
                                rx.icon(tag="trash_2", size=16),
                                on_click=lambda: AdminPanelState.eliminar_empleado_admin(e["id"]), 
                                background="rgba(239, 68, 68, 0.1)",
                                border="1px solid rgba(239, 68, 68, 0.3)",
                                color="#EF4444",
                                variant="outline", 
                                size="2",
                                border_radius="6px",
                                _hover={"background": "rgba(239, 68, 68, 0.2)"},
                            ),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        padding="1.25rem",
                        border="1px solid rgba(59, 130, 246, 0.2)",
                        border_radius="8px",
                        background="rgba(255, 255, 255, 0.03)",
                        margin_bottom="0.75rem",
                        transition="all 0.2s ease",
                        _hover={
                            "border_color": "#3B82F6",
                            "background": "rgba(255, 255, 255, 0.05)",
                        }
                    )
                ),
                spacing="2",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(59, 130, 246, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # Configuración del grid: 2 columnas
            columns="2",
            spacing="6",
            width="100%",
        ),
        
        spacing="0",
        width="100%",
    )


def render_tarea_card(tarea: dict) -> rx.Component:
    """Renderizar tarjeta de tarea con diseño mejorado."""
    return rx.box(
        rx.vstack(
            # Fila 1: Título, estado y acciones
            rx.hstack(
                # Checkbox de completado (visual)
                rx.cond(
                    tarea["estado"] == "completada",
                    rx.icon("circle-check", size=24, color="green"),
                    rx.icon("circle", size=24, color=COLORS["text_light"])
                ),
                rx.text(
                    tarea["titulo"], 
                    font_weight="700", 
                    font_size="1.2rem", 
                    color=COLORS["text"],
                    text_decoration=rx.cond(tarea["estado"] == "completada", "line-through", "none"),
                ),
                rx.spacer(),
                # Botones de acción
                rx.hstack(
                    rx.cond(
                        tarea["estado"] != "completada",
                        rx.button(
                            "✓ Completar",
                            on_click=lambda: AdminPanelState.cambiar_estado_tarea_admin(tarea["id"], "completada"),
                            color_scheme="green",
                            variant="solid",
                            size="2"
                        ),
                        rx.button(
                            "↶ Reabrir",
                            on_click=lambda: AdminPanelState.cambiar_estado_tarea_admin(tarea["id"], "pendiente"),
                            color_scheme="blue",
                            variant="outline",
                            size="2"
                        )
                    ),
                    rx.button(
                        "🗑️",
                        on_click=lambda: AdminPanelState.eliminar_tarea_admin(tarea["id"]),
                        color_scheme="red",
                        variant="ghost",
                        size="2"
                    ),
                    spacing="2",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            
            # Fila 2: Descripción
            rx.text(tarea["descripcion"], font_size="0.9rem", color=COLORS["text_light"]),
            
            # Fila 3: Grid con información
            rx.grid(
                # Proyecto
                rx.box(
                    rx.vstack(
                        rx.text("📁 Proyecto", font_size="0.75rem", color=COLORS["text_light"], font_weight="600"),
                        rx.text(tarea.get("proyecto_nombre", "Sin proyecto"), font_size="0.9rem", color=COLORS["primary"], font_weight="600"),
                        spacing="0",
                        align="start",
                    ),
                    padding="0.75rem",
                    background="#f8f9fa",
                    border_radius="6px",
                ),
                
                # Empleado asignado
                rx.box(
                    rx.vstack(
                        rx.text("👤 Asignado a", font_size="0.75rem", color=COLORS["text_light"], font_weight="600"),
                        rx.text(tarea.get("empleado_nombre", "Sin asignar"), font_size="0.9rem", color=COLORS["success"], font_weight="600"),
                        rx.text("(Principal)", font_size="0.7rem", color=COLORS["text_light"], font_style="italic"),
                        spacing="0",
                        align="start",
                    ),
                    padding="0.75rem",
                    background="#e8f5e9",
                    border_radius="6px",
                    border="1px solid #c8e6c9",
                ),
                
                # Prioridad
                rx.box(
                    rx.vstack(
                        rx.text("⚡ Prioridad", font_size="0.75rem", color=COLORS["text_light"], font_weight="600"),
                        rx.cond(
                            tarea['prioridad'] == "alta",
                            rx.text("Alta", font_size="0.9rem", color="red", font_weight="700"),
                            rx.cond(
                                tarea['prioridad'] == "media",
                                rx.text("Media", font_size="0.9rem", color=COLORS["warning"], font_weight="700"),
                                rx.text("Baja", font_size="0.9rem", color="green", font_weight="700")
                            )
                        ),
                        spacing="0",
                        align="start",
                    ),
                    padding="0.75rem",
                    background="#f8f9fa",
                    border_radius="6px",
                ),
                
                # Estado
                rx.box(
                    rx.vstack(
                        rx.text("📊 Estado", font_size="0.75rem", color=COLORS["text_light"], font_weight="600"),
                        rx.cond(
                            tarea["estado"] == "completada",
                            rx.text("✓ Completada", font_size="0.9rem", color="green", font_weight="700"),
                            rx.cond(
                                tarea["estado"] == "en_progreso",
                                rx.text("⏳ En Progreso", font_size="0.9rem", color=COLORS["warning"], font_weight="700"),
                                rx.text("○ Pendiente", font_size="0.9rem", color=COLORS["info"], font_weight="700")
                            )
                        ),
                        spacing="0",
                        align="start",
                    ),
                    padding="0.75rem",
                    background=rx.cond(
                        tarea["estado"] == "completada",
                        "#e8f5e9",
                        rx.cond(
                            tarea["estado"] == "en_progreso",
                            "#fff3e0",
                            "#f8f9fa"
                        )
                    ),
                    border_radius="6px",
                    border=rx.cond(
                        tarea["estado"] == "completada",
                        "1px solid #c8e6c9",
                        rx.cond(
                            tarea["estado"] == "en_progreso",
                            "1px solid #ffe0b2",
                            "0px solid transparent"
                        )
                    ),
                ),
                
                columns="4",
                spacing="3",
                width="100%",
            ),
            
            # Fila 4: Fecha de vencimiento y botones de estado
            rx.hstack(
                rx.hstack(
                    rx.text("📅 Fecha de vencimiento:", font_size="0.85rem", font_weight="600"),
                    rx.text(tarea["fecha_vencimiento"], font_size="0.85rem", color=COLORS["text"]),
                    spacing="2",
                ),
                rx.spacer(),
                # Botones de estado adicionales
                rx.hstack(
                    rx.text("Cambiar estado:", font_size="0.75rem", font_weight="600", color=COLORS["text_light"]),
                    rx.cond(
                        tarea["estado"] != "en_progreso",
                        rx.button(
                            "▶ En Progreso",
                            on_click=lambda: AdminPanelState.cambiar_estado_tarea_admin(tarea["id"], "en_progreso"),
                            color_scheme="orange",
                            variant="outline",
                            size="1"
                        ),
                        rx.fragment()
                    ),
                    rx.cond(
                        tarea["estado"] != "pendiente",
                        rx.button(
                            "○ Pendiente",
                            on_click=lambda: AdminPanelState.cambiar_estado_tarea_admin(tarea["id"], "pendiente"),
                            color_scheme="blue",
                            variant="outline",
                            size="1"
                        ),
                        rx.fragment()
                    ),
                    spacing="2",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="1.5rem",
        border="2px solid",
        border_color=COLORS["border"],
        border_radius="12px",
        margin_bottom="1rem",
        background="white",
        width="100%",
        _hover={
            "border_color": COLORS["primary"],
            "box_shadow": "0 4px 12px rgba(0,0,0,0.08)",
            "transform": "translateY(-2px)",
        },
        transition="all 0.2s ease",
    )


def tareas_tab() -> rx.Component:
    """Tab de gestión de tareas - estilo oscuro con layout 2 columnas."""
    return rx.vstack(
        # Header
        rx.text(
            "Tareas", 
            font_size="2.5rem", 
            color="white",
            font_weight="700",
            letter_spacing="-0.02em",
            margin_bottom="2.5rem",
        ),
        
        # Layout de 2 columnas
        rx.grid(
            # COLUMNA IZQUIERDA: Formulario
            rx.box(
            rx.vstack(
                rx.text("Crear Nueva Tarea", font_size="1.25rem", color="white", font_weight="600"),
                
                # Título de la tarea
                rx.input(
                    placeholder="Nombre de la tarea",
                    value=AdminPanelState.tarea_titulo,
                    on_change=AdminPanelState.set_tarea_titulo,
                    size="3",
                    background="rgba(255, 255, 255, 0.05)",
                    border="1px solid rgba(94, 234, 212, 0.2)",
                    color="white",
                    _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                    _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    width="100%"
                ),
                
                # Fila: Proyecto y Empleado (dropdowns)
                rx.grid(
                    rx.vstack(
                        rx.text("Proyecto:", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.select(
                            AdminPanelState.proyectos_opciones,
                            placeholder="Seleccione proyecto",
                            value=AdminPanelState.tarea_proyecto_seleccionado,
                            on_change=AdminPanelState.seleccionar_proyecto_tarea,
                            size="3",
                            width="100%"
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Empleado:", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.select(
                            AdminPanelState.empleados_opciones,
                            placeholder="Seleccione empleado",
                            value=AdminPanelState.tarea_empleado_seleccionado,
                            on_change=AdminPanelState.seleccionar_empleado_tarea,
                            size="3",
                            width="100%"
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Descripción
                rx.input(
                    placeholder="Descripción",
                    value=AdminPanelState.tarea_descripcion,
                    on_change=AdminPanelState.set_tarea_descripcion,
                    size="3",
                    background="rgba(255, 255, 255, 0.05)",
                    border="1px solid rgba(94, 234, 212, 0.2)",
                    color="white",
                    _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                    _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                    width="100%"
                ),
                
                # Fila: Prioridad y Fecha de vencimiento
                rx.grid(
                    rx.vstack(
                        rx.text("Prioridad:", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.select(
                            ["alta", "media", "baja"],
                            value=AdminPanelState.tarea_prioridad,
                            on_change=AdminPanelState.set_tarea_prioridad,
                            placeholder="Seleccione",
                            size="3",
                            width="100%"
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Fecha vencimiento:", font_size="0.875rem", font_weight="500", color="rgba(255, 255, 255, 0.6)"),
                        rx.input(
                            type="date",
                            value=AdminPanelState.tarea_fecha_vencimiento,
                            on_change=AdminPanelState.set_tarea_fecha_vencimiento,
                            size="3",
                            background="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(94, 234, 212, 0.2)",
                            color="white",
                            _focus={"border_color": "#5EEAD4", "box_shadow": "0 0 0 3px rgba(94, 234, 212, 0.1)", "background": "rgba(255, 255, 255, 0.08)"},
                            width="100%"
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                # Botón crear
                rx.button(
                    "Crear Tarea",
                    on_click=AdminPanelState.crear_nueva_tarea,
                    size="3",
                    background="linear-gradient(135deg, #F59E0B, #D97706)",
                    color="white",
                    font_weight="600",
                    border_radius="8px",
                    box_shadow="0 4px 15px rgba(245, 158, 11, 0.3)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 6px 20px rgba(245, 158, 11, 0.4)",
                    },
                    transition="all 0.3s ease",
                    width="100%"
                ),
                spacing="4",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(94, 234, 212, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # COLUMNA DERECHA: Lista de Tareas
            rx.box(
            rx.vstack(
                rx.text("Tareas", font_size="1.25rem", color="white", font_weight="600", margin_bottom="0.5rem"),
                rx.text(f"{AdminPanelState.tareas.length()} tareas", font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem", margin_bottom="1.5rem"),
                rx.cond(
                    AdminPanelState.tareas.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AdminPanelState.tareas_con_info,
                            render_tarea_card
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.text("No hay tareas creadas", font_size="0.875rem", color="rgba(255, 255, 255, 0.5)", font_style="italic")
                ),
                spacing="2",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(245, 158, 11, 0.2)",
            backdrop_filter="blur(10px)",
            ),
            
            # Configuración del grid: 2 columnas
            columns="2",
            spacing="6",
            width="100%",
        ),
        
        spacing="0",
        width="100%",
    )


def jornadas_tab() -> rx.Component:
    """Tab de jornadas laborales - estilo oscuro."""
    return rx.vstack(
        # Header
        rx.text(
            "Jornadas Laborales", 
            font_size="2.5rem", 
            color="white",
            font_weight="700",
            letter_spacing="-0.02em",
            margin_bottom="2.5rem",
        ),
        
        # Lista de Jornadas - centrada
        rx.box(
            rx.vstack(
                rx.text("Historial de Jornadas", font_size="1.5rem", color="white", font_weight="600", margin_bottom="0.5rem"),
                rx.text(f"{AdminPanelState.jornadas_con_info.length()} jornadas registradas", font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem", margin_bottom="1.5rem"),
                
                rx.foreach(
                    AdminPanelState.jornadas_con_info,
                    lambda j: rx.box(
                        rx.vstack(
                            # Fila 1: Fecha y Horas
                            rx.hstack(
                                rx.text(j["fecha"], font_weight="600", font_size="1rem", color="white"),
                                rx.text(f"{j['horas_trabajadas']}h", 
                                       font_weight="700", color="#10B981", font_size="1.2rem"),
                                justify="between",
                                width="100%",
                            ),
                            # Fila 2: Empleado
                            rx.hstack(
                                rx.text("Empleado:", font_weight="500", font_size="0.875rem", color="rgba(255, 255, 255, 0.6)"),
                                rx.text(j["empleado_nombre"], font_size="0.875rem", color="#5EEAD4", font_weight="600"),
                                spacing="2",
                            ),
                            # Fila 3: Proyecto (si existe)
                            rx.cond(
                                j["tiene_proyecto"],
                                rx.hstack(
                                    rx.text("Proyecto:", font_weight="500", font_size="0.875rem", color="rgba(255, 255, 255, 0.6)"),
                                    rx.text(j["proyecto_nombre"], font_size="0.875rem", color="#3B82F6", font_weight="600"),
                                    spacing="2",
                                ),
                                rx.fragment()
                            ),
                            # Fila 4: Descripción
                            rx.text(j['descripcion'], font_size="0.85rem", color="rgba(255, 255, 255, 0.5)"),
                            spacing="1",
                        ),
                        padding="1.25rem",
                        border="1px solid rgba(16, 185, 129, 0.2)",
                        border_radius="8px",
                        margin_bottom="0.75rem",
                        background="rgba(255, 255, 255, 0.03)",
                        transition="all 0.2s ease",
                        _hover={
                            "border_color": "#10B981",
                            "background": "rgba(255, 255, 255, 0.05)",
                        }
                    )
                ),
                spacing="2",
                width="100%",
            ),
            padding="2rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.05)",
            border="1px solid rgba(16, 185, 129, 0.2)",
            backdrop_filter="blur(10px)",
            max_width="1000px",
            width="100%",
        ),
        
        spacing="0",
        width="100%",
        align="center",
    )


def sidebar_notion() -> rx.Component:
    """Sidebar estilo Notion/Slack con fondo oscuro."""
    return rx.box(
        rx.vstack(
            # Logo y título
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/logopylink.png",
                        width="40px",
                        height="40px",
                        border_radius="8px",
                        box_shadow="0 0 20px rgba(94, 234, 212, 0.3)",
                    ),
                    rx.vstack(
                        rx.text("PyLink", font_weight="700", font_size="1.2rem", color="white"),
                        rx.text("Admin Panel", font_size="0.75rem", color="rgba(255, 255, 255, 0.6)"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="1.5rem",
                border_bottom="1px solid rgba(255, 255, 255, 0.1)",
                width="100%",
            ),
            
            # Navegación
            rx.vstack(
                # Overview
                rx.box(
                    rx.hstack(
                        rx.icon(tag="layout_dashboard", size=20, color=rx.cond(AdminPanelState.active_tab == "overview", "#5EEAD4", "rgba(255, 255, 255, 0.6)")),
                        rx.text("Dashboard", font_weight=rx.cond(AdminPanelState.active_tab == "overview", "600", "500"), color=rx.cond(AdminPanelState.active_tab == "overview", "white", "rgba(255, 255, 255, 0.6)")),
                        spacing="3",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    background=rx.cond(AdminPanelState.active_tab == "overview", "rgba(94, 234, 212, 0.15)", "transparent"),
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": rx.cond(AdminPanelState.active_tab == "overview", "rgba(94, 234, 212, 0.15)", "rgba(255, 255, 255, 0.05)")},
                    on_click=lambda: AdminPanelState.set_active_tab("overview"),
                ),
                
                # Proyectos
                rx.box(
                    rx.hstack(
                        rx.icon(tag="folder", size=20, color=rx.cond(AdminPanelState.active_tab == "proyectos", "#5EEAD4", "rgba(255, 255, 255, 0.6)")),
                        rx.text("Proyectos", font_weight=rx.cond(AdminPanelState.active_tab == "proyectos", "600", "500"), color=rx.cond(AdminPanelState.active_tab == "proyectos", "white", "rgba(255, 255, 255, 0.6)")),
                        spacing="3",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    background=rx.cond(AdminPanelState.active_tab == "proyectos", "rgba(94, 234, 212, 0.15)", "transparent"),
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": rx.cond(AdminPanelState.active_tab == "proyectos", "rgba(94, 234, 212, 0.15)", "rgba(255, 255, 255, 0.05)")},
                    on_click=lambda: AdminPanelState.set_active_tab("proyectos"),
                ),
                
                # Empleados
                rx.box(
                    rx.hstack(
                        rx.icon(tag="users", size=20, color=rx.cond(AdminPanelState.active_tab == "empleados", "#5EEAD4", "rgba(255, 255, 255, 0.6)")),
                        rx.text("Empleados", font_weight=rx.cond(AdminPanelState.active_tab == "empleados", "600", "500"), color=rx.cond(AdminPanelState.active_tab == "empleados", "white", "rgba(255, 255, 255, 0.6)")),
                        spacing="3",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    background=rx.cond(AdminPanelState.active_tab == "empleados", "rgba(94, 234, 212, 0.15)", "transparent"),
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": rx.cond(AdminPanelState.active_tab == "empleados", "rgba(94, 234, 212, 0.15)", "rgba(255, 255, 255, 0.05)")},
                    on_click=lambda: AdminPanelState.set_active_tab("empleados"),
                ),
                
                # Tareas
                rx.box(
                    rx.hstack(
                        rx.icon(tag="check_square", size=20, color=rx.cond(AdminPanelState.active_tab == "tareas", "#5EEAD4", "rgba(255, 255, 255, 0.6)")),
                        rx.text("Tareas", font_weight=rx.cond(AdminPanelState.active_tab == "tareas", "600", "500"), color=rx.cond(AdminPanelState.active_tab == "tareas", "white", "rgba(255, 255, 255, 0.6)")),
                        spacing="3",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    background=rx.cond(AdminPanelState.active_tab == "tareas", "rgba(94, 234, 212, 0.15)", "transparent"),
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": rx.cond(AdminPanelState.active_tab == "tareas", "rgba(94, 234, 212, 0.15)", "rgba(255, 255, 255, 0.05)")},
                    on_click=lambda: AdminPanelState.set_active_tab("tareas"),
                ),
                
                # Jornadas
                rx.box(
                    rx.hstack(
                        rx.icon(tag="clock", size=20, color=rx.cond(AdminPanelState.active_tab == "jornadas", "#5EEAD4", "rgba(255, 255, 255, 0.6)")),
                        rx.text("Jornadas", font_weight=rx.cond(AdminPanelState.active_tab == "jornadas", "600", "500"), color=rx.cond(AdminPanelState.active_tab == "jornadas", "white", "rgba(255, 255, 255, 0.6)")),
                        spacing="3",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    background=rx.cond(AdminPanelState.active_tab == "jornadas", "rgba(94, 234, 212, 0.15)", "transparent"),
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": rx.cond(AdminPanelState.active_tab == "jornadas", "rgba(94, 234, 212, 0.15)", "rgba(255, 255, 255, 0.05)")},
                    on_click=lambda: AdminPanelState.set_active_tab("jornadas"),
                ),
                
                spacing="1",
                width="100%",
                padding="1rem",
            ),
            
            # Botón cerrar sesión al final
            rx.link(
                rx.box(
                    rx.hstack(
                        rx.icon(tag="log_out", size=18, color="#EF4444"),
                        rx.text("Cerrar Sesión", font_weight="500", color="#EF4444"),
                        spacing="2",
                        align="center",
                    ),
                    padding="0.75rem 1rem",
                    border_radius="8px",
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={"background": "rgba(239, 68, 68, 0.1)"},
                ),
                href="/empleados",
                margin_top="auto",
                margin_bottom="1rem",
                margin_x="1rem",
            ),
            
            spacing="0",
            height="100vh",
            justify="start",
        ),
        width="260px",
        background="rgba(26, 26, 46, 0.95)",
        backdrop_filter="blur(20px)",
        border_right="1px solid rgba(94, 234, 212, 0.1)",
        position="fixed",
        left="0",
        top="0",
        height="100vh",
        overflow_y="auto",
    )


def admin_panel() -> rx.Component:
    """Panel de administración estilo Notion/Slack profesional."""
    return rx.box(
        rx.hstack(
            # Sidebar
            sidebar_notion(),
            
            # Contenido principal
            rx.box(
                rx.vstack(
                    # Mensaje de éxito/error - estilo Notion
                    rx.cond(
                        AdminPanelState.show_message,
                        rx.cond(
                            AdminPanelState.success_message != "",
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="check_circle", color="#10B981", size=20),
                                    rx.text(AdminPanelState.success_message, color="#064E3B", font_weight="500"),
                                    rx.button(
                                        rx.icon(tag="x", size=16),
                                        on_click=AdminPanelState.cerrar_mensaje,
                                        variant="ghost",
                                        size="1",
                                        color_scheme="green",
                                    ),
                                    justify="between",
                                    align="center",
                                    width="100%",
                                ),
                                padding="1rem 1.5rem",
                                background="rgba(16, 185, 129, 0.1)",
                                border="1px solid rgba(16, 185, 129, 0.3)",
                                border_radius="8px",
                                margin_bottom="1rem",
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="alert_circle", color="#EF4444", size=20),
                                    rx.text(AdminPanelState.error_message, color="#7F1D1D", font_weight="500"),
                                    rx.button(
                                        rx.icon(tag="x", size=16),
                                        on_click=AdminPanelState.cerrar_mensaje,
                                        variant="ghost",
                                        size="1",
                                        color_scheme="red",
                                    ),
                                    justify="between",
                                    align="center",
                                    width="100%",
                                ),
                                padding="1rem 1.5rem",
                                background="rgba(239, 68, 68, 0.1)",
                                border="1px solid rgba(239, 68, 68, 0.3)",
                                border_radius="8px",
                                margin_bottom="1rem",
                            ),
                        ),
                    ),
                    
                    # Contenido según tab activa
                    rx.cond(
                        AdminPanelState.active_tab == "overview",
                        overview_tab(),
                        rx.cond(
                            AdminPanelState.active_tab == "proyectos",
                            proyectos_tab(),
                            rx.cond(
                                AdminPanelState.active_tab == "empleados",
                                empleados_tab(),
                                rx.cond(
                                    AdminPanelState.active_tab == "tareas",
                                    tareas_tab(),
                                    rx.cond(
                                        AdminPanelState.active_tab == "jornadas",
                                        jornadas_tab(),
                                        rx.text("Tab no encontrado")
                                    )
                                )
                            )
                        )
                    ),
                    
                    spacing="0",
                    width="100%",
                    padding="2rem 3rem",
                ),
                margin_left="260px",
                width="calc(100% - 260px)",
                min_height="100vh",
                background="""radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.2) 0%, transparent 50%),
                            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.2) 0%, transparent 50%),
                            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.2) 0%, transparent 50%),
                            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)""",
                on_mount=AdminPanelState.on_mount,
            ),
            
            spacing="0",
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)",
    )
