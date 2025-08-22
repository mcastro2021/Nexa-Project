import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv
import json
from typing import List, Dict, Optional
import sqlite3
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nexa_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NexaWhatsAppBot:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_config()
        self.setup_database()
        self.setup_routes()
        
    def setup_config(self):
        """Configurar credenciales y configuraciones"""
        # Configuración Twilio
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_from = os.getenv('WHATSAPP_FROM')
        
        if not all([self.account_sid, self.auth_token, self.whatsapp_from]):
            raise ValueError("Faltan variables de entorno de Twilio")
        
        self.client = Client(self.account_sid, self.auth_token)
        
        # Configuración OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("Falta API key de OpenAI")
        
        openai.api_key = self.openai_api_key
        
        # Configuración de la aplicación
        self.contactos = self.load_contactos()
        self.respuestas_bot = self.load_respuestas_bot()
        self.conversation_history = {}
        
    def load_contactos(self) -> List[str]:
        """Cargar lista de contactos desde archivo o variable de entorno"""
        contactos_env = os.getenv('WHATSAPP_CONTACTOS')
        if contactos_env:
            return [contacto.strip() for contacto in contactos_env.split(',')]
        
        # Contactos por defecto
        return ['whatsapp:+5491111111111', 'whatsapp:+5492222222222']
    
    def load_respuestas_bot(self) -> Dict[str, str]:
        """Cargar respuestas automáticas"""
        return {
            'horario': '🕐 Nuestro horario de atención es de 9:00 a 18:00hs de lunes a viernes.',
            'precio': '💰 El precio de nuestro servicio es $1000. ¿Te gustaría conocer nuestros planes?',
            'ubicacion': '📍 Estamos ubicados en Av. Siempre Viva 123, Ciudad. ¿Necesitas indicaciones?',
            'contacto': '📞 Puedes contactarnos al +54 9 11 1234-5678 o por email: info@nexa.com',
            'servicios': '🛠️ Ofrecemos: Desarrollo web, Apps móviles, Consultoría IT, Soporte técnico',
            'ayuda': '🤖 Comandos disponibles:\n• horario\n• precio\n• ubicacion\n• contacto\n• servicios'
        }
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.db_path = 'nexa_bot.db'
        with self.get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    escalated BOOLEAN DEFAULT FALSE
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE NOT NULL,
                    name TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    @contextmanager
    def get_db_connection(self):
        """Context manager para conexiones de base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def setup_routes(self):
        """Configurar rutas de la aplicación"""
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            return self.handle_webhook()
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
        
        @self.app.route('/stats', methods=['GET'])
        def get_stats():
            return self.get_statistics()
        
        @self.app.route('/send-message', methods=['POST'])
        def send_message():
            return self.send_bulk_message()
    
    def handle_webhook(self):
        """Manejar mensajes entrantes de WhatsApp"""
        try:
            incoming_msg = request.values.get('Body', '').strip()
            from_number = request.values.get('From', '')
            
            if not incoming_msg:
                return self.create_response("No se recibió mensaje")
            
            logger.info(f"Mensaje recibido de {from_number}: {incoming_msg}")
            
            # Guardar mensaje en base de datos
            self.save_conversation(from_number, incoming_msg, "")
            
            # Procesar mensaje
            response_text = self.process_message(incoming_msg, from_number)
            
            # Crear respuesta TwiML
            resp = MessagingResponse()
            msg = resp.message()
            msg.body(response_text)
            
            # Guardar respuesta en base de datos
            self.save_conversation(from_number, incoming_msg, response_text)
            
            return str(resp)
            
        except Exception as e:
            logger.error(f"Error en webhook: {e}")
            return self.create_response("Lo siento, hubo un error. Inténtalo de nuevo.")
    
    def process_message(self, message: str, from_number: str) -> str:
        """Procesar mensaje y generar respuesta"""
        message_lower = message.lower()
        
        # Verificar respuestas automáticas
        for clave, respuesta in self.respuestas_bot.items():
            if clave in message_lower:
                return respuesta
        
        # Usar GPT para respuestas complejas
        gpt_response = self.responder_con_gpt(message, from_number)
        if gpt_response:
            return gpt_response
        
        # Respuesta por defecto
        return ("No entendí tu consulta. Escribe 'ayuda' para ver las opciones disponibles "
                "o te conectaremos con un agente humano.")
    
    def responder_con_gpt(self, pregunta: str, from_number: str) -> Optional[str]:
        """Usar GPT para generar respuestas inteligentes"""
        try:
            # Obtener historial de conversación
            conversation_history = self.get_conversation_history(from_number)
            
            messages = [
                {
                    "role": "system", 
                    "content": """Eres un asistente virtual de Nexa, una empresa de desarrollo de software. 
                    Responde de manera amigable y profesional. Si no puedes ayudar, sugiere contactar a un agente humano.
                    Mantén las respuestas concisas (máximo 150 palabras)."""
                }
            ]
            
            # Agregar historial de conversación
            for msg in conversation_history[-5:]:  # Últimos 5 mensajes
                messages.append({"role": "user", "content": msg['message']})
                messages.append({"role": "assistant", "content": msg['response']})
            
            messages.append({"role": "user", "content": pregunta})
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error con GPT: {e}")
            return None
    
    def get_conversation_history(self, phone_number: str) -> List[Dict]:
        """Obtener historial de conversación de un número"""
        with self.get_db_connection() as conn:
            cursor = conn.execute('''
                SELECT message, response FROM conversations 
                WHERE phone_number = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', (phone_number,))
            return [dict(row) for row in cursor.fetchall()]
    
    def save_conversation(self, phone_number: str, message: str, response: str):
        """Guardar conversación en base de datos"""
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO conversations (phone_number, message, response)
                    VALUES (?, ?, ?)
                ''', (phone_number, message, response))
        except Exception as e:
            logger.error(f"Error guardando conversación: {e}")
    
    def create_response(self, message: str) -> str:
        """Crear respuesta TwiML simple"""
        resp = MessagingResponse()
        resp.message(message)
        return str(resp)
    
    def send_bulk_message(self):
        """Enviar mensaje a múltiples contactos"""
        try:
            data = request.get_json()
            message = data.get('message', '')
            contacts = data.get('contacts', self.contactos)
            
            if not message:
                return jsonify({'error': 'Mensaje requerido'}), 400
            
            sent_count = 0
            for numero in contacts:
                try:
                    self.client.messages.create(
                        body=message,
                        from_=self.whatsapp_from,
                        to=numero
                    )
                    sent_count += 1
                    logger.info(f"Mensaje enviado a {numero}")
                except Exception as e:
                    logger.error(f"Error enviando a {numero}: {e}")
            
            return jsonify({
                'success': True,
                'sent_count': sent_count,
                'total_contacts': len(contacts)
            })
            
        except Exception as e:
            logger.error(f"Error en envío masivo: {e}")
            return jsonify({'error': str(e)}), 500
    
    def get_statistics(self):
        """Obtener estadísticas del bot"""
        try:
            with self.get_db_connection() as conn:
                # Total de conversaciones
                total_conversations = conn.execute(
                    'SELECT COUNT(*) as count FROM conversations'
                ).fetchone()['count']
                
                # Conversaciones hoy
                today_conversations = conn.execute('''
                    SELECT COUNT(*) as count FROM conversations 
                    WHERE DATE(timestamp) = DATE('now')
                ''').fetchone()['count']
                
                # Contactos únicos
                unique_contacts = conn.execute('''
                    SELECT COUNT(DISTINCT phone_number) as count FROM conversations
                ''').fetchone()['count']
                
                return jsonify({
                    'total_conversations': total_conversations,
                    'today_conversations': today_conversations,
                    'unique_contacts': unique_contacts,
                    'bot_responses': len(self.respuestas_bot)
                })
                
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return jsonify({'error': str(e)}), 500
    
    def send_welcome_message(self, contacts: List[str] = None):
        """Enviar mensaje de bienvenida"""
        if contacts is None:
            contacts = self.contactos
        
        welcome_message = """🤖 ¡Hola! Soy el asistente virtual de Nexa.

¿En qué puedo ayudarte hoy?

📋 Opciones disponibles:
1️⃣ Horario de atención
2️⃣ Precios y servicios
3️⃣ Ubicación
4️⃣ Contacto directo
5️⃣ Nuestros servicios

Escribe 'ayuda' para ver todos los comandos disponibles."""

        for numero in contacts:
            try:
                self.client.messages.create(
                    from_=self.whatsapp_from,
                    to=numero,
                    body=welcome_message
                )
                logger.info(f"Mensaje de bienvenida enviado a {numero}")
            except Exception as e:
                logger.error(f"Error enviando bienvenida a {numero}: {e}")
    
    def run(self, debug: bool = False, port: int = 5000):
        """Ejecutar la aplicación Flask"""
        logger.info(f"Iniciando Nexa WhatsApp Bot en puerto {port}")
        self.app.run(debug=debug, port=port, host='0.0.0.0')

if __name__ == '__main__':
    try:
        bot = NexaWhatsAppBot()
        # Enviar mensaje de bienvenida al iniciar (opcional)
        # bot.send_welcome_message()
        bot.run(debug=True)
    except Exception as e:
        logger.error(f"Error iniciando bot: {e}")
        exit(1)
