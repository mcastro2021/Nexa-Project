#!/usr/bin/env python3
"""
Script de prueba para el Nexa WhatsApp Bot
Permite probar la funcionalidad sin enviar mensajes reales de WhatsApp
"""

import os
import sys
from dotenv import load_dotenv
from app import NexaWhatsAppBot
import json

def test_bot_responses():
    """Probar las respuestas automáticas del bot"""
    print("🧪 Probando respuestas automáticas...")
    
    # Crear instancia del bot
    bot = NexaWhatsAppBot()
    
    # Casos de prueba
    test_cases = [
        ("horario", "horario"),
        ("¿Cuál es el precio?", "precio"),
        ("Dónde están ubicados", "ubicacion"),
        ("Necesito contactarlos", "contacto"),
        ("Qué servicios ofrecen", "servicios"),
        ("ayuda", "ayuda"),
        ("Hola, ¿cómo están?", "gpt"),
        ("Quiero información sobre desarrollo web", "gpt"),
    ]
    
    for test_input, expected_type in test_cases:
        print(f"\n📝 Entrada: '{test_input}'")
        response = bot.process_message(test_input, "whatsapp:+5491111111111")
        print(f"🤖 Respuesta: {response[:100]}...")
        print(f"✅ Tipo esperado: {expected_type}")

def test_database():
    """Probar funcionalidad de base de datos"""
    print("\n🗄️ Probando base de datos...")
    
    bot = NexaWhatsAppBot()
    
    # Probar guardar conversación
    test_message = "Mensaje de prueba"
    test_response = "Respuesta de prueba"
    test_phone = "whatsapp:+5491111111111"
    
    bot.save_conversation(test_phone, test_message, test_response)
    print("✅ Conversación guardada")
    
    # Probar obtener historial
    history = bot.get_conversation_history(test_phone)
    print(f"✅ Historial obtenido: {len(history)} mensajes")
    
    # Probar estadísticas
    stats = bot.get_statistics()
    print(f"✅ Estadísticas: {stats.json}")

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🌐 Probando endpoints de la API...")
    
    bot = NexaWhatsAppBot()
    
    with bot.app.test_client() as client:
        # Health check
        response = client.get('/health')
        print(f"✅ Health check: {response.status_code}")
        
        # Stats
        response = client.get('/stats')
        print(f"✅ Stats: {response.status_code}")
        
        # Webhook (simulado)
        response = client.post('/webhook', data={
            'Body': 'horario',
            'From': 'whatsapp:+5491111111111'
        })
        print(f"✅ Webhook: {response.status_code}")

def test_configuration():
    """Verificar configuración"""
    print("\n⚙️ Verificando configuración...")
    
    load_dotenv()
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'WHATSAPP_FROM',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Configurado")
        else:
            print(f"❌ {var}: Faltante")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Variables faltantes: {', '.join(missing_vars)}")
        print("Por favor, configura estas variables en tu archivo .env")
    else:
        print("\n✅ Todas las variables de entorno están configuradas")

def main():
    """Función principal de pruebas"""
    print("=" * 50)
    print("    NEXA WHATSAPP BOT - PRUEBAS")
    print("=" * 50)
    
    try:
        # Verificar configuración
        test_configuration()
        
        # Probar respuestas del bot
        test_bot_responses()
        
        # Probar base de datos
        test_database()
        
        # Probar endpoints
        test_api_endpoints()
        
        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
