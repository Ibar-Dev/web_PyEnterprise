"""
Panel de Administración Completo con integración Supabase
Gestión completa de proyectos, empleados y tareas
"""

import reflex as rx
from datetime import datetime
from typing import List, Dict, Any
from ..styles import *
from ..database import (
    obtener_todos_proyectos,
    obtener_todos_empleados,
    crear_proyecto,
    crear_empleado,
    crear_tarea,
    asignar_empleado_proyecto,
    obtener_tareas_proyecto,
    actualizar_estado_tarea,
    eliminar_proyecto,
    eliminar_empleado,
    obtener_estadisticas_sistema,
)


class AdminDashboardState(rx.State):
    """Estado del panel de administración."""

    # Datos cargados desde Supabase
    proyectos: List[Dict[str, Any]] = []
    empleados: List[Dict[str, Any]] = []
    estadisticas: Dict[str, Any] = {}

    # Estado de carga
    is_loading: bool = False

    # Pestaña activa
    active_tab: str = "overview"

    # Formulario: Nuevo Proyecto
    proyecto_nombre: str = ""
    proyecto_descripcion: str = ""
    proyecto_cliente: str = ""
    proyecto_fecha_inicio: str = ""
    proyecto_presupuesto_horas: str = "0"

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
    tarea_horas_estimadas: str = "0"

    # Mensajes
    success_message: str = ""
    error_message: str = ""
    show_message: bool = False

    async def on_mount(self):
        """Cargar datos al montar."""
        await self.cargar_datos()

    async def cargar_datos(self):
        """Cargar proyectos, empleados y estadísticas."""
        self.is_loading = True

        # Cargar proyectos
        proyectos_data = obtener_todos_proyectos()
        self.proyectos = proyectos_data if proyectos_data else []

        # Cargar empleados
        empleados_data = obtener_todos_empleados()
        self.empleados = empleados_data if empleados_data else []

        # Cargar estadísticas del sistema
        self.estadisticas = obtener_estadisticas_sistema() if obtener_estadisticas_sistema() else {
            "total_proyectos": len(self.proyectos),
            "total_empleados": len(self.empleados),
            "total_tareas": 0,
            "horas_totales": 0.0
        }

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

    def set_proyecto_presupuesto_horas(self, valor: str):
        self.proyecto_presupuesto_horas = valor

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

    def set_tarea_titulo(self, valor: str):
        self.tarea_titulo = valor

    def set_tarea_descripcion(self, valor: str):
        self.tarea_descripcion = valor

    def set_tarea_prioridad(self, valor: str):
        self.tarea_prioridad = valor

    def set_tarea_fecha_vencimiento(self, valor: str):
        self.tarea_fecha_vencimiento = valor

    def set_tarea_horas_estimadas(self, valor: str):
        self.tarea_horas_estimadas = valor

    def crear_nuevo_proyecto(self):
        """Crear proyecto en Supabase."""
        if not self.proyecto_nombre or not self.proyecto_cliente:
            self.error_message = "Nombre y cliente son obligatorios"
            self.show_message = True
            return

        resultado = crear_proyecto(
            nombre=self.proyecto_nombre,
            descripcion=self.proyecto_descripcion,
            cliente=self.proyecto_cliente,
            fecha_inicio=self.proyecto_fecha_inicio or datetime.now().strftime('%Y-%m-%d'),
            presupuesto_horas=int(self.proyecto_presupuesto_horas) if self.proyecto_presupuesto_horas else 0
        )

        if resultado:
            self.success_message = f"✅ Proyecto '{self.proyecto_nombre}' creado"
            self.show_message = True
            # Limpiar formulario
            self.proyecto_nombre = ""
            self.proyecto_descripcion = ""
            self.proyecto_cliente = ""
            self.proyecto_fecha_inicio = ""
            self.proyecto_presupuesto_horas = "0"
            # Recargar datos
            self.cargar_datos()
        else:
            self.error_message = "❌ Error al crear proyecto"
            self.show_message = True

    def crear_nuevo_empleado(self):
        """Crear empleado en Supabase."""
        if not self.empleado_email or not self.empleado_password or not self.empleado_nombre:
            self.error_message = "Email, contraseña y nombre son obligatorios"
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
            self.success_message = f"✅ Empleado '{self.empleado_nombre}' creado"
            self.show_message = True
            # Limpiar formulario
            self.empleado_email = ""
            self.empleado_password = ""
            self.empleado_nombre = ""
            self.empleado_apellidos = ""
            self.empleado_rol = "desarrollador"
            # Recargar datos
            self.cargar_datos()
        else:
            self.error_message = "❌ Error al crear empleado"
            self.show_message = True

    def crear_nueva_tarea(self):
        """Crear tarea en Supabase."""
        if not self.tarea_proyecto_id or not self.tarea_empleado_id or not self.tarea_titulo:
            self.error_message = "Proyecto, empleado y título son obligatorios"
            self.show_message = True
            return

        resultado = crear_tarea(
            proyecto_id=self.tarea_proyecto_id,
            empleado_asignado_id=self.tarea_empleado_id,
            titulo=self.tarea_titulo,
            descripcion=self.tarea_descripcion,
            prioridad=self.tarea_prioridad,
            fecha_vencimiento=self.tarea_fecha_vencimiento,
            horas_estimadas=float(self.tarea_horas_estimadas) if self.tarea_horas_estimadas else 0.0
        )

        if resultado:
            self.success_message = f"✅ Tarea '{self.tarea_titulo}' creada"
            self.show_message = True
            # Limpiar formulario
            self.tarea_titulo = ""
            self.tarea_descripcion = ""
            self.tarea_fecha_vencimiento = ""
            self.tarea_horas_estimadas = "0"
        else:
            self.error_message = "❌ Error al crear tarea"
            self.show_message = True

    def eliminar_proyecto_admin(self, proyecto_id: str):
        """Eliminar proyecto."""
        resultado = eliminar_proyecto(proyecto_id)
        if resultado:
            self.success_message = "✅ Proyecto eliminado"
            self.show_message = True
            self.cargar_datos()
        else:
            self.error_message = "❌ Error al eliminar proyecto"
            self.show_message = True

    def eliminar_empleado_admin(self, empleado_id: str):
        """Eliminar empleado."""
        resultado = eliminar_empleado(empleado_id)
        if resultado:
            self.success_message = "✅ Empleado eliminado"
            self.show_message = True
            self.cargar_datos()
        else:
            self.error_message = "❌ Error al eliminar empleado"
            self.show_message = True

    def asignar_empleado_a_proyecto(self, empleado_id: str, proyecto_id: str):
        """Asignar empleado a proyecto."""
        resultado = asignar_empleado_proyecto(empleado_id, proyecto_id)
        if resultado:
            self.success_message = "✅ Empleado asignado al proyecto"
            self.show_message = True
            self.cargar_datos()
        else:
            self.error_message = "❌ Error al asignar empleado"
            self.show_message = True

    def cerrar_mensaje(self):
        """Cerrar mensaje."""
        self.show_message = False
        self.success_message = ""
        self.error_message = ""


def admin_header() -> rx.Component:
    """Header del panel de admin."""
    return rx.hstack(
        rx.heading("🔧 Panel de Administración", size="8"),
        rx.button(
            "Cerrar Sesión",
            on_click=lambda: rx.redirect("/empleados"),
            variant="outline",
            color_scheme="red",
        ),
        justify="between",
        align="center",
        width="100%",
        padding="2rem 0",
    )


def tab_buttons() -> rx.Component:
    """Botones de navegación entre tabs."""
    return rx.hstack(
        rx.button(
            "📊 Resumen",
            on_click=lambda: AdminDashboardState.cambiar_tab("overview"),
            variant=rx.cond(AdminDashboardState.active_tab == "overview", "solid", "outline"),
        ),
        rx.button(
            "📁 Proyectos",
            on_click=lambda: AdminDashboardState.cambiar_tab("proyectos"),
            variant=rx.cond(AdminDashboardState.active_tab == "proyectos", "solid", "outline"),
        ),
        rx.button(
            "👥 Empleados",
            on_click=lambda: AdminDashboardState.cambiar_tab("empleados"),
            variant=rx.cond(AdminDashboardState.active_tab == "empleados", "solid", "outline"),
        ),
        rx.button(
            "✅ Tareas",
            on_click=lambda: AdminDashboardState.cambiar_tab("tareas"),
            variant=rx.cond(AdminDashboardState.active_tab == "tareas", "solid", "outline"),
        ),
        spacing="3",
        width="100%",
    )


def overview_tab() -> rx.Component:
    """Tab de resumen general."""
    return rx.vstack(
        rx.heading("Resumen del Sistema", size="6"),

        rx.grid(
            # Card: Total Proyectos
            rx.card(
                rx.vstack(
                    rx.text("📁 Total Proyectos", font_weight="600"),
                    rx.text(
                        AdminDashboardState.estadisticas.get("total_proyectos", 0),
                        font_size="2rem",
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
                    rx.text("👥 Total Empleados", font_weight="600"),
                    rx.text(
                        AdminDashboardState.estadisticas.get("total_empleados", 0),
                        font_size="2rem",
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
                    rx.text("✅ Total Tareas", font_weight="600"),
                    rx.text(
                        AdminDashboardState.estadisticas.get("total_tareas", 0),
                        font_size="2rem",
                        font_weight="bold",
                        color=COLORS["warning"]
                    ),
                    spacing="2",
                ),
                size="3",
            ),

            # Card: Horas Totales
            rx.card(
                rx.vstack(
                    rx.text("⏰ Horas Trabajadas", font_weight="600"),
                    rx.text(
                        f"{AdminDashboardState.estadisticas.get('horas_totales', 0):.1f}h",
                        font_size="2rem",
                        font_weight="bold",
                        color=COLORS["info"]
                    ),
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

                rx.input(
                    placeholder="Nombre del proyecto",
                    value=AdminDashboardState.proyecto_nombre,
                    on_change=AdminDashboardState.set_proyecto_nombre,
                ),

                rx.input(
                    placeholder="Cliente",
                    value=AdminDashboardState.proyecto_cliente,
                    on_change=AdminDashboardState.set_proyecto_cliente,
                ),

                rx.input(
                    placeholder="Descripción",
                    value=AdminDashboardState.proyecto_descripcion,
                    on_change=AdminDashboardState.set_proyecto_descripcion,
                ),

                rx.input(
                    placeholder="Fecha de inicio (YYYY-MM-DD)",
                    value=AdminDashboardState.proyecto_fecha_inicio,
                    on_change=AdminDashboardState.set_proyecto_fecha_inicio,
                ),

                rx.input(
                    placeholder="Presupuesto de horas",
                    type="number",
                    value=AdminDashboardState.proyecto_presupuesto_horas,
                    on_change=AdminDashboardState.set_proyecto_presupuesto_horas,
                ),

                rx.button(
                    "Crear Proyecto",
                    on_click=AdminDashboardState.crear_nuevo_proyecto,
                    background=COLORS["primary"],
                    color="white",
                    width="100%",
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

                rx.cond(
                    AdminDashboardState.is_loading,
                    rx.spinner(),
                    rx.cond(
                        AdminDashboardState.proyectos.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                AdminDashboardState.proyectos,
                                lambda p: rx.hstack(
                                    rx.vstack(
                                        rx.text(p["nombre"], font_weight="600"),
                                        rx.text(f"Cliente: {p.get('cliente', 'N/A')}", font_size="0.9rem"),
                                        rx.text(f"Estado: {p.get('estado', 'Activo')}", font_size="0.9rem"),
                                        spacing="1",
                                    ),
                                    rx.button(
                                        "🗑️",
                                        on_click=lambda: AdminDashboardState.eliminar_proyecto_admin(p["id"]),
                                        color_scheme="red",
                                        variant="outline",
                                        size="2",
                                    ),
                                    justify="between",
                                    align="center",
                                    width="100%",
                                    padding="1rem",
                                    border="1px solid",
                                    border_color=COLORS["border"],
                                    border_radius="8px",
                                )
                            ),
                            spacing="2",
                        ),
                        rx.text("No hay proyectos creados", color=COLORS["text_light"])
                    )
                ),

                spacing="4",
                width="100%",
            ),
            size="3",
        ),

        spacing="6",
        width="100%",
    )


def empleados_tab() -> rx.Component:
    """Tab de gestión de empleados."""
    return rx.vstack(
        rx.heading("Gestión de Empleados", size="6"),

        # Formulario: Nuevo Empleado
        rx.card(
            rx.vstack(
                rx.heading("Crear Nuevo Empleado", size="4"),

                rx.input(
                    placeholder="Email",
                    value=AdminDashboardState.empleado_email,
                    on_change=AdminDashboardState.set_empleado_email,
                ),

                rx.input(
                    placeholder="Contraseña",
                    type="password",
                    value=AdminDashboardState.empleado_password,
                    on_change=AdminDashboardState.set_empleado_password,
                ),

                rx.input(
                    placeholder="Nombre",
                    value=AdminDashboardState.empleado_nombre,
                    on_change=AdminDashboardState.set_empleado_nombre,
                ),

                rx.input(
                    placeholder="Apellidos",
                    value=AdminDashboardState.empleado_apellidos,
                    on_change=AdminDashboardState.set_empleado_apellidos,
                ),

                rx.select(
                    ["desarrollador", "diseñador", "admin", "gerente"],
                    value=AdminDashboardState.empleado_rol,
                    on_change=AdminDashboardState.set_empleado_rol,
                ),

                rx.button(
                    "Crear Empleado",
                    on_click=AdminDashboardState.crear_nuevo_empleado,
                    background=COLORS["success"],
                    color="white",
                    width="100%",
                ),

                spacing="3",
                width="100%",
            ),
            size="3",
        ),

        # Lista de Empleados
        rx.card(
            rx.vstack(
                rx.heading("Empleados Registrados", size="4"),

                rx.cond(
                    AdminDashboardState.is_loading,
                    rx.spinner(),
                    rx.cond(
                        AdminDashboardState.empleados.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                AdminDashboardState.empleados,
                                lambda e: rx.hstack(
                                    rx.vstack(
                                        rx.text(e["nombre"], font_weight="600"),
                                        rx.text(f"Email: {e['email']}", font_size="0.9rem"),
                                        rx.text(f"Rol: {e['rol']}", font_size="0.9rem"),
                                        spacing="1",
                                    ),
                                    rx.button(
                                        "🗑️",
                                        on_click=lambda: AdminDashboardState.eliminar_empleado_admin(e["id"]),
                                        color_scheme="red",
                                        variant="outline",
                                        size="2",
                                    ),
                                    justify="between",
                                    align="center",
                                    width="100%",
                                    padding="1rem",
                                    border="1px solid",
                                    border_color=COLORS["border"],
                                    border_radius="8px",
                                )
                            ),
                            spacing="2",
                        ),
                        rx.text("No hay empleados registrados", color=COLORS["text_light"])
                    )
                ),

                spacing="4",
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

                rx.input(
                    placeholder="ID del proyecto",
                    value=AdminDashboardState.tarea_proyecto_id,
                    on_change=AdminDashboardState.set_tarea_proyecto_id,
                ),

                rx.input(
                    placeholder="ID del empleado",
                    value=AdminDashboardState.tarea_empleado_id,
                    on_change=AdminDashboardState.set_tarea_empleado_id,
                ),

                rx.input(
                    placeholder="Título de la tarea",
                    value=AdminDashboardState.tarea_titulo,
                    on_change=AdminDashboardState.set_tarea_titulo,
                ),

                rx.input(
                    placeholder="Descripción",
                    value=AdminDashboardState.tarea_descripcion,
                    on_change=AdminDashboardState.set_tarea_descripcion,
                ),

                rx.select(
                    ["alta", "media", "baja"],
                    placeholder="Prioridad",
                    value=AdminDashboardState.tarea_prioridad,
                    on_change=AdminDashboardState.set_tarea_prioridad,
                ),

                rx.input(
                    placeholder="Fecha de vencimiento (YYYY-MM-DD)",
                    value=AdminDashboardState.tarea_fecha_vencimiento,
                    on_change=AdminDashboardState.set_tarea_fecha_vencimiento,
                ),

                rx.input(
                    placeholder="Horas estimadas",
                    type="number",
                    value=AdminDashboardState.tarea_horas_estimadas,
                    on_change=AdminDashboardState.set_tarea_horas_estimadas,
                ),

                rx.button(
                    "Crear Tarea",
                    on_click=AdminDashboardState.crear_nueva_tarea,
                    background=COLORS["warning"],
                    color="white",
                    width="100%",
                ),

                spacing="3",
                width="100%",
            ),
            size="3",
        ),

        # Lista de Tareas por Proyecto
        rx.card(
            rx.vstack(
                rx.heading("Tareas por Proyecto", size="4"),

                rx.cond(
                    AdminDashboardState.is_loading,
                    rx.spinner(),
                    rx.text("Selecciona un proyecto para ver sus tareas")
                ),

                spacing="4",
                width="100%",
            ),
            size="3",
        ),

        spacing="6",
        width="100%",
    )


def admin_dashboard() -> rx.Component:
    """Panel de administración completo."""
    return rx.container(
        rx.vstack(
            admin_header(),

            # Mensaje de éxito/error
            rx.cond(
                AdminDashboardState.show_message,
                rx.cond(
                    AdminDashboardState.success_message != "",
                    rx.card(
                        rx.hstack(
                            rx.text(AdminDashboardState.success_message),
                            rx.button(
                                "✕",
                                on_click=AdminDashboardState.cerrar_mensaje,
                                variant="ghost",
                                size="1",
                            ),
                            justify="between",
                            width="100%",
                        ),
                        background="green",
                        color="white",
                    ),
                    rx.card(
                        rx.hstack(
                            rx.text(AdminDashboardState.error_message),
                            rx.button(
                                "✕",
                                on_click=AdminDashboardState.cerrar_mensaje,
                                variant="ghost",
                                size="1",
                            ),
                            justify="between",
                            width="100%",
                        ),
                        background="red",
                        color="white",
                    ),
                ),
            ),

            tab_buttons(),

            # Contenido según tab activa
            rx.cond(
                AdminDashboardState.active_tab == "overview",
                overview_tab(),
                rx.cond(
                    AdminDashboardState.active_tab == "proyectos",
                    proyectos_tab(),
                    rx.cond(
                        AdminDashboardState.active_tab == "empleados",
                        empleados_tab(),
                        rx.cond(
                            AdminDashboardState.active_tab == "tareas",
                            tareas_tab(),
                            rx.text("Tab no encontrado")
                        )
                    )
                )
            ),

            spacing="6",
            width="100%",
        ),
        max_width="1200px",
        padding="2rem",
        on_mount=AdminDashboardState.on_mount,
    )
