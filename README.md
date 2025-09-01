# 🏗️ Nexa Lead Manager

Sistema integral de gestión de leads y automatización de WhatsApp para **Nexa Constructora**. Diseñado específicamente para reenviar mensajes a clientes potenciales que mostraron interés en los productos de construcción pero no continuaron el contacto.

## 🚀 Características Principales

### 📊 **Gestión Inteligente de Leads**
- **Seguimiento automático** de clientes potenciales
- **Estados de lead** personalizados (Nuevo, Contactado, Interesado, Calificado, Convertido, Perdido)
- **Fuentes de lead** (Website, WhatsApp, Referidos, Redes Sociales, Eventos)
- **Sistema de recordatorios** automáticos programados

### 💬 **Automatización de WhatsApp**
- **Plantillas personalizables** para diferentes tipos de mensajes
- **Envío automático** de mensajes de bienvenida
- **Seguimiento programado** con recordatorios inteligentes
- **Integración con Twilio** para WhatsApp Business API

### 📈 **Dashboard Web Moderno**
- **Interfaz intuitiva** con diseño responsive
- **Estadísticas en tiempo real** con gráficos interactivos
- **Gestión visual** de leads y campañas
- **Analytics avanzados** para optimizar conversiones

### 🎯 **Campañas Inteligentes**
- **Campañas automáticas** basadas en estado del lead
- **Programación flexible** de envíos
- **Segmentación por fuente** y comportamiento
- **Métricas de efectividad** en tiempo real

## 🛠️ Instalación y Configuración

### 1. **Requisitos Previos**
```bash
# Python 3.8+
python --version

# Git
git --version
```

### 2. **Clonar e Instalar**
```bash
# Clonar el repositorio
git clone <repository-url>
cd Nexa-Project

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. **Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp env_example .env

# Editar .env con tus credenciales
```

**Variables requeridas en `.env`:**
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
WHATSAPP_FROM=whatsapp:+1234567890

# OpenAI Configuration (opcional para respuestas inteligentes)
OPENAI_API_KEY=your_openai_api_key_here

# Dashboard Configuration
SECRET_KEY=your-secret-key-here
ADMIN_WHATSAPP=whatsapp:+5491112345678
```

### 4. **Inicializar Base de Datos**
```bash
# Ejecutar script de inicialización
python init_db.py
```

Este script creará:
- ✅ Usuario administrador (admin/admin123)
- ✅ Plantillas de mensajes por defecto
- ✅ Leads de ejemplo
- ✅ Campañas de demostración

## 🚀 Uso del Sistema

### **Iniciar el Dashboard Web**
```bash
python dashboard.py
```
Acceder a: `http://localhost:5001`
- Usuario: `admin`
- Contraseña: `admin123`

### **Iniciar el Bot de WhatsApp**
```bash
python app.py
```
El bot estará disponible en: `http://localhost:5000`

## 📱 Funcionalidades Principales

### **1. Gestión de Leads**
- **Importar leads** desde archivos CSV
- **Seguimiento automático** con recordatorios
- **Estados personalizables** para cada lead
- **Historial completo** de interacciones

### **2. Plantillas de Mensajes**
- **Bienvenida**: Mensaje automático para nuevos leads
- **Seguimiento**: Recordatorios personalizados
- **Ofertas**: Promociones especiales
- **Consultas**: Solicitud de información del proyecto

### **3. Campañas Automáticas**
- **Seguimiento semanal** para leads contactados
- **Recordatorio mensual** para leads nuevos
- **Ofertas especiales** para leads calificados
- **Programación flexible** de envíos

### **4. Analytics y Reportes**
- **Dashboard en tiempo real** con métricas clave
- **Gráficos interactivos** de distribución de leads
- **Tasa de conversión** por fuente y período
- **Efectividad de campañas** con métricas detalladas

## 🎯 Casos de Uso para Nexa Constructora

### **Reenvío a Clientes Potenciales**
1. **Lead visita el sitio web** → Sistema detecta interés
2. **Mensaje automático de bienvenida** → Presentación de Nexa
3. **Seguimiento programado** → Recordatorios personalizados
4. **Ofertas especiales** → Promociones para reconectar
5. **Conversión** → Cliente retoma contacto

### **Campañas Específicas**
- **Proyectos residenciales**: Mensajes para construcción de casas
- **Desarrollo comercial**: Ofertas para edificios comerciales
- **Remodelaciones**: Promociones para renovaciones
- **Consultoría**: Servicios de asesoramiento técnico

## 📊 Métricas y Analytics

### **KPIs Principales**
- **Total de leads** gestionados
- **Tasa de conversión** por fuente
- **Efectividad de campañas** de WhatsApp
- **Tiempo promedio** hasta conversión
- **ROI de marketing** digital

### **Reportes Disponibles**
- **Dashboard ejecutivo** con métricas clave
- **Análisis por fuente** de leads
- **Efectividad de plantillas** de mensajes
- **Seguimiento de campañas** en tiempo real

## 🔧 Personalización

### **Plantillas de Mensajes**
Editar en el dashboard o directamente en la base de datos:

```python
# Ejemplo de plantilla personalizada
template = MessageTemplate(
    name='Oferta Especial Nexa',
    category='offer',
    content='🏗️ ¡Oferta especial para {name}! Descuento del 15% en construcción de {project_type}',
    variables='{"name": "Nombre", "project_type": "Tipo de proyecto"}'
)
```

### **Estados de Lead**
Personalizar el flujo de trabajo:

```python
# Estados disponibles
LeadStatus.NUEVO = "nuevo"
LeadStatus.CONTACTADO = "contactado"
LeadStatus.INTERESADO = "interesado"
LeadStatus.CALIFICADO = "calificado"
LeadStatus.CONVERTIDO = "convertido"
LeadStatus.PERDIDO = "perdido"
```

## 🔒 Seguridad

- **Autenticación** con Flask-Login
- **Encriptación** de contraseñas
- **Validación** de entrada de datos
- **Logs seguros** sin información sensible
- **Rate limiting** para prevenir spam

## 📈 Escalabilidad

### **Optimizaciones Implementadas**
- **Base de datos SQLite** para desarrollo
- **PostgreSQL** recomendado para producción
- **Caché Redis** para sesiones
- **CDN** para archivos estáticos
- **Load balancing** para alta disponibilidad

### **Monitoreo**
- **Logs estructurados** para debugging
- **Métricas de rendimiento** en tiempo real
- **Alertas automáticas** para errores críticos
- **Backup automático** de base de datos

## 🚀 Despliegue en Producción

### **Opción 1: Render (Recomendado) ✅**
El proyecto incluye configuración automática para Render:

**Archivos de configuración incluidos:**
- `render.yaml` - Configuración automática del servicio
- `Procfile` - Comando de inicio para producción
- `runtime.txt` - Versión específica de Python
- `gunicorn.conf.py` - Configuración optimizada de Gunicorn

**Pasos para desplegar:**
1. Crear cuenta en [Render](https://render.com)
2. Conectar repositorio de GitHub
3. Render detectará automáticamente la configuración
4. Configurar variables de entorno en el dashboard de Render
5. Desplegar automáticamente

### **Opción 2: Heroku**
```bash
# Crear aplicación
heroku create nexa-lead-manager
heroku addons:create heroku-postgresql:mini

# Configurar variables
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token

# Desplegar
git push heroku main
```

### **Opción 3: VPS (DigitalOcean/AWS)**
```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pip nginx

# Configurar Nginx
sudo nano /etc/nginx/sites-available/nexa-lead-manager

# Configurar SSL con Let's Encrypt
sudo certbot --nginx -d tu-dominio.com
```

### **Variables de Entorno Requeridas**

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

## 📞 Soporte y Contacto

### **Documentación Técnica**
- **API Reference**: `/api/docs`
- **Guías de usuario**: `/docs/user-guide`
- **Troubleshooting**: `/docs/troubleshooting`

### **Contacto Nexa Constructora**
- **Website**: https://nexaconstructora.com.ar
- **Email**: info@nexaconstructora.com.ar
- **WhatsApp**: +54 9 11 1234-5678

## 🤝 Contribución

1. **Fork** el proyecto
2. **Crear rama** feature (`git checkout -b feature/NuevaFuncionalidad`)
3. **Commit** cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/NuevaFuncionalidad`)
5. **Abrir Pull Request**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

**Desarrollado con ❤️ para Nexa Constructora**

*Sistema optimizado para maximizar la reconexión con clientes potenciales y aumentar las conversiones en el sector de la construcción.*
