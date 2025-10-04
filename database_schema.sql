-- ====================================================
-- ESQUEMA DE BASE DE DATOS PARA SISTEMA DE EMPLEADOS
-- PyLink - Gestión de Proyectos y Jornadas
-- ====================================================

-- Tabla de Empleados
CREATE TABLE empleados (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    rol VARCHAR(50) NOT NULL, -- 'admin', 'desarrollador', 'diseñador', etc.
    activo BOOLEAN DEFAULT true,
    fecha_ingreso DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de Proyectos
CREATE TABLE proyectos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    cliente VARCHAR(200),
    estado VARCHAR(50) DEFAULT 'activo', -- 'activo', 'pausado', 'completado', 'cancelado'
    fecha_inicio DATE,
    fecha_fin_estimada DATE,
    fecha_fin_real DATE,
    progreso INTEGER DEFAULT 0 CHECK (progreso >= 0 AND progreso <= 100),
    presupuesto_horas INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de Asignación de Empleados a Proyectos
CREATE TABLE proyecto_empleado (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID REFERENCES proyectos(id) ON DELETE CASCADE,
    empleado_id UUID REFERENCES empleados(id) ON DELETE CASCADE,
    rol_en_proyecto VARCHAR(100), -- 'Lead Developer', 'Designer', 'Support', etc.
    fecha_asignacion DATE DEFAULT CURRENT_DATE,
    fecha_desasignacion DATE,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(proyecto_id, empleado_id)
);

-- Tabla de Jornadas Laborales (Registro de Horas)
CREATE TABLE jornadas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empleado_id UUID REFERENCES empleados(id) ON DELETE CASCADE,
    proyecto_id UUID REFERENCES proyectos(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    hora_inicio TIMESTAMP,
    hora_fin TIMESTAMP,
    horas_trabajadas DECIMAL(5,2), -- Calculado automáticamente
    descripcion TEXT, -- Qué se hizo en esas horas
    estado VARCHAR(50) DEFAULT 'completada', -- 'en_progreso', 'completada', 'pausada'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de Tareas
CREATE TABLE tareas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID REFERENCES proyectos(id) ON DELETE CASCADE,
    empleado_asignado_id UUID REFERENCES empleados(id) ON DELETE SET NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    prioridad VARCHAR(20) DEFAULT 'media', -- 'baja', 'media', 'alta', 'urgente'
    estado VARCHAR(50) DEFAULT 'pendiente', -- 'pendiente', 'en_progreso', 'completada', 'cancelada'
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE,
    fecha_completada DATE,
    horas_estimadas DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ====================================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- ====================================================

CREATE INDEX idx_empleados_email ON empleados(email);
CREATE INDEX idx_empleados_activo ON empleados(activo);
CREATE INDEX idx_proyectos_estado ON proyectos(estado);
CREATE INDEX idx_jornadas_empleado ON jornadas(empleado_id);
CREATE INDEX idx_jornadas_proyecto ON jornadas(proyecto_id);
CREATE INDEX idx_jornadas_fecha ON jornadas(fecha);
CREATE INDEX idx_tareas_empleado ON tareas(empleado_asignado_id);
CREATE INDEX idx_tareas_proyecto ON tareas(proyecto_id);
CREATE INDEX idx_tareas_estado ON tareas(estado);

-- ====================================================
-- FUNCIONES Y TRIGGERS
-- ====================================================

-- Función para actualizar 'updated_at' automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar 'updated_at'
CREATE TRIGGER update_empleados_updated_at BEFORE UPDATE ON empleados
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_proyectos_updated_at BEFORE UPDATE ON proyectos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jornadas_updated_at BEFORE UPDATE ON jornadas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tareas_updated_at BEFORE UPDATE ON tareas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para calcular horas trabajadas automáticamente
CREATE OR REPLACE FUNCTION calcular_horas_trabajadas()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.hora_inicio IS NOT NULL AND NEW.hora_fin IS NOT NULL THEN
        NEW.horas_trabajadas = EXTRACT(EPOCH FROM (NEW.hora_fin - NEW.hora_inicio)) / 3600;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular horas automáticamente
CREATE TRIGGER calcular_horas_jornada BEFORE INSERT OR UPDATE ON jornadas
    FOR EACH ROW EXECUTE FUNCTION calcular_horas_trabajadas();

-- ====================================================
-- DATOS DE PRUEBA (SEED DATA)
-- ====================================================

-- Insertar empleados de prueba (contraseñas hasheadas con bcrypt)
-- Nota: Las contraseñas reales son 'emp123' y 'admin123'
INSERT INTO empleados (email, password_hash, nombre, apellidos, rol) VALUES
('juan@pylink.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5SupAhR8L3qFa', 'Juan', 'Pérez', 'desarrollador'),
('maria@pylink.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5SupAhR8L3qFa', 'María', 'García', 'diseñadora'),
('admin@pylink.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5SupAhR8L3qFa', 'Administrador', 'Sistema', 'admin');

-- Insertar proyectos de ejemplo
INSERT INTO proyectos (nombre, descripcion, cliente, estado, fecha_inicio, progreso, presupuesto_horas) VALUES
('E-commerce Tienda Online', 'Desarrollo de plataforma e-commerce completa con pasarela de pagos', 'TechStore S.A.', 'activo', '2024-09-01', 68, 320),
('App Móvil Delivery', 'Aplicación móvil para delivery de comida rápida', 'FastFood Corp', 'activo', '2024-09-15', 25, 280),
('Portal Web Corporativo', 'Sitio web corporativo con CMS personalizado', 'Empresa XYZ', 'completado', '2024-07-01', 100, 160);

-- Nota: Los IDs se generarán automáticamente. Para las siguientes inserciones,
-- necesitarás usar los IDs reales de tu base de datos o consultar primero.

-- ====================================================
-- VISTAS ÚTILES
-- ====================================================

-- Vista de resumen de horas por empleado y proyecto
CREATE OR REPLACE VIEW resumen_horas_empleado AS
SELECT 
    e.id as empleado_id,
    e.nombre || ' ' || COALESCE(e.apellidos, '') as empleado,
    p.id as proyecto_id,
    p.nombre as proyecto,
    COUNT(j.id) as total_jornadas,
    SUM(j.horas_trabajadas) as total_horas,
    AVG(j.horas_trabajadas) as promedio_horas_dia
FROM empleados e
LEFT JOIN jornadas j ON e.id = j.empleado_id
LEFT JOIN proyectos p ON j.proyecto_id = p.id
GROUP BY e.id, e.nombre, e.apellidos, p.id, p.nombre;

-- Vista de proyectos activos con empleados asignados
CREATE OR REPLACE VIEW proyectos_con_empleados AS
SELECT 
    p.id as proyecto_id,
    p.nombre as proyecto,
    p.estado,
    p.progreso,
    e.id as empleado_id,
    e.nombre || ' ' || COALESCE(e.apellidos, '') as empleado,
    pe.rol_en_proyecto
FROM proyectos p
LEFT JOIN proyecto_empleado pe ON p.id = pe.proyecto_id
LEFT JOIN empleados e ON pe.empleado_id = e.id
WHERE p.estado = 'activo' AND pe.activo = true;

-- ====================================================
-- POLÍTICAS DE SEGURIDAD (Row Level Security - RLS)
-- ====================================================

-- Habilitar RLS en las tablas principales
ALTER TABLE empleados ENABLE ROW LEVEL SECURITY;
ALTER TABLE proyectos ENABLE ROW LEVEL SECURITY;
ALTER TABLE jornadas ENABLE ROW LEVEL SECURITY;
ALTER TABLE tareas ENABLE ROW LEVEL SECURITY;

-- Nota: Las políticas específicas se configurarán según tus necesidades de autenticación
-- Por ahora, permite acceso completo para desarrollo (ajustar en producción)
CREATE POLICY "Permitir todo para desarrollo" ON empleados FOR ALL USING (true);
CREATE POLICY "Permitir todo para desarrollo" ON proyectos FOR ALL USING (true);
CREATE POLICY "Permitir todo para desarrollo" ON jornadas FOR ALL USING (true);
CREATE POLICY "Permitir todo para desarrollo" ON tareas FOR ALL USING (true);
