# Fix para Error 500 en Login - Nexa Project

## Problema Identificado

El error 500 en el endpoint `/login` se debía a problemas de inicialización de la base de datos cuando la aplicación se ejecuta en Render.com.

## Causas Principales

1. **Inconsistencia en rutas de base de datos**: Algunos archivos usaban `nexa_leads.db` mientras otros usaban `instance/nexa_leads.db`
2. **Falta de inicialización de BD**: `db.create_all()` solo se ejecutaba cuando se ejecutaba el archivo directamente, no cuando se importaba
3. **Manejo de errores insuficiente**: No había logging detallado para diagnosticar problemas de BD
4. **Falta de verificación de estado**: No se verificaba si la BD estaba disponible antes de procesar requests

## Soluciones Implementadas

### 1. Corrección de Rutas de Base de Datos

**Archivos modificados:**
- `dashboard.py`
- `wsgi.py` 
- `app.py`

**Cambios:**
- Estandarización de ruta de BD a `instance/nexa_leads.db`
- Configuración dinámica de ruta de BD desde variables de entorno
- Creación automática del directorio `instance` si no existe

### 2. Inicialización Automática de Base de Datos

**En `dashboard.py`:**
```python
# Crear todas las tablas de la base de datos
with app.app_context():
    try:
        print("🗄️ Creando tablas de la base de datos...")
        
        # Verificar que la base de datos esté disponible
        if not db.engine:
            print("❌ Motor de base de datos no disponible")
            raise Exception("Motor de base de datos no disponible")
        
        # Crear tablas
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        # Verificar que las tablas se crearon correctamente
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Tablas disponibles: {tables}")
        
        # Crear usuario admin por defecto
        # ... código para crear usuario admin
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        print("⚠️ La aplicación continuará pero puede no funcionar correctamente")
```

### 3. Mejora del Manejo de Errores en Login

**Endpoint `/login` mejorado:**
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            # Verificar que la base de datos esté disponible
            if not db.engine:
                logger.error("Base de datos no disponible")
                flash('Error del sistema. Por favor, contacte al administrador.')
                return render_template('login.html'), 500
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                logger.info(f"Usuario {username} autenticado exitosamente")
                return redirect(url_for('dashboard'))
            else:
                logger.warning(f"Intento de login fallido para usuario: {username}")
                flash('Usuario o contraseña incorrectos')
                
        except Exception as e:
            logger.error(f"Error durante el login: {e}")
            flash('Error del sistema. Por favor, contacte al administrador.')
            return render_template('login.html'), 500
    
    return render_template('login.html')
```

### 4. Endpoint de Verificación de Salud

**Nuevo endpoint `/health`:**
- Verifica estado de la base de datos
- Verifica existencia de directorios críticos
- Verifica archivos de base de datos
- Muestra variables de entorno configuradas
- Útil para diagnóstico en producción

### 5. Script de Prueba de Base de Datos

**Archivo `test_database.py`:**
- Prueba creación básica de BD
- Prueba creación de tabla user
- Verifica inserción y recuperación de datos
- Útil para testing local y diagnóstico

## Archivos Modificados

1. **`dashboard.py`** - Lógica principal de la aplicación
2. **`wsgi.py`** - Punto de entrada WSGI para Render
3. **`app.py`** - Archivo de compatibilidad
4. **`test_database.py`** - Script de prueba (nuevo)

## Cómo Probar

### 1. Verificar Estado del Sistema
```bash
curl https://nexa-project.onrender.com/health
```

### 2. Probar Login
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Testing Local
```bash
cd Nexa-Project
python test_database.py
```

## Variables de Entorno Configuradas

- `DATABASE_URL`: `sqlite:///instance/nexa_leads.db`
- `SECRET_KEY`: `dev-secret-key-change-in-production`
- `FLASK_ENV`: `production`

## Estructura de Directorios

```
Nexa-Project/
├── instance/          # Base de datos SQLite
├── logs/             # Logs de la aplicación
├── uploads/          # Archivos subidos
├── templates/        # Plantillas HTML
└── ...
```

## Próximos Pasos

1. **Deploy en Render**: Los cambios se aplicarán automáticamente
2. **Verificar logs**: Revisar logs de Render para confirmar inicialización exitosa
3. **Test de login**: Probar el endpoint `/login` con credenciales admin
4. **Monitoreo**: Usar endpoint `/health` para verificar estado del sistema

## Notas Importantes

- La aplicación ahora crea automáticamente la base de datos al iniciar
- Se incluye usuario admin por defecto: `admin/admin123`
- Mejor logging y manejo de errores para diagnóstico
- Compatible con Render.com y entornos de producción
