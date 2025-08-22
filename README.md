# Nexa WhatsApp Bot

Un bot inteligente de WhatsApp para Nexa, empresa de desarrollo de software, que utiliza Twilio y OpenAI para proporcionar atención al cliente automatizada.

## 🚀 Características

- **Respuestas automáticas** para consultas frecuentes
- **Integración con GPT** para respuestas inteligentes
- **Base de datos SQLite** para almacenar conversaciones
- **Logging completo** para monitoreo
- **API REST** para estadísticas y envío de mensajes
- **Manejo de errores** robusto
- **Historial de conversaciones** para contexto

## 📋 Requisitos

- Python 3.8+
- Cuenta de Twilio con WhatsApp habilitado
- API key de OpenAI
- Conexión a internet

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd Nexa-Project
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
# Copiar el archivo de ejemplo
cp env_example .env

# Editar .env con tus credenciales
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
WHATSAPP_FROM=whatsapp:+1234567890

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# WhatsApp Contacts (comma-separated)
WHATSAPP_CONTACTOS=whatsapp:+5491111111111,whatsapp:+5492222222222
```

### Configurar Twilio

1. Crear cuenta en [Twilio](https://www.twilio.com/)
2. Obtener Account SID y Auth Token
3. Configurar WhatsApp Business API
4. Configurar webhook URL: `https://tu-dominio.com/webhook`

## 🚀 Uso

### Ejecutar en desarrollo:
```bash
python app.py
```

### Ejecutar en producción:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:bot.app
```

## 📡 Endpoints API

### Webhook (Twilio)
- **URL:** `/webhook`
- **Método:** POST
- **Descripción:** Recibe mensajes de WhatsApp

### Health Check
- **URL:** `/health`
- **Método:** GET
- **Descripción:** Verifica el estado del servicio

### Estadísticas
- **URL:** `/stats`
- **Método:** GET
- **Descripción:** Obtiene estadísticas del bot

### Enviar Mensaje
- **URL:** `/send-message`
- **Método:** POST
- **Body:**
```json
{
    "message": "Tu mensaje aquí",
    "contacts": ["whatsapp:+5491111111111"]
}
```

## 🤖 Comandos del Bot

El bot responde automáticamente a estas palabras clave:

- **horario** - Horario de atención
- **precio** - Información de precios
- **ubicacion** - Dirección de la empresa
- **contacto** - Información de contacto
- **servicios** - Servicios ofrecidos
- **ayuda** - Lista de comandos disponibles

## 📊 Base de Datos

El bot utiliza SQLite para almacenar:

- **conversations**: Historial de mensajes y respuestas
- **contacts**: Información de contactos

### Estructura de la base de datos:
```sql
-- Tabla de conversaciones
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    escalated BOOLEAN DEFAULT FALSE
);

-- Tabla de contactos
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 📝 Logging

El bot genera logs en:
- **Archivo:** `nexa_bot.log`
- **Consola:** Salida estándar

### Niveles de log:
- INFO: Operaciones normales
- ERROR: Errores y excepciones
- DEBUG: Información detallada (solo en desarrollo)

## 🔧 Personalización

### Agregar nuevas respuestas automáticas:

Edita el método `load_respuestas_bot()` en `app.py`:

```python
def load_respuestas_bot(self) -> Dict[str, str]:
    return {
        'horario': '🕐 Nuestro horario...',
        'tu_nueva_palabra': 'Tu nueva respuesta aquí',
        # ... más respuestas
    }
```

### Modificar el prompt de GPT:

Edita el método `responder_con_gpt()` en `app.py`:

```python
messages = [
    {
        "role": "system", 
        "content": "Tu prompt personalizado aquí"
    }
]
```

## 🚨 Manejo de Errores

El bot incluye manejo de errores para:
- Credenciales faltantes
- Errores de API de Twilio
- Errores de OpenAI
- Errores de base de datos
- Mensajes malformados

## 📈 Monitoreo

### Estadísticas disponibles:
- Total de conversaciones
- Conversaciones del día
- Contactos únicos
- Respuestas automáticas disponibles

### Verificar estado:
```bash
curl http://localhost:5000/health
curl http://localhost:5000/stats
```

## 🔒 Seguridad

- Validación de entrada
- Manejo seguro de credenciales
- Logs sin información sensible
- Rate limiting (implementar según necesidades)

## 🚀 Despliegue

### Opciones de despliegue:
1. **Heroku** - Fácil despliegue
2. **AWS EC2** - Control total
3. **Google Cloud** - Escalabilidad
4. **DigitalOcean** - Simplicidad

### Variables de producción:
```env
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico:
- Email: soporte@nexa.com
- WhatsApp: +54 9 11 1234-5678
- Documentación: [docs.nexa.com](https://docs.nexa.com)

---

**Desarrollado con ❤️ por el equipo de Nexa**
