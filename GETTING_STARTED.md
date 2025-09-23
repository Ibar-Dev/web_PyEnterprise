# 🚀 Guía de Inicio Rápido - PyEnterprise

## ✅ Errores Solucionados

1. **Error `app.compile()`**: ❌ Removido - No es necesario en versiones recientes de Reflex
2. **Errores de modelos**: ❌ Simplificados para compatibilidad
3. **Imports problemáticos**: ❌ Corregidos

## 🏃‍♂️ Iniciar la Aplicación

### Opción 1: Comando directo
```bash
reflex run
```

### Opción 2: Usando el script de gestión
```bash
python manage.py runserver
```

## 🌐 URLs Disponibles

- **Página Principal**: http://localhost:3000
- **Panel Admin**: http://localhost:3000/admin (en desarrollo)

## 📋 Funcionalidades Actuales

### ✅ Funcionando
- ✅ Página principal con todas las secciones
- ✅ Formulario de contacto (frontend)
- ✅ Diseño responsive
- ✅ Navegación suave entre secciones
- ✅ Estilos profesionales

### 🚧 En Desarrollo (Backend)
- 🚧 Base de datos para contactos
- 🚧 Panel de administración
- 🚧 Sistema de emails automático
- 🚧 Gestión de servicios dinámicos

## 🛠️ Próximos Pasos

### 1. Personalizar Contenido
Editar los archivos en `pyenterprise/components/`:
- `hero.py` - Mensaje principal y estadísticas
- `about.py` - Información de la empresa
- `services.py` - Servicios oferecidos
- `contact.py` - Información de contacto

### 2. Añadir tu Logo
Reemplazar `assets/logo.png` con tu logo real

### 3. Configurar Colores
Editar `pyenterprise/styles.py` para cambiar la paleta de colores:
```python
COLORS = {
    "primary": "#2563eb",    # Tu color principal
    "secondary": "#1e40af",  # Tu color secundario
    # ... más colores
}
```

### 4. Activar Backend (Opcional)
Para habilitar el backend completo:

1. **Instalar dependencias adicionales**:
   ```bash
   pip install sqlalchemy alembic python-dotenv
   ```

2. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env con tu configuración
   ```

3. **Poblar base de datos**:
   ```bash
   python seed_data.py
   ```

## 🎨 Personalización Avanzada

### Cambiar Fuente
En `pyenterprise.py`, línea 34:
```python
"https://fonts.googleapis.com/css2?family=TU_FUENTE:wght@300;400;500;600;700&display=swap"
```

### Añadir Nuevas Secciones
1. Crear nuevo componente en `components/`
2. Importar en `pyenterprise.py`
3. Añadir al layout en la función `index()`

### Modificar Servicios
Editar la función `service_card()` en `components/services.py`

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
# Verificar estructura de archivos
ls pyenterprise/
ls pyenterprise/components/
```

### Error: "Permission denied"
```bash
# En Windows, ejecutar como administrador
# En Linux/Mac:
sudo reflex run
```

### Error de puertos
```bash
# Cambiar puerto en rxconfig.py
config = rx.Config(port=8000)
```

## 📞 Soporte

Si encuentras algún problema:
1. Revisa los logs en la terminal
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de estar en el directorio correcto

## 🎉 ¡Listo!

Tu página web de PyEnterprise está funcionando. Visita http://localhost:3000 para verla en acción.

---
**PyEnterprise** - Soluciones Empresariales con Python 🐍✨
