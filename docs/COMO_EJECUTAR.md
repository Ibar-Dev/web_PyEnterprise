# 🚀 Cómo Ejecutar el Proyecto

## 📋 Guía Rápida de Ejecución

### **Iniciar la Aplicación**
```bash
# Desde la raíz del proyecto
reflex run
```
URL: **http://localhost:3000**

---

## 🧪 Ejecutar Tests

### **Todos los tests están en `tests/`**

```bash
# Test completo del backend
python tests/test_backend_completo.py

# Test de autenticación
python tests/test_login.py

# Test del sistema completo
python tests/test_sistema_completo.py

# Test de Supabase
python tests/test_supabase.py
```

---

## 🛠️ Ejecutar Scripts Auxiliares

### **Todos los scripts están en `scripts/`**

```bash
# Agregar datos de prueba
python scripts/agregar_datos_prueba.py

# Asignar admin a un proyecto
python scripts/asignar_admin_proyecto.py

# Actualizar contraseñas (si es necesario)
python scripts/fix_passwords.py

# Seed de datos iniciales
python scripts/seed_data.py
```

---

## 📚 Ver Documentación

### **Toda la documentación está en `docs/`**

```bash
# Listar documentación
ls docs/

# Archivos disponibles:
- CAMBIOS_REALIZADOS.md       # Cambios recientes
- COMO_EJECUTAR.md             # Esta guía
- database_schema.md           # Esquema de BD
- DOCUMENTACION_COMPLETA.md    # Documentación completa
- ESTRUCTURA.md                # Estructura del proyecto
- GETTING_STARTED.md           # Guía de inicio
- GUIA_RAPIDA.md               # Guía rápida
- REORGANIZACION.md            # Detalles de reorganización
```

---

## 🔑 Credenciales de Acceso

### **Administrador**
```
URL: http://localhost:3000/empleados
Email: admin@pylink.com
Contraseña: admin123
→ Redirige automáticamente a /admin
```

### **Empleados**
```
Juan (Desarrollador):
Email: juan@pylink.com
Contraseña: emp123

María (Diseñadora):
Email: maria@pylink.com
Contraseña: emp123
```

---

## 🐛 Solución de Problemas

### **Error: "No module named 'pyenterprise'"**
**Solución:** Ejecuta los scripts/tests desde la raíz del proyecto:
```bash
# ✅ Correcto
python tests/test_backend_completo.py

# ❌ Incorrecto
cd tests
python test_backend_completo.py
```

### **Error: "reflex: command not found"**
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### **Error: Variables de entorno no configuradas**
**Solución:** Crea el archivo `.env`:
```bash
cp .env.example .env
# Editar .env con tus credenciales de Supabase
```

### **Error: "Connection refused"**
**Solución:** Verifica que Supabase esté configurado correctamente en `.env`

---

## 📁 Estructura del Proyecto

```
web_PyEnterprise/
├── docs/                    # 📄 Documentación (aquí estás)
├── tests/                   # 🧪 Tests
├── scripts/                 # 🛠️ Scripts auxiliares
├── pyenterprise/            # 💻 Código principal
│   ├── components/          # Frontend
│   └── database/            # Backend
├── app.py                   # Entry point
├── requirements.txt         # Dependencias
└── rxconfig.py              # Configuración Reflex
```

---

## ⚡ Comandos Rápidos

```bash
# Iniciar app
reflex run

# Test rápido
python tests/test_backend_completo.py

# Agregar datos de prueba
python scripts/agregar_datos_prueba.py

# Ver docs
ls docs/
```

---

## 🎯 Flujo de Trabajo Recomendado

1. **Iniciar la aplicación:**
   ```bash
   reflex run
   ```

2. **En otra terminal, agregar datos de prueba:**
   ```bash
   python scripts/agregar_datos_prueba.py
   ```

3. **Acceder al panel de admin:**
   - Ir a: http://localhost:3000/empleados
   - Login: admin@pylink.com / admin123

4. **Probar funcionalidades:**
   - Crear proyectos
   - Crear tareas
   - Ver empleados
   - Ver estadísticas

---

## 📞 Ayuda Adicional

- **Documentación completa:** `docs/DOCUMENTACION_COMPLETA.md`
- **Guía rápida:** `docs/GUIA_RAPIDA.md`
- **Cambios recientes:** `docs/CAMBIOS_REALIZADOS.md`

---

**¡Todo listo para usar! 🎉**
