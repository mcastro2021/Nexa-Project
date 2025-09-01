# 🗄️ Guía de Migración de Base de Datos - Nexa Project

## 📋 **Descripción del Problema**

El error `sqlite3.OperationalError: no such column: user.first_name` indica que la base de datos en Render.com no tiene la estructura correcta que requiere la aplicación.

## 🔧 **Solución Implementada**

### **1. Script de Migración Forzada (`force_migrate.py`)**
- **Función**: Elimina completamente la base de datos existente y la recrea desde cero
- **Ventaja**: Garantiza que la estructura sea 100% correcta
- **Desventaja**: Se pierden todos los datos existentes

### **2. Script de Verificación (`check_db.py`)**
- **Función**: Verifica que todas las tablas y columnas estén presentes
- **Uso**: Post-migración para confirmar éxito

### **3. Build Script Actualizado (`build.sh`)**
- **Función**: Ejecuta migración y verificación automáticamente
- **Trigger**: Se ejecuta en cada deploy de Render.com

## 🚀 **Proceso de Migración**

### **Paso 1: Deploy Automático**
```bash
# Render detecta cambios en GitHub
git push origin main
# Render ejecuta build.sh automáticamente
```

### **Paso 2: Migración Forzada**
```bash
# Se ejecuta force_migrate.py
python force_migrate.py
# - Elimina BD existente
# - Crea todas las tablas desde cero
# - Inserta datos iniciales
```

### **Paso 3: Verificación**
```bash
# Se ejecuta check_db.py
python check_db.py
# - Verifica estructura de tablas
# - Confirma columnas críticas
# - Valida datos iniciales
```

## 📊 **Estructura de Base de Datos**

### **Tabla `user`**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT,           -- ✅ NUEVA COLUMNA
    last_name TEXT,            -- ✅ NUEVA COLUMNA
    phone_number TEXT,         -- ✅ NUEVA COLUMNA
    role TEXT DEFAULT 'user',  -- ✅ NUEVA COLUMNA
    is_active INTEGER DEFAULT 1, -- ✅ NUEVA COLUMNA
    last_login DATETIME,       -- ✅ NUEVA COLUMNA
    password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Tabla `lead`**
```sql
CREATE TABLE lead (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT,
    company TEXT,
    status TEXT DEFAULT 'NUEVO',
    source TEXT DEFAULT 'OTRO',
    interest_level INTEGER DEFAULT 3,
    notes TEXT,
    next_follow_up DATETIME,
    last_contact_date DATETIME,
    priority TEXT DEFAULT 'medium',      -- ✅ NUEVA COLUMNA
    estimated_value REAL,               -- ✅ NUEVA COLUMNA
    project_type TEXT,                  -- ✅ NUEVA COLUMNA
    location TEXT,                      -- ✅ NUEVA COLUMNA
    created_by_id INTEGER,              -- ✅ NUEVA COLUMNA
    assigned_to_id INTEGER,             -- ✅ NUEVA COLUMNA
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔑 **Datos Iniciales**

### **Usuario Administrador**
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin`
- **Email**: `admin@nexa.com`

### **Plantillas de Mensaje**
1. **Bienvenida**: Mensaje de bienvenida para nuevos leads
2. **Seguimiento**: Mensaje de seguimiento para leads existentes
3. **Oferta**: Mensaje promocional con descuentos

## ⚠️ **Consideraciones Importantes**

### **Pérdida de Datos**
- **⚠️ ADVERTENCIA**: La migración forzada elimina TODOS los datos existentes
- **✅ SOLUCIÓN**: Si necesitas preservar datos, exporta antes del deploy

### **Tiempo de Migración**
- **Duración**: ~30-60 segundos
- **Impacto**: La aplicación estará offline durante la migración

### **Verificación Post-Migración**
- **Automática**: Se ejecuta en cada build
- **Manual**: Puedes ejecutar `python check_db.py` localmente

## 🛠️ **Troubleshooting**

### **Error: "no such column: user.first_name"**
- **Causa**: Base de datos con estructura antigua
- **Solución**: Deploy automático ejecutará migración forzada

### **Error: "database is locked"**
- **Causa**: Múltiples conexiones simultáneas
- **Solución**: Reiniciar la aplicación en Render

### **Error: "table already exists"**
- **Causa**: Conflicto durante migración
- **Solución**: La migración forzada elimina y recrea todo

## 📈 **Monitoreo Post-Migración**

### **Logs de Render**
```bash
# Buscar estas líneas en los logs:
✅ Migración forzada completada exitosamente!
✅ Base de datos está en buen estado!
```

### **Verificación Manual**
```bash
# Acceder a la aplicación
# Login con admin/admin123
# Verificar que todas las funcionalidades funcionen
```

## 🎯 **Próximos Pasos**

1. **Deploy Automático**: Los cambios se aplicarán automáticamente
2. **Verificación**: La aplicación debería funcionar sin errores
3. **Funcionalidades**: Todas las características estarán disponibles
4. **Monitoreo**: Verificar logs y funcionalidad

## 📞 **Soporte**

Si encuentras problemas después de la migración:
1. Revisar logs de Render.com
2. Ejecutar `python check_db.py` localmente
3. Verificar que `force_migrate.py` se ejecute correctamente
4. Contactar soporte técnico si persisten los problemas

---

**🎉 ¡La migración forzada resolverá definitivamente el problema de compatibilidad de base de datos!**
