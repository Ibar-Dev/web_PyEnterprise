"""
Sistema de analíticas y reportes para PyEnterprise
"""

import reflex as rx
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class TimeStats:
    """Estadísticas de tiempo trabajado"""
    total_hours: float
    days_worked: int
    average_hours_per_day: float
    overtime_hours: float


@dataclass
class ProjectStats:
    """Estadísticas de proyectos"""
    total_projects: int
    active_projects: int
    completed_projects: int
    total_budget: float
    average_project_value: float


@dataclass
class TaskStats:
    """Estadísticas de tareas"""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completion_rate: float


@dataclass
class EmployeeStats:
    """Estadísticas de empleados"""
    total_employees: int
    active_employees: int
    new_employees_this_month: int
    average_hours_per_employee: float


class AnalyticsService:
    """Servicio de analíticas y reportes"""

    @staticmethod
    def calculate_time_stats(jornadas: List[Dict]) -> TimeStats:
        """Calcular estadísticas de tiempo trabajado"""
        if not jornadas:
            return TimeStats(0, 0, 0, 0)

        total_hours = sum(j.get('total_horas', 0) for j in jornadas)
        unique_days = len(set(j.get('fecha') for j in jornadas))
        avg_hours = total_hours / unique_days if unique_days > 0 else 0

        # Calcular horas extra (más de 8 horas diarias)
        overtime = 0
        daily_hours = {}
        for jornada in jornadas:
            date = jornada.get('fecha')
            hours = jornada.get('total_horas', 0)
            daily_hours[date] = daily_hours.get(date, 0) + hours

        for daily in daily_hours.values():
            if daily > 8:
                overtime += daily - 8

        return TimeStats(
            total_hours=round(total_hours, 2),
            days_worked=unique_days,
            average_hours_per_day=round(avg_hours, 2),
            overtime_hours=round(overtime, 2)
        )

    @staticmethod
    def calculate_project_stats(proyectos: List[Dict]) -> ProjectStats:
        """Calcular estadísticas de proyectos"""
        if not proyectos:
            return ProjectStats(0, 0, 0, 0, 0)

        total = len(proyectos)
        active = len([p for p in proyectos if p.get('estado') == 'activo'])
        completed = len([p for p in proyectos if p.get('estado') == 'completado'])
        total_budget = sum(p.get('presupuesto', 0) for p in proyectos)
        avg_value = total_budget / total if total > 0 else 0

        return ProjectStats(
            total_projects=total,
            active_projects=active,
            completed_projects=completed,
            total_budget=total_budget,
            average_project_value=round(avg_value, 2)
        )

    @staticmethod
    def calculate_task_stats(tareas: List[Dict]) -> TaskStats:
        """Calcular estadísticas de tareas"""
        if not tareas:
            return TaskStats(0, 0, 0, 0, 0)

        total = len(tareas)
        completed = len([t for t in tareas if t.get('estado') == 'completada'])
        pending = len([t for t in tareas if t.get('estado') == 'pendiente'])
        in_progress = len([t for t in tareas if t.get('estado') == 'en_progreso'])
        completion_rate = (completed / total * 100) if total > 0 else 0

        return TaskStats(
            total_tasks=total,
            completed_tasks=completed,
            pending_tasks=pending,
            in_progress_tasks=in_progress,
            completion_rate=round(completion_rate, 2)
        )

    @staticmethod
    def calculate_employee_stats(empleados: List[Dict], jornadas: List[Dict]) -> EmployeeStats:
        """Calcular estadísticas de empleados"""
        if not empleados:
            return EmployeeStats(0, 0, 0, 0)

        total = len(empleados)
        active = len([e for e in empleados if e.get('activo', True)])

        # Empleados nuevos este mes
        current_month = datetime.now().month
        current_year = datetime.now().year
        new_this_month = 0

        for emp in empleados:
            if 'fecha_contratacion' in emp:
                try:
                    hire_date = datetime.fromisoformat(emp['fecha_contratacion'].replace('Z', '+00:00'))
                    if hire_date.month == current_month and hire_date.year == current_year:
                        new_this_month += 1
                except:
                    continue

        # Promedio de horas por empleado
        if jornadas and active > 0:
            total_hours = sum(j.get('total_horas', 0) for j in jornadas)
            avg_hours = total_hours / active
        else:
            avg_hours = 0

        return EmployeeStats(
            total_employees=total,
            active_employees=active,
            new_employees_this_month=new_this_month,
            average_hours_per_employee=round(avg_hours, 2)
        )

    @staticmethod
    def generate_productivity_report(jornadas: List[Dict], tareas: List[Dict]) -> Dict:
        """Generar reporte de productividad"""
        if not jornadas:
            return {
                'productivity_score': 0,
                'tasks_per_hour': 0,
                'efficiency_rating': 'Baja'
            }

        total_hours = sum(j.get('total_horas', 0) for j in jornadas)
        completed_tasks = len([t for t in tareas if t.get('estado') == 'completada'])

        tasks_per_hour = completed_tasks / total_hours if total_hours > 0 else 0

        # Calcular score de productividad (0-100)
        if tasks_per_hour > 1.5:
            score = min(100, tasks_per_hour * 40)
            rating = 'Excelente'
        elif tasks_per_hour > 1.0:
            score = tasks_per_hour * 50
            rating = 'Buena'
        elif tasks_per_hour > 0.5:
            score = tasks_per_hour * 60
            rating = 'Normal'
        else:
            score = tasks_per_hour * 80
            rating = 'Mejorable'

        return {
            'productivity_score': round(score, 2),
            'tasks_per_hour': round(tasks_per_hour, 2),
            'efficiency_rating': rating
        }

    @staticmethod
    def get_weekly_trend(jornadas: List[Dict]) -> List[Dict]:
        """Obtener tendencia semanal"""
        if not jornadas:
            return []

        # Últimas 4 semanas
        weekly_data = []
        for i in range(4):
            week_start = datetime.now() - timedelta(weeks=i+1)
            week_end = week_start + timedelta(days=7)

            week_hours = 0
            for jornada in jornadas:
                try:
                    jornada_date = datetime.fromisoformat(jornada.get('fecha', '').replace('Z', '+00:00'))
                    if week_start <= jornada_date < week_end:
                        week_hours += jornada.get('total_horas', 0)
                except:
                    continue

            weekly_data.append({
                'week': f"Semana {4-i}",
                'hours': round(week_hours, 2),
                'start_date': week_start.strftime('%Y-%m-%d'),
                'end_date': (week_end - timedelta(days=1)).strftime('%Y-%m-%d')
            })

        return list(reversed(weekly_data))

    @staticmethod
    def get_project_progress(proyectos: List[Dict], tareas: List[Dict]) -> List[Dict]:
        """Obtener progreso de proyectos"""
        project_progress = []

        for proyecto in proyectos:
            proyecto_id = proyecto.get('id')
            proyecto_tareas = [t for t in tareas if t.get('proyecto_id') == proyecto_id]

            if proyecto_tareas:
                completed = len([t for t in proyecto_tareas if t.get('estado') == 'completada'])
                total = len(proyecto_tareas)
                progress = (completed / total * 100) if total > 0 else 0

                project_progress.append({
                    'project_name': proyecto.get('nombre', 'Sin nombre'),
                    'project_id': proyecto_id,
                    'total_tasks': total,
                    'completed_tasks': completed,
                    'progress_percentage': round(progress, 2),
                    'status': proyecto.get('estado', 'activo'),
                    'budget': proyecto.get('presupuesto', 0)
                })

        return project_progress