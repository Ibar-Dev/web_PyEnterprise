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
    tarea_proyecto_id: str = ""
    tarea_empleado_id: str = ""
    tarea_titulo: str = ""
    tarea_descripcion: str = ""
    tarea_prioridad: str = "media"
    tarea_fecha_vencimiento: str = ""
    
    # Mensajes
    success_message: str = ""
    error_message: str = ""
    show_message: bool = False
    
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
    
    async def crear_nuevo_proyecto(self):
        """Crear proyecto en Supabase."""
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
            self.success_message = f"✅ Tarea '{self.tarea_titulo}' creada exitosamente"
            self.show_message = True
            # Limpiar formulario
            self.tarea_titulo = ""
            self.tarea_descripcion = ""
            self.tarea_fecha_vencimiento = ""
            # Recargar datos
            await self.cargar_todos_datos()
        else:
            self.error_message = "❌ Error al crear tarea. Verifique el formato de la fecha (AAAA-MM-DD) y los IDs"
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
        
        # Formulario: Nuevo Proyecto
        rx.card(
            rx.vstack(
                rx.heading("Crear Nuevo Proyecto", size="4"),
                rx.grid(
                    rx.input(placeholder="Nombre del proyecto", value=AdminPanelState.proyecto_nombre, on_change=AdminPanelState.set_proyecto_nombre),
                    rx.input(placeholder="Cliente", value=AdminPanelState.proyecto_cliente, on_change=AdminPanelState.set_proyecto_cliente),
                    rx.input(placeholder="Fecha de inicio (AAAA-MM-DD)", value=AdminPanelState.proyecto_fecha_inicio, on_change=AdminPanelState.set_proyecto_fecha_inicio),
                    rx.input(placeholder="Presupuesto (€)", type="number", value=AdminPanelState.proyecto_presupuesto, on_change=AdminPanelState.set_proyecto_presupuesto),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.input(placeholder="Descripción", value=AdminPanelState.proyecto_descripcion, on_change=AdminPanelState.set_proyecto_descripcion),
                rx.button("Crear Proyecto", on_click=AdminPanelState.crear_nuevo_proyecto, background=COLORS["primary"], color="white", width="100%"),
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
                            rx.button("🗑️", on_click=lambda: AdminPanelState.eliminar_proyecto_admin(p["id"]), color_scheme="red", variant="outline", size="2"),
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


def tareas_tab() -> rx.Component:
    """Tab de gestión de tareas."""
    return rx.vstack(
        rx.heading("Gestión de Tareas", size="6"),
        
        # Formulario: Nueva Tarea
        rx.card(
            rx.vstack(
                rx.heading("Crear Nueva Tarea", size="4"),
                rx.text("Seleccione proyecto y empleado:", font_size="0.9rem", color=COLORS["text_light"]),
                rx.text("💡 Copie los IDs de las listas de abajo:", font_size="0.85rem", color=COLORS["text_light"], font_style="italic"),
                rx.grid(
                    rx.vstack(
                        rx.text("Proyecto (ID):", font_weight="600", font_size="0.85rem"),
                        rx.input(
                            placeholder="ID del proyecto",
                            value=AdminPanelState.tarea_proyecto_id,
                            on_change=AdminPanelState.set_tarea_proyecto_id
                        ),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Empleado (ID):", font_weight="600", font_size="0.85rem"),
                        rx.input(
                            placeholder="ID del empleado",
                            value=AdminPanelState.tarea_empleado_id,
                            on_change=AdminPanelState.set_tarea_empleado_id
                        ),
                        spacing="1",
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.input(placeholder="Título de la tarea", value=AdminPanelState.tarea_titulo, on_change=AdminPanelState.set_tarea_titulo),
                rx.input(placeholder="Descripción de la tarea", value=AdminPanelState.tarea_descripcion, on_change=AdminPanelState.set_tarea_descripcion),
                rx.grid(
                    rx.select(["alta", "media", "baja"], value=AdminPanelState.tarea_prioridad, on_change=AdminPanelState.set_tarea_prioridad, placeholder="Prioridad"),
                    rx.input(placeholder="Fecha vencimiento (AAAA-MM-DD)", value=AdminPanelState.tarea_fecha_vencimiento, on_change=AdminPanelState.set_tarea_fecha_vencimiento),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.text("Formato de fecha: AAAA-MM-DD (ejemplo: 2024-12-31)", font_size="0.75rem", color=COLORS["text_light"]),
                rx.button("Crear Tarea", on_click=AdminPanelState.crear_nueva_tarea, background=COLORS["warning"], color="white", width="100%"),
                spacing="3",
                width="100%",
            ),
            size="3",
        ),
        
        # Listas de referencia para copiar IDs
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("📁 Proyectos Disponibles", size="4"),
                    rx.text("Copie el ID del proyecto:", font_size="0.85rem", color=COLORS["text_light"]),
                    rx.foreach(
                        AdminPanelState.proyectos,
                        lambda p: rx.box(
                            rx.vstack(
                                rx.text(f"{p['nombre']} - {p['cliente']}", font_weight="600", font_size="0.9rem"),
                                rx.text(f"ID: {p['id']}", font_size="0.75rem", color=COLORS["primary"], font_family="monospace"),
                                spacing="0",
                            ),
                            padding="0.5rem",
                            border="1px solid",
                            border_color=COLORS["border"],
                            border_radius="4px",
                            margin_bottom="0.25rem",
                        )
                    ),
                    spacing="2",
                    width="100%",
                ),
                size="3",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("👥 Empleados Disponibles", size="4"),
                    rx.text("Copie el ID del empleado:", font_size="0.85rem", color=COLORS["text_light"]),
                    rx.foreach(
                        AdminPanelState.empleados,
                        lambda e: rx.box(
                            rx.vstack(
                                rx.text(f"{e['nombre']} {e['apellidos']} ({e['rol']})", font_weight="600", font_size="0.9rem"),
                                rx.text(f"ID: {e['id']}", font_size="0.75rem", color=COLORS["success"], font_family="monospace"),
                                spacing="0",
                            ),
                            padding="0.5rem",
                            border="1px solid",
                            border_color=COLORS["border"],
                            border_radius="4px",
                            margin_bottom="0.25rem",
                        )
                    ),
                    spacing="2",
                    width="100%",
                ),
                size="3",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        
        # Lista de Tareas
        rx.card(
            rx.vstack(
                rx.heading("Todas las Tareas", size="4"),
                rx.text(f"Total: {AdminPanelState.tareas.length()} tareas", font_weight="600"),
                rx.foreach(
                    AdminPanelState.tareas,
                    lambda t: rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text(t["titulo"], font_weight="600", font_size="1.1rem"),
                                rx.hstack(
                                    rx.text(f"Estado: {t['estado']}", font_size="0.85rem"),
                                    rx.text(f"Prioridad: {t['prioridad']}", 
                                           font_size="0.85rem", 
                                           color=COLORS["warning"]),
                                    rx.text(f"Vence: {t['fecha_vencimiento']}", font_size="0.85rem"),
                                    spacing="4",
                                ),
                                spacing="1",
                            ),
                            rx.button("🗑️", on_click=lambda: AdminPanelState.eliminar_tarea_admin(t["id"]), color_scheme="red", variant="outline", size="2"),
                            justify="between",
                            align="center",
                            width="100%",
                        ),
                        padding="0.75rem",
                        border="1px solid",
                        border_color=COLORS["border"],
                        border_radius="6px",
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


def jornadas_tab() -> rx.Component:
    """Tab de jornadas laborales."""
    return rx.vstack(
        rx.heading("Jornadas Laborales", size="6"),
        
        rx.card(
            rx.vstack(
                rx.heading("Historial de Jornadas", size="4"),
                rx.text(f"Total: {AdminPanelState.jornadas.length()} jornadas registradas", font_weight="600"),
                
                rx.foreach(
                    AdminPanelState.jornadas,
                    lambda j: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(j["fecha"], font_weight="600"),
                                rx.text(f"{j['horas_trabajadas']}h", 
                                       font_weight="600", color=COLORS["success"]),
                                justify="between",
                                width="100%",
                            ),
                            rx.text(f"Descripción: {j['descripcion']}", font_size="0.85rem"),
                            spacing="1",
                        ),
                        padding="0.75rem",
                        border="1px solid",
                        border_color=COLORS["border"],
                        border_radius="6px",
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
