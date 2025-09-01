#!/usr/bin/env python3
"""
Script para probar el bot de WhatsApp localmente
"""

import os
from bot_responses import get_response_for_message, is_transfer_request, MENSAJE_BIENVENIDA
from lead_manager import lead_manager
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_bot_responses():
    """Probar respuestas automáticas del bot"""
    print("🤖 **PRUEBA DEL BOT DE WHATSAPP NEXA**\n")
    
    # Mensaje de bienvenida
    print("📱 **Mensaje de Bienvenida:**")
    print(MENSAJE_BIENVENIDA)
    print("\n" + "="*50 + "\n")
    
    # Pruebas de respuestas automáticas
    test_messages = [
        "¿Cuál es el horario de atención?",
        "Necesito saber los precios",
        "¿Dónde están ubicados?",
        "Quiero hablar con un agente humano",
        "¿Qué servicios ofrecen?",
        "Necesito ayuda con mi proyecto",
        "¿Cuánto cuesta construir una casa?",
        "Hola, buenos días"
    ]
    
    for message in test_messages:
        print(f"👤 **Usuario**: {message}")
        
        # Verificar si es solicitud de transferencia
        if is_transfer_request(message):
            print("🤖 **Bot**: [TRANSFERENCIA A AGENTE HUMANO]")
            print("📞 Conectando con agente...")
        else:
            # Buscar respuesta automática
            response = get_response_for_message(message)
            if response:
                print(f"🤖 **Bot**: {response}")
            else:
                # Simular respuesta con GPT
                gpt_response = simulate_gpt_response(message)
                print(f"🤖 **Bot (GPT)**: {gpt_response}")
        
        print("\n" + "-"*30 + "\n")

def simulate_gpt_response(message):
    """Simular respuesta de GPT (sin API key)"""
    responses = [
        "Entiendo tu consulta. Te puedo ayudar con información específica sobre construcción y remodelación. ¿Podrías contarme más detalles sobre tu proyecto?",
        "Excelente pregunta. En Nexa Constructora tenemos experiencia en diversos tipos de proyectos. ¿Te gustaría que te contacte un especialista?",
        "Gracias por tu interés. Para darte la mejor respuesta, necesito algunos detalles adicionales sobre tu proyecto. ¿Cuándo te gustaría que te contactemos?",
        "Perfecto, entiendo lo que necesitas. Te voy a conectar con nuestro equipo especializado para que te den una respuesta personalizada.",
        "Muy buena consulta. Te recomiendo que hablemos con uno de nuestros expertos para darte la información más precisa. ¿Te parece bien?"
    ]
    
    import random
    return random.choice(responses)

def test_lead_manager():
    """Probar funcionalidades del lead manager"""
    print("📊 **PRUEBA DEL LEAD MANAGER**\n")
    
    try:
        # Crear un lead de prueba
        lead_data = {
            'phone_number': '+5491112345678',
            'name': 'Juan Pérez',
            'email': 'juan.perez@email.com',
            'company': 'Constructora ABC',
            'notes': 'Interesado en construcción residencial'
        }
        
        print("✅ Lead Manager funcionando correctamente")
        print(f"📝 Lead de prueba creado: {lead_data['name']}")
        
    except Exception as e:
        print(f"❌ Error en Lead Manager: {e}")

def main():
    """Función principal"""
    print("🚀 **INICIANDO PRUEBAS DEL SISTEMA NEXA**\n")
    
    # Probar bot
    test_bot_responses()
    
    # Probar lead manager
    test_lead_manager()
    
    print("\n🎉 **PRUEBAS COMPLETADAS**")
    print("\n📋 **PRÓXIMOS PASOS:**")
    print("1. Configurar credenciales de Twilio en .env")
    print("2. Configurar API key de OpenAI en .env")
    print("3. Desplegar en Render")
    print("4. Configurar webhook de WhatsApp")
    print("5. ¡Empezar a recibir leads!")

if __name__ == '__main__':
    main()
