# 🚀 **GUÍA DE INICIO RÁPIDO - NEXA LEAD MANAGER**

## 📋 **RESUMEN DEL SISTEMA**

El **Nexa Lead Manager** es un sistema completo para gestionar leads y automatizar respuestas de WhatsApp con IA. Consta de:

### **🏗️ Componentes Principales:**
1. **Dashboard Web** - Gestión visual de leads y campañas
2. **Bot de WhatsApp** - Respuestas automáticas e inteligentes
3. **Lead Manager** - Lógica de negocio y automatización

---

## 🎯 **PASO 1: CONFIGURAR CREDENCIALES**

### **A) Crear archivo .env**
```bash
# Copiar el archivo de ejemplo
cp env_example .env
```

### **B) Configurar Twilio (WhatsApp Business API)**
1. **Registrarse en Twilio**: https://www.twilio.com
2. **Obtener credenciales**:
   - Account SID
   - Auth Token
   - Número de WhatsApp Business
3. **Configurar en .env**:
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=your_auth_token_here
WHATSAPP_FROM=whatsapp:+1234567890
```

### **C) Configurar OpenAI (Respuestas inteligentes)**
1. **Registrarse en OpenAI**: https://platform.openai.com
2. **Obtener API Key**
3. **Configurar en .env**:
```bash
OPENAI_API_KEY=sk-1234567890abcdef...
```

---

## 🤖 **PASO 2: CÓMO FUNCIONAN LAS RESPUESTAS AUTOMÁTICAS**

### **A) Respuestas por Palabras Clave**
El bot detecta automáticamente palabras clave y responde:

| **Palabra Clave** | **Respuesta Automática** |
|-------------------|--------------------------|
| "horario" | Horarios de atención detallados |
| "precio" | Precios y servicios |
| "ubicacion" | Ubicación y zonas de trabajo |
| "contacto" | Información de contacto directo |
| "servicios" | Lista completa de servicios |
| "ayuda" | Comandos disponibles |

### **B) Respuestas Inteligentes con GPT**
Para consultas complejas, el bot usa GPT para respuestas personalizadas:

**Ejemplo:**
- **Usuario**: "Necesito construir una casa de 150m² en San Isidro"
- **Bot**: Respuesta personalizada con recomendaciones específicas

### **C) Transferencia a Agente Humano**
Cuando el usuario dice "agente" o "humano", se activa la transferencia.

---

## 📱 **PASO 3: PROBAR EL BOT LOCALMENTE**

### **A) Ejecutar pruebas**
```bash
python test_bot.py
```

### **B) Ver respuestas automáticas**
El script mostrará cómo responde el bot a diferentes mensajes.

---

## 🌐 **PASO 4: DESPLEGAR EN RENDER**

### **A) Configurar variables de entorno en Render**
1. Ir a [render.com](https://render.com)
2. En tu servicio, ir a **Environment**
3. Agregar las variables del archivo `.env`

### **B) Variables requeridas:**
```
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=your_auth_token_here
WHATSAPP_FROM=whatsapp:+1234567890
OPENAI_API_KEY=sk-1234567890abcdef...
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

---

## 🔗 **PASO 5: CONFIGURAR WEBHOOK DE WHATSAPP**

### **A) En Twilio Console:**
1. Ir a **Messaging** > **Settings** > **WhatsApp Sandbox**
2. Configurar **Webhook URL**: `https://tu-app.onrender.com/webhook`
3. Método: **POST**

### **B) En tu aplicación:**
El webhook ya está configurado en el código para recibir mensajes.

---

## 📊 **PASO 6: GESTIONAR LEADS DESDE EL DASHBOARD**

### **A) Acceder al dashboard:**
- **URL**: `https://tu-app.onrender.com`
- **Login**: admin / admin123

### **B) Funcionalidades disponibles:**
- **Ver leads**: Lista completa de contactos
- **Editar leads**: Actualizar información
- **Enviar mensajes**: Comunicación directa
- **Crear campañas**: Mensajes automáticos
- **Analytics**: Estadísticas y reportes

---

## 🎯 **PASO 7: FLUJO DE TRABAJO COMPLETO**

### **1. Lead llega por WhatsApp**
```
👤 Cliente: "Hola, necesito información sobre construcción"
🤖 Bot: [Respuesta automática con horarios y servicios]
```

### **2. Lead se guarda automáticamente**
- Se crea un lead en la base de datos
- Se clasifica por interés
- Se programa seguimiento

### **3. Gestión desde el dashboard**
- Ver lead en la lista
- Actualizar estado (Nuevo → Contactado → Interesado → Convertido)
- Enviar mensajes personalizados
- Programar seguimientos

### **4. Campañas automáticas**
- Mensajes de seguimiento automático
- Recordatorios de citas
- Ofertas especiales

---

## 🚀 **PASO 8: PERSONALIZAR RESPUESTAS**

### **A) Editar respuestas automáticas**
Modificar archivo `bot_responses.py`:

```python
RESPUESTAS_AUTOMATICAS = {
    'tu_categoria': {
        'palabras_clave': ['palabra1', 'palabra2'],
        'respuesta': 'Tu respuesta personalizada aquí'
    }
}
```

### **B) Agregar nuevas categorías**
1. Agregar nueva entrada en `RESPUESTAS_AUTOMATICAS`
2. Definir palabras clave
3. Escribir respuesta personalizada

---

## 📈 **PASO 9: MÉTRICAS Y ANALYTICS**

### **A) Métricas disponibles:**
- Total de leads
- Leads por estado
- Tasa de conversión
- Mensajes enviados
- Respuestas del bot

### **B) Reportes automáticos:**
- Leads que necesitan seguimiento
- Conversiones semanales
- Efectividad de campañas

---

## 🔧 **PASO 10: MANTENIMIENTO**

### **A) Monitoreo diario:**
- Revisar leads nuevos
- Responder mensajes pendientes
- Actualizar estados de leads

### **B) Mejoras continuas:**
- Analizar respuestas del bot
- Optimizar palabras clave
- Ajustar campañas

---

## 🎉 **¡LISTO PARA EMPEZAR!**

### **✅ Checklist de inicio:**
- [ ] Credenciales de Twilio configuradas
- [ ] API key de OpenAI configurada
- [ ] Aplicación desplegada en Render
- [ ] Webhook configurado
- [ ] Dashboard accesible
- [ ] Bot probado localmente

### **🚀 Próximos pasos:**
1. **Configurar credenciales reales**
2. **Personalizar respuestas para tu negocio**
3. **Probar con mensajes reales**
4. **Empezar a recibir leads**
5. **Optimizar basado en resultados**

---

## 📞 **SOPORTE**

Si tienes problemas:
1. Revisar logs en Render
2. Verificar credenciales
3. Probar con `python test_bot.py`
4. Consultar documentación en `README.md`

**¡Tu sistema de leads automatizado está listo para funcionar!** 🎯📱
