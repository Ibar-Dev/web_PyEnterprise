"""
Dashboard integrado con autenticación para empleados PyLink
"""

import reflex as rx
from datetime import datetime, timedelta
from ..styles import *
from ..database import (
    obtener_proyectos_empleado,
    obtener_tareas_empleado,
    registrar_jornada,
    obtener_jornadas_empleado,
    calcular_horas_totales_empleado,
    actualizar_estado_tarea
)
from .employee_auth import EmployeeAuthState


class EmployeeDashboardState(rx.State):
    """Estado del dashboard de empleados."""

    # Estado de sesión de trabajo
    is_working: bool = False
    current_session: dict = {}
    work_description: str = ""

    # Datos cargados de la base de datos (simplificado)
    proyectos: list[dict] = []
    tareas: list[dict] = []
    jornadas: list[dict] = []
    horas_hoy: float = 0.0
    horas_semana: float = 0.0

    # Estado de carga
    is_loading: bool = False

    # Información del empleado
    empleado_id: str = ""
    empleado_nombre: str = ""

    async def on_mount(self):
        """Cargar datos al montar el componente."""
        await self.cargar_datos_desde_auth()

    async def cargar_datos_desde_auth(self):
        """Cargar datos usando información de autenticación."""
        self.is_loading = True

        try:
            # Obtener el estado de autenticación usando el estado padre
            from .employee_auth import EmployeeAuthState
            auth_state = await self.get_state(EmployeeAuthState)

            if auth_state and auth_state.employee_id:
                empleado_id = auth_state.employee_id
                empleado_nombre = auth_state.employee_name

                print(f"✅ Cargando datos para empleado: {empleado_nombre} ({empleado_id})")

                self.empleado_id = empleado_id
                self.empleado_nombre = empleado_nombre

                # Cargar proyectos del empleado
                proyectos_data = obtener_proyectos_empleado(empleado_id)
                self.proyectos = proyectos_data if proyectos_data else []

                # Cargar tareas del empleado
                tareas_data = obtener_tareas_empleado(empleado_id)
                self.tareas = tareas_data if tareas_data else []

                # Cargar jornadas recientes
                jornadas_data = obtener_jornadas_empleado(empleado_id)
                self.jornadas = jornadas_data if jornadas_data else []

                # Calcular horas trabajadas
                fecha_hoy = datetime.now().date()
                fecha_lunes = fecha_hoy - timedelta(days=fecha_hoy.weekday())

                self.horas_hoy = calcular_horas_totales_empleado(
                    empleado_id,
                    fecha_hoy.strftime('%Y-%m-%d'),
                    fecha_hoy.strftime('%Y-%m-%d')
                )

                self.horas_semana = calcular_horas_totales_empleado(
                    empleado_id,
                    fecha_lunes.strftime('%Y-%m-%d'),
                    fecha_hoy.strftime('%Y-%m-%d')
                )

                print(f"✅ Datos cargados: {len(self.proyectos)} proyectos, {len(self.tareas)} tareas")

            else:
                print("❌ No se pudo obtener información de autenticación")

        except Exception as e:
            print(f"❌ Error cargando datos del dashboard: {e}")
            import traceback
            traceback.print_exc()

        self.is_loading = False

    def start_work_session(self, proyecto_id: str = ""):
        """Iniciar sesión de trabajo."""
        if not self.is_working:
            # Si hay proyectos, usar el primero; si no, permitir jornada sin proyecto
            proyecto_para_usar = None
            if proyecto_id:
                proyecto_para_usar = proyecto_id
            elif len(self.proyectos) > 0:
                proyecto_para_usar = self.proyectos[0]["id"]
            
            self.current_session = {
                "proyecto_id": proyecto_para_usar,
                "start_time": datetime.now().isoformat(),
                "description": ""
            }
            self.is_working = True
            if proyecto_para_usar:
                print(f"✅ Jornada iniciada en proyecto: {proyecto_para_usar}")
            else:
                print("✅ Jornada iniciada (sin proyecto asignado)")

    async def end_work_session(self):
        """Finalizar sesión de trabajo."""
        if self.is_working and self.current_session:
            start_time = datetime.fromisoformat(self.current_session["start_time"])
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 3600  # horas

            # Usar el empleado_id ya cargado en el estado
            empleado_id = self.empleado_id
            proyecto_id = self.current_session.get("proyecto_id")  # Puede ser None

            # Validar que tengamos empleado_id (proyecto_id es opcional)
            if empleado_id:
                jornada_data = registrar_jornada(
                    empleado_id=empleado_id,
                    proyecto_id=proyecto_id,  # Puede ser None ahora
                    fecha=end_time.strftime('%Y-%m-%d'),
                    hora_inicio=start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    hora_fin=end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    descripcion=self.work_description or "Jornada de trabajo"
                )

                if jornada_data:
                    # Recargar datos después de registrar
                    await self.cargar_datos_desde_auth()
                    self.horas_hoy += duration
                    print(f"✅ Jornada registrada: {duration:.2f} horas")
                else:
                    print("❌ Error al registrar jornada")
            else:
                print(f"❌ No se puede registrar jornada: empleado_id no válido")

            # Limpiar sesión
            self.is_working = False
            self.current_session = {}
            self.work_description = ""

    def set_work_description(self, description: str):
        """Actualizar descripción de la sesión de trabajo."""
        self.work_description = description
    
    async def marcar_tarea_completada(self, tarea_id: str):
        """Marcar una tarea como completada."""
        resultado = actualizar_estado_tarea(tarea_id, "completada")
        if resultado:
            print(f"✅ Tarea {tarea_id} marcada como completada")
            # Recargar tareas
            await self.cargar_datos_desde_auth()
        else:
            print(f"❌ Error al marcar tarea como completada")
    
    async def cambiar_estado_tarea(self, tarea_id: str, nuevo_estado: str):
        """Cambiar estado de una tarea."""
        resultado = actualizar_estado_tarea(tarea_id, nuevo_estado)
        if resultado:
            print(f"✅ Tarea {tarea_id} cambiada a '{nuevo_estado}'")
            # Recargar tareas
            await self.cargar_datos_desde_auth()
        else:
            print(f"❌ Error al cambiar estado de tarea")


def time_control_card() -> rx.Component:
    """Tarjeta de control de tiempo - estilo oscuro."""
    return rx.box(
        rx.vstack(
            rx.text("Control de Tiempo", font_size="1.25rem", color="white", font_weight="600"),
            rx.text("Gestión de jornadas laborales", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.vstack(
                    rx.text(f"Horas hoy: {EmployeeDashboardState.horas_hoy:.1f}h",
                           font_weight="700", font_size="1.5rem", color="#10B981"),
                    rx.text(f"Horas semana: {EmployeeDashboardState.horas_semana:.1f}h",
                           font_size="0.9rem", color="rgba(255, 255, 255, 0.7)"),
                    spacing="2",
                )
            ),

            rx.cond(
                ~EmployeeDashboardState.is_working,
                rx.button(
                    "Iniciar Jornada",
                    on_click=lambda: EmployeeDashboardState.start_work_session(""),
                    background="linear-gradient(135deg, #10B981, #059669)",
                    color="white",
                    font_weight="600",
                    width="100%",
                    size="3",
                    border_radius="8px",
                    box_shadow="0 4px 15px rgba(16, 185, 129, 0.3)",
                    _hover={
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 6px 20px rgba(16, 185, 129, 0.4)",
                    },
                    transition="all 0.3s ease",
                ),
                rx.vstack(
                    rx.text("🟢 Sesión Activa", color="#10B981", font_weight="600"),
                    rx.input(
                        placeholder="¿Qué estás haciendo?",
                        value=EmployeeDashboardState.work_description,
                        on_change=EmployeeDashboardState.set_work_description,
                        size="3",
                        background="rgba(255, 255, 255, 0.05)",
                        border="1px solid rgba(16, 185, 129, 0.3)",
                        color="white",
                        _placeholder={"color": "rgba(255, 255, 255, 0.4)"},
                        _focus={"border_color": "#10B981", "box_shadow": "0 0 0 3px rgba(16, 185, 129, 0.1)"},
                    ),
                    rx.button(
                        "Finalizar Jornada",
                        on_click=EmployeeDashboardState.end_work_session,
                        background="rgba(239, 68, 68, 0.2)",
                        border="1px solid rgba(239, 68, 68, 0.4)",
                        color="#EF4444",
                        font_weight="600",
                        width="100%",
                        size="3",
                        _hover={"background": "rgba(239, 68, 68, 0.3)"},
                    ),
                    spacing="3",
                )
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        padding="2rem",
        border_radius="12px",
        background="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(16, 185, 129, 0.2)",
        backdrop_filter="blur(10px)",
    )


def projects_card() -> rx.Component:
    """Tarjeta de proyectos asignados - estilo oscuro."""
    return rx.box(
        rx.vstack(
            rx.text("Mis Proyectos", font_size="1.25rem", color="white", font_weight="600"),
            rx.text("Proyectos donde colaboras", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.vstack(
                    rx.text(f"{EmployeeDashboardState.proyectos.length()} proyectos", 
                           font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),
                    rx.foreach(
                        EmployeeDashboardState.proyectos,
                        lambda p: rx.box(
                            rx.vstack(
                                rx.text(p["nombre"], font_weight="600", font_size="1rem", color="white"),
                                rx.text(f"Cliente: {p['cliente']}", 
                                       font_size="0.85rem", color="rgba(255, 255, 255, 0.6)"),
                                rx.badge(p['estado'], color_scheme="green", size="1"),
                                spacing="1",
                            ),
                            padding="1rem",
                            border="1px solid rgba(94, 234, 212, 0.2)",
                            border_radius="8px",
                            margin_bottom="0.5rem",
                            background="rgba(255, 255, 255, 0.03)",
                            transition="all 0.2s ease",
                            _hover={
                                "border_color": "#5EEAD4",
                                "background": "rgba(255, 255, 255, 0.05)"
                            }
                        )
                    ),
                    spacing="2",
                    width="100%",
                )
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        padding="2rem",
        border_radius="12px",
        background="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(59, 130, 246, 0.2)",
        backdrop_filter="blur(10px)",
    )


def tasks_card() -> rx.Component:
    """Tarjeta de tareas asignadas - estilo oscuro."""
    return rx.box(
        rx.vstack(
            rx.text("Mis Tareas", font_size="1.25rem", color="white", font_weight="600"),
            rx.text("Tareas pendientes y en progreso", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),

            rx.cond(
                EmployeeDashboardState.is_loading,
                rx.spinner(),
                rx.vstack(
                    rx.text(f"{EmployeeDashboardState.tareas.length()} tareas", 
                           font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),
                    rx.foreach(
                        EmployeeDashboardState.tareas,
                        lambda t: rx.box(
                            rx.vstack(
                                # Fila 1: Título con check
                                rx.hstack(
                                    rx.cond(
                                        t["estado"] == "completada",
                                        rx.icon("circle-check", size=20, color="#22c55e"),
                                        rx.icon("circle", size=20, color="#94a3b8")
                                    ),
                                    rx.text(
                                        t["titulo"], 
                                        font_weight="700", 
                                        font_size="1.05rem",
                                        color="white",
                                        text_decoration=rx.cond(t["estado"] == "completada", "line-through", "none"),
                                    ),
                                    spacing="2",
                                    align="center",
                                    width="100%",
                                ),
                                
                                # Fila 2: Prioridad y Estado
                                rx.hstack(
                                    # Prioridad
                                    rx.cond(
                                        t['prioridad'] == "alta",
                                        rx.badge("⚡ Alta", color_scheme="red", variant="soft", font_size="0.8rem"),
                                        rx.cond(
                                            t['prioridad'] == "media",
                                            rx.badge("⚡ Media", color_scheme="orange", variant="soft", font_size="0.8rem"),
                                            rx.badge("⚡ Baja", color_scheme="gray", variant="soft", font_size="0.8rem")
                                        )
                                    ),
                                    # Estado
                                    rx.cond(
                                        t["estado"] == "completada",
                                        rx.badge("✓ Completada", color_scheme="green", variant="soft", font_size="0.8rem"),
                                        rx.cond(
                                            t["estado"] == "en_progreso",
                                            rx.badge("⏳ En Progreso", color_scheme="orange", variant="soft", font_size="0.8rem"),
                                            rx.badge("○ Pendiente", color_scheme="blue", variant="soft", font_size="0.8rem")
                                        )
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                
                                # Fila 3: Fecha
                                rx.text(
                                    f"📅 Vence: {t['fecha_vencimiento']}", 
                                    font_size="0.9rem", 
                                    color="#64748b",
                                    font_weight="500"
                                ),
                                
                                # Fila 4: Botones de acción
                                rx.cond(
                                    t["estado"] == "completada",
                                    # Si está completada: solo botón Reabrir
                                    rx.button(
                                        "↶ Reabrir Tarea",
                                        on_click=lambda: EmployeeDashboardState.cambiar_estado_tarea(t["id"], "pendiente"),
                                        color_scheme="blue",
                                        variant="outline",
                                        size="2",
                                        width="100%"
                                    ),
                                    # Si NO está completada: botones según estado
                                    rx.cond(
                                        t["estado"] == "pendiente",
                                        # Pendiente: Iniciar + Completar
                                        rx.hstack(
                                            rx.button(
                                                "▶ Iniciar",
                                                on_click=lambda: EmployeeDashboardState.cambiar_estado_tarea(t["id"], "en_progreso"),
                                                color_scheme="orange",
                                                variant="outline",
                                                size="2",
                                                width="50%"
                                            ),
                                            rx.button(
                                                "✓ Completar",
                                                on_click=lambda: EmployeeDashboardState.marcar_tarea_completada(t["id"]),
                                                color_scheme="green",
                                                variant="solid",
                                                size="2",
                                                width="50%"
                                            ),
                                            spacing="2",
                                            width="100%",
                                        ),
                                        # En progreso: solo Completar
                                        rx.button(
                                            "✓ Completar",
                                            on_click=lambda: EmployeeDashboardState.marcar_tarea_completada(t["id"]),
                                            color_scheme="green",
                                            variant="solid",
                                            size="2",
                                            width="100%"
                                        )
                                    )
                                ),
                                
                                spacing="3",
                                align="start",
                                width="100%",
                            ),
                            padding="1.25rem",
                            border="1px solid",
                            border_color=rx.cond(
                                t["estado"] == "completada",
                                "rgba(34, 197, 94, 0.3)",
                                "rgba(245, 158, 11, 0.2)"
                            ),
                            border_radius="8px",
                            margin_bottom="0.75rem",
                            background=rx.cond(
                                t["estado"] == "completada",
                                "rgba(34, 197, 94, 0.05)",
                                "rgba(255, 255, 255, 0.03)"
                            ),
                            _hover={
                                "border_color": "#F59E0B",
                                "background": "rgba(255, 255, 255, 0.05)",
                            },
                            transition="all 0.2s ease",
                            width="100%",
                        )
                    ),
                    spacing="2",
                    width="100%",
                )
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        padding="2rem",
        border_radius="12px",
        background="rgba(255, 255, 255, 0.05)",
        border="1px solid rgba(245, 158, 11, 0.2)",
        backdrop_filter="blur(10px)",
    )


def employee_dashboard() -> rx.Component:
    """Dashboard principal para empleados - estilo oscuro."""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text("Dashboard de Empleados", font_size="2.5rem", color="white", font_weight="700", letter_spacing="-0.02em"),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="log_out", size=18),
                            rx.text("Cerrar Sesión", font_weight="600"),
                            spacing="2",
                        ),
                        background="rgba(239, 68, 68, 0.2)",
                        border="1px solid rgba(239, 68, 68, 0.4)",
                        color="#EF4444",
                        size="3",
                        _hover={"background": "rgba(239, 68, 68, 0.3)"},
                    ),
                    href="/empleados",
                ),
                justify="between",
                align="center",
                width="100%",
                margin_bottom="2rem",
            ),

            # Información del empleado
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text("Empleado:", font_weight="500", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),
                        rx.text(EmployeeDashboardState.empleado_nombre, font_size="1.3rem", color="white", font_weight="600"),
                        spacing="1",
                    ),
                    justify="start",
                    align="center",
                    width="100%",
                ),
                padding="1.5rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(94, 234, 212, 0.2)",
                backdrop_filter="blur(10px)",
                margin_bottom="2rem",
            ),

            # Grid de tarjetas principales
            rx.grid(
                time_control_card(),
                projects_card(),
                tasks_card(),
                columns="3",
                spacing="6",
                width="100%",
            ),

            # Historial reciente de jornadas
            rx.box(
                rx.vstack(
                    rx.text("Historial de Jornadas", font_size="1.5rem", color="white", font_weight="600"),
                    rx.text("Últimas jornadas registradas", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),

                    rx.cond(
                        EmployeeDashboardState.is_loading,
                        rx.spinner(),
                        rx.vstack(
                            rx.text(f"{EmployeeDashboardState.jornadas.length()} jornadas", 
                                   font_weight="400", color="rgba(255, 255, 255, 0.6)", font_size="0.875rem"),
                            rx.foreach(
                                EmployeeDashboardState.jornadas,
                                lambda j: rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(j["fecha"], font_weight="600", color="white"),
                                            rx.text(f"{j['horas_trabajadas']}h", 
                                                   font_weight="700", color="#10B981", font_size="1.1rem"),
                                            justify="between",
                                            width="100%",
                                        ),
                                        rx.text(j['descripcion'], 
                                               font_size="0.85rem", color="rgba(255, 255, 255, 0.6)"),
                                        spacing="1",
                                    ),
                                    padding="1rem",
                                    border="1px solid rgba(16, 185, 129, 0.2)",
                                    border_radius="8px",
                                    margin_bottom="0.5rem",
                                    background="rgba(255, 255, 255, 0.03)",
                                    transition="all 0.2s ease",
                                    _hover={
                                        "border_color": "#10B981",
                                        "background": "rgba(255, 255, 255, 0.05)"
                                    }
                                )
                            ),
                            spacing="2",
                            width="100%",
                        )
                    ),

                    spacing="4",
                    align="stretch",
                    width="100%",
                ),
                padding="2rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.05)",
                border="1px solid rgba(16, 185, 129, 0.2)",
                backdrop_filter="blur(10px)",
            ),

            spacing="6",
            width="100%",
            max_width="1400px",
        ),
        
        # Fondo oscuro del landing
        background="""
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)
        """,
        min_height="100vh",
        padding="3rem",
        on_mount=EmployeeDashboardState.on_mount,
    )
