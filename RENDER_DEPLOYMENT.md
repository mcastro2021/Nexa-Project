# 🚀 Guía de Despliegue en Render - Nexa Lead Manager

## 📋 Opciones de Despliegue

### **Opción 1: Despliegue Estándar (Recomendado)**
1. Crear cuenta en [Render](https://render.com)
2. Conectar repositorio de GitHub
3. Render detectará automáticamente `render.yaml`
4. Configurar variables de entorno
5. Desplegar

### **Opción 2: Despliegue con Docker**
Si el despliegue estándar falla:
1. Usar `render-docker.yaml` en lugar de `render.yaml`
2. Render usará el `Dockerfile` para construir la imagen
3. Más estable pero más lento

### **Opción 3: Despliegue Manual**
Si ambos fallan:
1. Crear servicio web manualmente en Render
2. Usar `build-fallback.sh` como comando de build
3. Configurar variables de entorno manualmente

## 🔧 Variables de Entorno Requeridas

```env
# Configuración de Twilio (WhatsApp Business API)
TWILIO_ACCOUNT_SID=tu_account_sid_de_twilio
TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
WHATSAPP_FROM=whatsapp:+1234567890

# Configuración de la aplicación
SECRET_KEY=tu-secret-key-seguro
FLASK_ENV=production
DATABASE_URL=sqlite:///nexa_leads.db

# Configuración de administrador
ADMIN_WHATSAPP=+5491112345678

# Configuración de OpenAI (opcional)
OPENAI_API_KEY=tu_openai_api_key

# Configuración de logging
LOG_LEVEL=INFO
```

## 🛠️ Solución de Problemas

### **Error de pandas**
Si ves errores de compilación de pandas:
1. Usar `render-docker.yaml` (Opción 2)
2. O cambiar el comando de build a: `chmod +x build-fallback.sh && ./build-fallback.sh`

### **Error de Python 3.13**
El proyecto está configurado para Python 3.10.12:
- `runtime.txt`: python-3.10.12
- `render.yaml`: PYTHON_VERSION=3.10.12

### **Error de dependencias**
Si hay problemas con dependencias:
1. Usar `requirements-minimal.txt`
2. Instalar pandas y plotly manualmente después del despliegue

## 📊 Monitoreo

### **Logs de Build**
- Revisar logs en el dashboard de Render
- Verificar que Python 3.10.12 se use
- Confirmar que no hay errores de pandas

### **Logs de Aplicación**
- Monitorear logs en tiempo real
- Verificar que la aplicación inicie correctamente
- Confirmar que la base de datos se cree

## 🎯 Verificación del Despliegue

1. **Acceso al dashboard**: `https://tu-app.onrender.com`
2. **Login**: admin / admin123
3. **Verificar funcionalidades**:
   - Dashboard carga correctamente
   - Analytics funcionan
   - Importación de leads funciona
   - Plantillas se muestran

## 📞 Soporte

Si persisten los problemas:
1. Revisar logs completos en Render
2. Verificar que todas las variables de entorno estén configuradas
3. Probar con el Dockerfile como alternativa
4. Contactar soporte de Render si es necesario

---

**¡El proyecto está optimizado para Render y debería desplegarse sin problemas!** 🚀
