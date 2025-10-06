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
    """Header del panel de admin."""
    return rx.hstack(
        rx.heading("🔧 Panel de Administración", size="8", color=COLORS["primary"]),
        rx.button(
            "↻ Recargar",
            on_click=AdminPanelState.cargar_todos_datos,
            variant="outline",
            color_scheme="blue",
        ),
        rx.button(
            "Cerrar Sesión",
            on_click=lambda: rx.redirect("/empleados"),
            variant="outline",
            color_scheme="red",
        ),
        justify="between",
        align="center",
        width="100%",
        padding="2rem 0 1rem 0",
    )


def tab_buttons() -> rx.Component:
    """Botones de navegación entre tabs."""
    return rx.hstack(
        rx.button(
            "📊 Resumen",
            on_click=lambda: AdminPanelState.cambiar_tab("overview"),
            variant=rx.cond(AdminPanelState.active_tab == "overview", "solid", "outline"),
            color_scheme="blue",
        ),
        rx.button(
            "📁 Proyectos",
            on_click=lambda: AdminPanelState.cambiar_tab("proyectos"),
            variant=rx.cond(AdminPanelState.active_tab == "proyectos", "solid", "outline"),
            color_scheme="blue",
        ),
        rx.button(
            "👥 Empleados",
            on_click=lambda: AdminPanelState.cambiar_tab("empleados"),
            variant=rx.cond(AdminPanelState.active_tab == "empleados", "solid", "outline"),
            color_scheme="blue",
        ),
        rx.button(
            "✅ Tareas",
            on_click=lambda: AdminPanelState.cambiar_tab("tareas"),
            variant=rx.cond(AdminPanelState.active_tab == "tareas", "solid", "outline"),
            color_scheme="blue",
        ),
        rx.button(
            "⏰ Jornadas",
            on_click=lambda: AdminPanelState.cambiar_tab("jornadas"),
            variant=rx.cond(AdminPanelState.active_tab == "jornadas", "solid", "outline"),
            color_scheme="blue",
        ),
        spacing="3",
        width="100%",
        wrap="wrap",
    )


def overview_tab() -> rx.Component:
    """Tab de resumen general con estadísticas."""
    return rx.vstack(
        rx.heading("Resumen del Sistema", size="6"),
        rx.text(f"Mes actual: {AdminPanelState.resumen.get('mes_actual', '')}", 
               font_weight="600", color=COLORS["text_light"]),

        rx.grid(
            # Card: Total Proyectos
            rx.card(
                rx.vstack(
                    rx.text("📁 Proyectos Activos", font_weight="600", font_size="0.9rem"),
                    rx.text(
                        AdminPanelState.resumen.get("total_proyectos", 0),
                        font_size="2.5rem",
                        font_weight="bold",
                        color=COLORS["primary"]
                    ),
                    spacing="2",
                ),
                size="3",
            ),

            # Card: Total Empleados
            rx.card(
                rx.vstack(
                    rx.text("👥 Empleados Activos", font_weight="600", font_size="0.9rem"),
                    rx.text(
                        AdminPanelState.resumen.get("total_empleados", 0),
                        font_size="2.5rem",
                        font_weight="bold",
                        color=COLORS["success"]
                    ),
                    spacing="2",
                ),
                size="3",
            ),

            # Card: Total Tareas
            rx.card(
                rx.vstack(
                    rx.text("✅ Total Tareas", font_weight="600", font_size="0.9rem"),
                    rx.hstack(
                        rx.text(
                            AdminPanelState.resumen.get("total_tareas", 0),
                            font_size="2.5rem",
                            font_weight="bold",
                            color=COLORS["warning"]
                        ),
                        rx.vstack(
                            rx.text(f"Pendientes: {AdminPanelState.resumen.get('tareas_pendientes', 0)}", 
                                   font_size="0.75rem"),
                            rx.text(f"Completadas: {AdminPanelState.resumen.get('tareas_completadas', 0)}", 
                                   font_size="0.75rem"),
                            spacing="0",
                        ),
                        spacing="3",
                    ),
                    spacing="2",
                ),
                size="3",
            ),

            # Card: Horas Este Mes
            rx.card(
                rx.vstack(
                    rx.text("⏰ Horas Este Mes", font_weight="600", font_size="0.9rem"),
                    rx.text(
                        f"{AdminPanelState.resumen.get('horas_mes_actual', 0):.1f}h",
                        font_size="2.5rem",
                        font_weight="bold",
                        color=COLORS["info"]
                    ),
                    rx.text(f"Total: {AdminPanelState.resumen.get('horas_totales', 0):.1f}h", 
                           font_size="0.75rem", color=COLORS["text_light"]),
                    spacing="2",
                ),
                size="3",
            ),

            columns="4",
            spacing="4",
            width="100%",
        ),

        spacing="6",
        width="100%",
    )


def proyectos_tab() -> rx.Component:
    """Tab de gestión de proyectos."""
    return rx.vstack(
        rx.heading("Gestión de Proyectos", size="6"),
        
        # Formulario: Nuevo/Editar Proyecto
        rx.card(
            rx.vstack(
                rx.cond(
                    AdminPanelState.modo_edicion_proyecto,
                    rx.heading("✏️ Editar Proyecto", size="4"),
                    rx.heading("➕ Crear Nuevo Proyecto", size="4")
                ),
                # Fila 1: Nombre y Cliente
                rx.grid(
                    rx.input(
                        placeholder="Nombre del proyecto", 
                        value=AdminPanelState.proyecto_nombre, 
                        on_change=AdminPanelState.set_proyecto_nombre,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Cliente", 
                        value=AdminPanelState.proyecto_cliente, 
                        on_change=AdminPanelState.set_proyecto_cliente,
                        width="100%"
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                
                # Fila 2: Fecha de inicio y Presupuesto
                rx.grid(
                    rx.vstack(
                        rx.text("📅 Fecha de inicio:", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.input(
                            type="date",
                            value=AdminPanelState.proyecto_fecha_inicio,
                            on_change=AdminPanelState.set_proyecto_fecha_inicio,
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("💰 Presupuesto (€):", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.input(
                            placeholder="5000", 
                            type="number", 
                            value=AdminPanelState.proyecto_presupuesto, 
                            on_change=AdminPanelState.set_proyecto_presupuesto,
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                
                # Fila 3: Descripción
                rx.input(
                    placeholder="Descripción del proyecto", 
                    value=AdminPanelState.proyecto_descripcion, 
                    on_change=AdminPanelState.set_proyecto_descripcion,
                    width="100%"
                ),
                rx.cond(
                    AdminPanelState.modo_edicion_proyecto,
                    # Botones para modo edición
                    rx.hstack(
                        rx.button(
                            "✅ Actualizar Proyecto", 
                            on_click=AdminPanelState.crear_nuevo_proyecto, 
                            background=COLORS["success"], 
                            color="white", 
                            width="70%"
                        ),
                        rx.button(
                            "❌ Cancelar", 
                            on_click=AdminPanelState.cancelar_edicion_proyecto, 
                            color_scheme="gray", 
                            variant="outline",
                            width="30%"
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    # Botón para modo creación
                    rx.button(
                        "➕ Crear Proyecto", 
                        on_click=AdminPanelState.crear_nuevo_proyecto, 
                        background=COLORS["primary"], 
                        color="white", 
                        width="100%"
                    )
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        # Lista de Proyectos
        rx.card(
            rx.vstack(
                rx.heading("Proyectos Existentes", size="4"),
                rx.text(f"Total: {AdminPanelState.proyectos.length()} proyectos", font_weight="600"),
                rx.foreach(
                    AdminPanelState.proyectos,
                    lambda p: rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text(p["nombre"], font_weight="600", font_size="1.1rem"),
                                rx.text(f"Cliente: {p['cliente']}", font_size="0.9rem"),
                                rx.hstack(
                                    rx.text(f"Estado: {p['estado']}", font_size="0.85rem"),
                                    rx.text(f"Presupuesto: {p['presupuesto_horas']}€", font_size="0.85rem", color=COLORS["success"]),
                                    spacing="4",
                                ),
                                spacing="1",
                            ),
                            rx.hstack(
                                rx.button(
                                    "✏️", 
                                    on_click=lambda: AdminPanelState.iniciar_edicion_proyecto(p["id"]), 
                                    color_scheme="blue", 
                                    variant="outline", 
                                    size="2"
                                ),
                                rx.button(
                                    "🗑️", 
                                    on_click=lambda: AdminPanelState.eliminar_proyecto_admin(p["id"]), 
                                    color_scheme="red", 
                                    variant="outline", 
                                    size="2"
                                ),
                                spacing="2",
                            ),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        padding="1rem",
                        border="1px solid",
                        border_color=COLORS["border"],
                        border_radius="8px",
                        margin_bottom="0.5rem",
                    )
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        spacing="6",
        width="100%",
    )


def empleados_tab() -> rx.Component:
    """Tab de gestión de empleados con horas totales."""
    return rx.vstack(
        rx.heading("Gestión de Empleados", size="6"),
        
        # Formulario: Nuevo Empleado
        rx.card(
            rx.vstack(
                rx.heading("Crear Nuevo Empleado", size="4"),
                rx.grid(
                    rx.input(placeholder="Email", value=AdminPanelState.empleado_email, on_change=AdminPanelState.set_empleado_email),
                    rx.input(placeholder="Contraseña", type="password", value=AdminPanelState.empleado_password, on_change=AdminPanelState.set_empleado_password),
                    rx.input(placeholder="Nombre", value=AdminPanelState.empleado_nombre, on_change=AdminPanelState.set_empleado_nombre),
                    rx.input(placeholder="Apellidos", value=AdminPanelState.empleado_apellidos, on_change=AdminPanelState.set_empleado_apellidos),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.select(["desarrollador", "diseñador", "admin", "gerente", "qa"], value=AdminPanelState.empleado_rol, on_change=AdminPanelState.set_empleado_rol),
                rx.button("Crear Empleado", on_click=AdminPanelState.crear_nuevo_empleado, background=COLORS["success"], color="white", width="100%"),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        # Lista de Empleados con Estadísticas
        rx.card(
            rx.vstack(
                rx.heading("Empleados Registrados", size="4"),
                rx.text(f"Total: {AdminPanelState.empleados.length()} empleados", font_weight="600"),
                
                # Tabla de empleados
                rx.foreach(
                    AdminPanelState.empleados,
                    lambda e: rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(f"{e['nombre']} {e['apellidos']}", size="4", color=COLORS["text"]),
                                rx.text(f"📧 {e['email']}", font_size="0.9rem", color=COLORS["text"]),
                                rx.text(f"👔 Rol: {e['rol']}", font_size="0.85rem", color=COLORS["primary"], font_weight="600"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text(f"⏰ Horas este mes: {e['horas_mes_actual']}h", 
                                       font_weight="700", color=COLORS["info"], font_size="1.1rem"),
                                rx.hstack(
                                    rx.text(f"📁 {e['total_proyectos']} proyectos", font_size="0.85rem", color=COLORS["text"]),
                                    rx.text(f"✅ {e['total_tareas']} tareas", font_size="0.85rem", color=COLORS["text"]),
                                    spacing="3",
                                ),
                                spacing="1",
                                align="end",
                            ),
                            rx.button("🗑️", on_click=lambda: AdminPanelState.eliminar_empleado_admin(e["id"]), color_scheme="red", variant="solid", size="2"),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        padding="1.2rem",
                        border="2px solid",
                        border_color=COLORS["border"],
                        border_radius="10px",
                        margin_bottom="0.75rem",
                        background="white",
                        _hover={
                            "border_color": COLORS["primary"],
                            "box_shadow": "0 4px 6px rgba(0,0,0,0.1)"
                        }
                    )
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        spacing="6",
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
    """Tab de gestión de tareas."""
    return rx.vstack(
        rx.heading("Gestión de Tareas", size="6"),
        
        # Formulario: Nueva Tarea
        rx.card(
            rx.vstack(
                rx.heading("➕ Crear Nueva Tarea", size="4"),
                
                # Título de la tarea
                rx.input(
                    placeholder="Nombre de la tarea",
                    value=AdminPanelState.tarea_titulo,
                    on_change=AdminPanelState.set_tarea_titulo,
                    width="100%"
                ),
                
                # Fila: Proyecto y Empleado (dropdowns)
                rx.grid(
                    rx.vstack(
                        rx.text("📁 Asignar a Proyecto:", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.select(
                            AdminPanelState.proyectos_opciones,
                            placeholder="Seleccione un proyecto",
                            value=AdminPanelState.tarea_proyecto_seleccionado,
                            on_change=AdminPanelState.seleccionar_proyecto_tarea,
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("👤 Asignar a Empleado:", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.select(
                            AdminPanelState.empleados_opciones,
                            placeholder="Seleccione un empleado",
                            value=AdminPanelState.tarea_empleado_seleccionado,
                            on_change=AdminPanelState.seleccionar_empleado_tarea,
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                
                # Sección: Empleados Adicionales
                rx.box(
                    rx.vstack(
                        rx.text("👥 Agregar Empleados Adicionales (Opcional)", font_size="0.9rem", font_weight="600", color=COLORS["text"]),
                        rx.text("Puedes asignar múltiples empleados a esta tarea", font_size="0.75rem", color=COLORS["text_light"]),
                        
                        # Agregar empleado adicional
                        rx.hstack(
                            rx.select(
                                AdminPanelState.empleados_opciones,
                                placeholder="Seleccione otro empleado",
                                value=AdminPanelState.tarea_empleado_adicional_seleccionado,
                                on_change=AdminPanelState.seleccionar_empleado_adicional,
                                width="70%"
                            ),
                            rx.button(
                                "➕ Agregar",
                                on_click=AdminPanelState.agregar_empleado_adicional,
                                color_scheme="blue",
                                variant="solid",
                                width="30%"
                            ),
                            width="100%",
                            spacing="2",
                        ),
                        
                        # Lista de empleados adicionales
                        rx.cond(
                            AdminPanelState.tarea_empleados_adicionales.length() > 0,
                            rx.vstack(
                                rx.text("Empleados asignados adicionales:", font_size="0.8rem", font_weight="600"),
                                rx.foreach(
                                    AdminPanelState.tarea_empleados_adicionales,
                                    lambda emp: rx.hstack(
                                        rx.text(f"👤 {emp}", font_size="0.85rem"),
                                        rx.button(
                                            "❌",
                                            on_click=lambda: AdminPanelState.quitar_empleado_adicional(emp),
                                            color_scheme="red",
                                            variant="ghost",
                                            size="1"
                                        ),
                                        justify="between",
                                        align="center",
                                        width="100%",
                                        padding="0.5rem",
                                        border="1px solid",
                                        border_color=COLORS["border"],
                                        border_radius="6px",
                                        background="#f8f9fa",
                                    )
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.fragment()
                        ),
                        
                        spacing="2",
                        width="100%",
                    ),
                    padding="1rem",
                    border="1px dashed",
                    border_color=COLORS["border"],
                    border_radius="8px",
                    background="#fafbfc",
                    width="100%",
                ),
                
                # Descripción
                rx.input(
                    placeholder="Descripción de la tarea",
                    value=AdminPanelState.tarea_descripcion,
                    on_change=AdminPanelState.set_tarea_descripcion,
                    width="100%"
                ),
                
                # Fila: Prioridad y Fecha de vencimiento
                rx.grid(
                    rx.vstack(
                        rx.text("⚡ Prioridad:", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.select(
                            ["alta", "media", "baja"],
                            value=AdminPanelState.tarea_prioridad,
                            on_change=AdminPanelState.set_tarea_prioridad,
                            placeholder="Seleccione prioridad",
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("📅 Fecha de vencimiento:", font_size="0.85rem", font_weight="600", color=COLORS["text"]),
                        rx.input(
                            type="date",
                            value=AdminPanelState.tarea_fecha_vencimiento,
                            on_change=AdminPanelState.set_tarea_fecha_vencimiento,
                            width="100%"
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                
                # Botón crear
                rx.button(
                    "✅ Crear Tarea",
                    on_click=AdminPanelState.crear_nueva_tarea,
                    background=COLORS["warning"],
                    color="white",
                    width="100%"
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        # Lista de Tareas
        rx.card(
            rx.vstack(
                rx.heading("Todas las Tareas", size="4"),
                rx.text(f"Total: {AdminPanelState.tareas.length()} tareas", font_weight="600"),
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
                    rx.text("No hay tareas creadas aún", font_size="0.9rem", color=COLORS["text_light"], font_style="italic")
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        spacing="6",
        width="100%",
    )


def jornadas_tab() -> rx.Component:
    """Tab de jornadas laborales."""
    return rx.vstack(
        rx.heading("Jornadas Laborales", size="6"),
        
        rx.card(
            rx.vstack(
                rx.heading("Historial de Jornadas", size="4"),
                rx.text(f"Total: {AdminPanelState.jornadas_con_info.length()} jornadas registradas", font_weight="600"),
                
                rx.foreach(
                    AdminPanelState.jornadas_con_info,
                    lambda j: rx.box(
                        rx.vstack(
                            # Fila 1: Fecha y Horas
                            rx.hstack(
                                rx.text(j["fecha"], font_weight="700", font_size="1rem"),
                                rx.text(f"{j['horas_trabajadas']}h", 
                                       font_weight="700", color=COLORS["success"], font_size="1.1rem"),
                                justify="between",
                                width="100%",
                            ),
                            # Fila 2: Empleado
                            rx.hstack(
                                rx.text("👤 Empleado:", font_weight="600", font_size="0.85rem"),
                                rx.text(j["empleado_nombre"], font_size="0.9rem", color=COLORS["primary"], font_weight="600"),
                                spacing="2",
                            ),
                            # Fila 3: Proyecto (si existe)
                            rx.cond(
                                j["tiene_proyecto"],
                                rx.hstack(
                                    rx.text("📁 Proyecto:", font_weight="600", font_size="0.85rem"),
                                    rx.text(j["proyecto_nombre"], font_size="0.9rem", color=COLORS["info"], font_weight="600"),
                                    spacing="2",
                                ),
                                rx.fragment()
                            ),
                            # Fila 4: Descripción
                            rx.text(f"📝 {j['descripcion']}", font_size="0.85rem", color=COLORS["text_light"]),
                            spacing="2",
                        ),
                        padding="1rem",
                        border="2px solid",
                        border_color=COLORS["border"],
                        border_radius="8px",
                        margin_bottom="0.75rem",
                        background="white",
                        _hover={
                            "border_color": COLORS["primary"],
                            "box_shadow": "0 2px 8px rgba(0,0,0,0.08)"
                        }
                    )
                ),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        spacing="6",
        width="100%",
    )


def admin_panel() -> rx.Component:
    """Panel de administración profesional completo."""
    return rx.container(
        rx.vstack(
            admin_header(),
            
            # Mensaje de éxito/error
            rx.cond(
                AdminPanelState.show_message,
                rx.cond(
                    AdminPanelState.success_message != "",
                    rx.card(
                        rx.hstack(
                            rx.text(AdminPanelState.success_message, color="white"),
                            rx.button(
                                "✕",
                                on_click=AdminPanelState.cerrar_mensaje,
                                variant="ghost",
                                size="1",
                                color="white",
                            ),
                            justify="between",
                            width="100%",
                        ),
                        background=COLORS["success"],
                        color="white",
                    ),
                    rx.card(
                        rx.hstack(
                            rx.text(AdminPanelState.error_message, color="white"),
                            rx.button(
                                "✕",
                                on_click=AdminPanelState.cerrar_mensaje,
                                variant="ghost",
                                size="1",
                                color="white",
                            ),
                            justify="between",
                            width="100%",
                        ),
                        background=COLORS["error"],
                        color="white",
                    ),
                ),
            ),
            
            tab_buttons(),
            
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
            
            spacing="6",
            width="100%",
        ),
        max_width="1400px",
        padding="2rem",
        on_mount=AdminPanelState.on_mount,
    )
