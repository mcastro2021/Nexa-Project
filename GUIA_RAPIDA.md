# 🚀 Guía Rápida - Nexa Lead Manager

## 📋 Resumen del Sistema

**Nexa Lead Manager** es una aplicación completa para gestionar leads y automatizar el envío de mensajes de WhatsApp para **Nexa Constructora**. El sistema permite reconectar con clientes potenciales que mostraron interés pero no continuaron el contacto.

## 🎯 Funcionalidades Principales

### ✅ **Gestión de Leads**
- Importación masiva desde archivos CSV
- Seguimiento con estados personalizados
- Historial completo de interacciones
- Filtros y búsqueda avanzada

### ✅ **Automatización de WhatsApp**
- Plantillas de mensajes personalizables
- Envío automático de mensajes de bienvenida
- Campañas programadas de seguimiento
- Integración con Twilio WhatsApp Business API

### ✅ **Dashboard Web**
- Interfaz moderna y responsive
- Estadísticas en tiempo real
- Gráficos interactivos
- Analytics avanzados

### ✅ **Campañas Inteligentes**
- Campañas automáticas por estado
- Segmentación por fuente
- Programación flexible
- Métricas de efectividad

## 🚀 Inicio Rápido

### 1. **Acceso al Sistema**
```bash
# Iniciar el dashboard
python dashboard.py
```

**URL:** `http://localhost:5001`
**Usuario:** `admin`
**Contraseña:** `admin123`

### 2. **Configurar Twilio (WhatsApp)**
Editar el archivo `.env`:
```env
TWILIO_ACCOUNT_SID=tu_account_sid_de_twilio
TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
WHATSAPP_FROM=whatsapp:+1234567890
```

### 3. **Importar Leads**
1. Ir a **Leads** → **Importar Leads**
2. Seleccionar archivo CSV con formato:
   ```csv
   phone_number,name,email,company,notes
   5491112345678,Juan Pérez,juan@email.com,Empresa ABC,Interesado en casa
   ```

## 📊 Estados de Leads

| Estado | Descripción | Acción Sugerida |
|--------|-------------|-----------------|
| **Nuevo** | Lead recién creado | Enviar mensaje de bienvenida |
| **Contactado** | Primer contacto realizado | Seguimiento en 3-5 días |
| **Interesado** | Mostró interés activo | Propuesta detallada |
| **Calificado** | Lead validado | Negociación avanzada |
| **Convertido** | Cliente adquirido | Mantenimiento |
| **Perdido** | No continuó contacto | Reintento con oferta especial |

## 📝 Plantillas de Mensajes

### **Tipos Disponibles:**
- **Bienvenida**: Mensaje inicial automático
- **Seguimiento**: Recordatorios personalizados
- **Recordatorio**: Reenvío a leads perdidos
- **Oferta**: Promociones especiales
- **Consulta**: Solicitud de información

### **Variables Disponibles:**
- `{name}` - Nombre del cliente
- `{company}` - Empresa del cliente
- `{phone}` - Teléfono
- `{email}` - Email
- `{date}` - Fecha actual
- `{website}` - Sitio web de Nexa

## 📢 Crear Campañas

### **Paso a Paso:**
1. Ir a **Campañas** → **Nueva Campaña**
2. Seleccionar **Plantilla** de mensaje
3. Definir **Objetivo** (estado/fuente)
4. Programar **Fecha** de envío
5. **Guardar** y ejecutar

### **Ejemplos de Campañas:**
- **Reconexión Semanal**: Leads perdidos cada lunes
- **Oferta Mensual**: Descuentos especiales
- **Seguimiento Automático**: Recordatorios cada 3 días

## 📈 Analytics y Reportes

### **Métricas Disponibles:**
- Total de leads por período
- Tasa de conversión
- Tiempo promedio de respuesta
- Mensajes enviados
- Rendimiento por fuente

### **Gráficos Interactivos:**
- Distribución por estado
- Leads por fuente
- Evolución temporal
- Rendimiento comparativo

## 🔧 Comandos Útiles

```bash
# Inicializar base de datos
python init_db.py

# Iniciar dashboard
python dashboard.py

# Iniciar bot de WhatsApp
python app.py

# Probar sistema
python test_system.py

# Ejecutar script de inicio (Windows)
start.bat
```

## 📱 Casos de Uso para Nexa Constructora

### **1. Reconexión de Clientes Potenciales**
- Lead visita [nexaconstructora.com.ar](https://nexaconstructora.com.ar)
- Sistema detecta interés automáticamente
- Envío de mensaje de bienvenida personalizado
- Seguimiento programado cada 3-5 días

### **2. Campañas Específicas del Sector**
- **Construcción Residencial**: Casas y departamentos
- **Desarrollo Comercial**: Edificios comerciales
- **Remodelaciones**: Renovaciones y ampliaciones
- **Consultoría**: Asesoramiento técnico

### **3. Ofertas Temporales**
- Descuentos por temporada
- Promociones de lanzamiento
- Ofertas especiales para reconexión
- Eventos y ferias

## 🛠️ Solución de Problemas

### **Error: "Credenciales de Twilio no encontradas"**
- Verificar archivo `.env`
- Configurar `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN`
- Obtener credenciales en [twilio.com/console](https://www.twilio.com/console)

### **Error: "Template not found"**
- Verificar que todos los archivos HTML estén en `/templates`
- Reiniciar el servidor Flask

### **Error: "Database connection failed"**
- Verificar que `nexa_leads.db` existe
- Ejecutar `python init_db.py`

## 📞 Soporte

### **Archivos Importantes:**
- `README.md` - Documentación completa
- `requirements.txt` - Dependencias
- `env_example` - Configuración de ejemplo
- `sample_leads.csv` - Datos de prueba

### **Estructura del Proyecto:**
```
Nexa-Project/
├── dashboard.py          # Servidor web principal
├── lead_manager.py       # Lógica de negocio
├── models.py             # Modelos de base de datos
├── templates/            # Archivos HTML
├── .env                  # Configuración
└── nexa_leads.db        # Base de datos
```

## 🎉 ¡Listo para Usar!

El sistema **Nexa Lead Manager** está completamente configurado y listo para maximizar la reconexión con clientes potenciales de Nexa Constructora.

**¡Comienza a aumentar tus conversiones hoy mismo!**
