#!/usr/bin/env python3
"""
Configuración de respuestas automáticas del bot de WhatsApp
"""

# Respuestas automáticas por palabras clave
RESPUESTAS_AUTOMATICAS = {
    'horario': {
        'palabras_clave': ['horario', 'hora', 'cuando', 'disponible', 'atencion'],
        'respuesta': '''🕐 **Horario de Atención Nexa Constructora**

📅 **Lunes a Viernes**: 9:00 AM - 6:00 PM
📅 **Sábados**: 9:00 AM - 1:00 PM
📅 **Domingos**: Cerrado

💬 **WhatsApp**: Disponible 24/7 para consultas urgentes
📞 **Teléfono**: +54 9 11 1234-5678

¿En qué horario te resulta más conveniente que te contactemos?'''
    },
    
    'precio': {
        'palabras_clave': ['precio', 'costo', 'cuanto', 'tarifa', 'presupuesto'],
        'respuesta': '''💰 **Precios y Servicios Nexa Constructora**

🏠 **Construcción Residencial**:
• Desde $2,500/m² (básico)
• Desde $3,500/m² (estándar)
• Desde $4,500/m² (premium)

🏢 **Construcción Comercial**:
• Desde $3,000/m² (básico)
• Desde $4,000/m² (estándar)

📋 **Incluye**:
✅ Diseño arquitectónico
✅ Permisos municipales
✅ Materiales de calidad
✅ Supervisión técnica
✅ Garantía de 2 años

💡 **¿Te gustaría que te prepare un presupuesto personalizado?**'''
    },
    
    'ubicacion': {
        'palabras_clave': ['ubicacion', 'donde', 'direccion', 'zona', 'barrio'],
        'respuesta': '''📍 **Ubicación Nexa Constructora**

🏢 **Oficina Principal**:
Av. Siempre Viva 123, Ciudad Autónoma de Buenos Aires

🗺️ **Zonas de Trabajo**:
• CABA y GBA Norte
• GBA Oeste
• GBA Sur
• Interior de la Provincia

🚗 **Servicios**:
✅ Visitas técnicas sin cargo
✅ Transporte de materiales
✅ Coordinación logística

📍 **¿En qué zona estás interesado? Te coordinamos una visita.**'''
    },
    
    'contacto': {
        'palabras_clave': ['contacto', 'llamar', 'hablar', 'agente', 'humano'],
        'respuesta': '''📞 **Contacto Directo Nexa Constructora**

👨‍💼 **Gerente de Ventas**: Juan Pérez
📱 **WhatsApp**: +54 9 11 1234-5678
📧 **Email**: juan.perez@nexaconstructora.com.ar

👩‍💼 **Asesora Comercial**: María García
📱 **WhatsApp**: +54 9 11 2345-6789
📧 **Email**: maria.garcia@nexaconstructora.com.ar

🏢 **Oficina**: +54 11 4567-8901
🌐 **Web**: https://nexaconstructora.com.ar

⏰ **Te contactamos en menos de 30 minutos**'''
    },
    
    'servicios': {
        'palabras_clave': ['servicios', 'que hacen', 'construccion', 'remodelacion'],
        'respuesta': '''🛠️ **Servicios Nexa Constructora**

🏗️ **Construcción**:
• Casas y departamentos
• Edificios comerciales
• Oficinas y locales
• Galpones industriales

🔨 **Remodelación**:
• Ampliaciones
• Refacciones completas
• Cambios de uso
• Mejoras estructurales

📐 **Diseño**:
• Arquitectura
• Interiorismo
• Paisajismo
• Ingeniería estructural

🏭 **Especialidades**:
• Construcción en seco
• Steel framing
• Construcción tradicional
• Sostenibilidad

💡 **¿Qué tipo de proyecto tienes en mente?**'''
    },
    
    'ayuda': {
        'palabras_clave': ['ayuda', 'comandos', 'opciones', 'menu'],
        'respuesta': '''🤖 **Comandos Disponibles Nexa Bot**

📋 **Consulta rápida**:
• "horario" - Horarios de atención
• "precio" - Precios y servicios
• "ubicacion" - Dónde estamos
• "contacto" - Hablar con agente
• "servicios" - Qué ofrecemos

💬 **O simplemente escribe tu consulta y te ayudo personalmente.**

🔄 **Para hablar con un agente humano, escribe "agente" o "humano"**

¿En qué puedo ayudarte hoy? 😊'''
    }
}

# Mensaje de bienvenida
MENSAJE_BIENVENIDA = '''🤖 **¡Hola! Soy el asistente virtual de Nexa Constructora**

🏗️ Somos expertos en construcción y remodelación en Buenos Aires.

📋 **¿En qué puedo ayudarte?**

1️⃣ **Horarios de atención** - Escribe "horario"
2️⃣ **Precios y servicios** - Escribe "precio"  
3️⃣ **Ubicación y zonas** - Escribe "ubicacion"
4️⃣ **Contacto directo** - Escribe "contacto"
5️⃣ **Nuestros servicios** - Escribe "servicios"

💡 **O simplemente cuéntame tu proyecto y te ayudo personalmente.**

¿Qué te gustaría saber? 😊'''

# Mensaje de transferencia a agente
MENSAJE_TRANSFERENCIA = '''🔄 **Conectándote con un agente humano...**

⏳ **Tiempo de espera estimado**: 2-5 minutos

👨‍💼 **Mientras tanto, puedes**:
• Revisar nuestros proyectos en: https://nexaconstructora.com.ar
• Dejar tu consulta y te responderemos por WhatsApp

📞 **Si es urgente, llama directamente**: +54 9 11 1234-5678

¡Gracias por tu paciencia! 🙏'''

def get_response_for_message(message):
    """
    Obtener respuesta automática basada en el mensaje
    """
    message_lower = message.lower()
    
    # Buscar coincidencias por palabras clave
    for key, config in RESPUESTAS_AUTOMATICAS.items():
        for palabra in config['palabras_clave']:
            if palabra in message_lower:
                return config['respuesta']
    
    # Si no encuentra coincidencias, retornar None para usar GPT
    return None

def is_transfer_request(message):
    """
    Verificar si el usuario quiere hablar con un agente humano
    """
    transfer_keywords = ['agente', 'humano', 'persona', 'operador', 'representante']
    message_lower = message.lower()
    
    return any(keyword in message_lower for keyword in transfer_keywords)
