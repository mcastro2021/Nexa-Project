# 🚀 Despliegue en Render.com - Nexa Lead Manager

## ✅ **Configuración Automática Completada**

El proyecto está completamente configurado para desplegarse automáticamente en Render.com.

---

## 🎯 **Pasos para Desplegar**

### **1. Preparar el Repositorio**
- ✅ Asegúrate de que todos los cambios estén commitados y pusheados a GitHub
- ✅ Verifica que el repositorio sea público o que tengas acceso desde Render

### **2. Crear Cuenta en Render**
1. Ve a [render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub

### **3. Crear Nuevo Servicio Web**
1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente la configuración

### **4. Configurar Variables de Entorno**
En la sección **"Environment Variables"** del servicio, agrega:

```env
# Configuración de Twilio (WhatsApp Business API)
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=your_auth_token_here
WHATSAPP_FROM=whatsapp:+1234567890

# Configuración de la aplicación
FLASK_ENV=production
DATABASE_URL=sqlite:///nexa_leads.db

# Configuración de administrador
ADMIN_WHATSAPP=+5491112345678

# Configuración de OpenAI (opcional)
OPENAI_API_KEY=sk-1234567890abcdef...

# Configuración de logging
LOG_LEVEL=INFO
```

**Nota**: `SECRET_KEY` se generará automáticamente por Render.

### **5. Desplegar**
1. Haz clic en **"Create Web Service"**
2. Render comenzará el despliegue automáticamente
3. El proceso tomará aproximadamente 5-10 minutos

---

## 🔧 **Configuración Automática Incluida**

### **Archivos de Configuración**
- ✅ `render.yaml` - Configuración del servicio
- ✅ `Procfile` - Comando de inicio
- ✅ `gunicorn.conf.py` - Configuración del servidor
- ✅ `build.sh` - Script de build optimizado
- ✅ `init_render.py` - Inicialización del entorno
- ✅ `runtime.txt` - Versión de Python

### **Configuración del Servicio**
- **Tipo**: Web Service
- **Plan**: Starter (gratuito)
- **Python**: 3.10.12
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn app:app`

---

## 📱 **Configurar WhatsApp Business API**

### **1. Obtener Credenciales de Twilio**
1. Ve a [twilio.com](https://www.twilio.com)
2. Crea una cuenta o inicia sesión
3. Ve a **Console** → **Dashboard**
4. Copia tu **Account SID** y **Auth Token**

### **2. Configurar WhatsApp Sandbox**
1. En Twilio Console, ve a **Messaging** → **Settings** → **WhatsApp Sandbox**
2. Copia el número de WhatsApp proporcionado
3. Configura el **Webhook URL** en tu servicio de Render:
   ```
   https://tu-app.onrender.com/webhook
   ```

### **3. Probar la Integración**
1. Envía un mensaje al número de WhatsApp de Twilio
2. El bot debería responder automáticamente
3. Verifica los logs en Render para confirmar

---

## 🗄️ **Base de Datos**

### **SQLite (Incluido)**
- ✅ Base de datos SQLite incluida por defecto
- ✅ Se inicializa automáticamente en el primer despliegue
- ✅ Usuario admin creado: `admin` / `admin123`

### **PostgreSQL (Recomendado para Producción)**
Para mayor escalabilidad, considera usar PostgreSQL:

1. En Render, crea un **PostgreSQL Database**
2. Copia la **Database URL** proporcionada
3. Actualiza la variable `DATABASE_URL` en tu servicio web
4. Ejecuta las migraciones de la base de datos

---

## 📊 **Monitoreo y Logs**

### **Acceder a Logs**
1. En tu servicio de Render, ve a **"Logs"**
2. Revisa **"Build Logs"** para errores de construcción
3. Revisa **"Runtime Logs"** para errores de ejecución

### **Métricas del Servicio**
- **CPU Usage**: Monitoreo en tiempo real
- **Memory Usage**: Uso de memoria
- **Request Count**: Número de solicitudes
- **Response Time**: Tiempo de respuesta

---

## 🚨 **Solución de Problemas Comunes**

### **Error: "Build Failed"**
```bash
# Verificar logs de build
# Problemas comunes:
# - Dependencias no encontradas
# - Errores de sintaxis en Python
# - Problemas de permisos en build.sh
```

### **Error: "Service Failed to Start"**
```bash
# Verificar logs de runtime
# Problemas comunes:
# - Variables de entorno faltantes
# - Puerto en uso
# - Errores en la base de datos
```

### **Error: "Module Not Found"**
```bash
# Verificar requirements.txt
# Asegurarse de que todas las dependencias estén listadas
# Verificar que build.sh se ejecute correctamente
```

---

## 🔄 **Actualizaciones y Re-despliegue**

### **Despliegue Automático**
- ✅ Render detecta cambios automáticamente
- ✅ Se re-despliega cada vez que haces push a la rama principal
- ✅ No es necesario hacer nada manualmente

### **Despliegue Manual**
1. En tu servicio de Render, haz clic en **"Manual Deploy"**
2. Selecciona la rama o commit deseado
3. Haz clic en **"Deploy Latest Commit"**

---

## 🌐 **Acceso al Sistema**

### **URL del Servicio**
```
https://tu-app.onrender.com
```

### **Credenciales de Acceso**
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### **Endpoints Disponibles**
- **Dashboard**: `/` (requiere login)
- **API Stats**: `/api/stats`
- **API Leads**: `/api/leads`
- **API Campaigns**: `/api/campaigns`
- **Webhook WhatsApp**: `/webhook`

---

## 🎉 **¡Despliegue Completado!**

Una vez que el servicio esté funcionando:

1. ✅ **Accede al dashboard**: https://tu-app.onrender.com
2. ✅ **Configura WhatsApp**: Sigue las instrucciones de Twilio
3. ✅ **Prueba las funcionalidades**: Crea leads, envía mensajes
4. ✅ **Monitorea el rendimiento**: Revisa logs y métricas

**¡Tu sistema de gestión de leads está listo para producción!** 🚀
