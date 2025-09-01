#!/usr/bin/env python3
"""
Funcionalidades de Inteligencia Artificial para Nexa Lead Manager
Sistema inteligente para optimizar la gestión de leads y campañas
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import re
from models import db, Lead, LeadStatus, LeadSource, Message, MessageTemplate, Campaign, CampaignResult, Interaction

logger = logging.getLogger(__name__)

class NexaAI:
    def __init__(self):
        self.openai_client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Configurar cliente de OpenAI"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                self.openai_client = openai
                logger.info("OpenAI configurado correctamente")
            else:
                logger.warning("API key de OpenAI no encontrada")
        except ImportError:
            logger.warning("OpenAI no está disponible")
        except Exception as e:
            logger.error(f"Error configurando OpenAI: {e}")
    
    def analyze_lead_intent(self, message_content: str, lead_data: Dict) -> Dict:
        """Analizar la intención del lead usando IA"""
        try:
            if not self.openai_client:
                return self._fallback_intent_analysis(message_content, lead_data)
            
            prompt = f"""
            Analiza la intención del siguiente mensaje de un lead potencial para una constructora:
            
            Mensaje: "{message_content}"
            Lead: {lead_data.get('name', 'Sin nombre')} - {lead_data.get('company', 'Sin empresa')}
            
            Clasifica la intención en una de estas categorías:
            1. CONSULTA_GENERAL - Preguntas generales sobre servicios
            2. INTERESADO_PROYECTO - Muestra interés en un proyecto específico
            3. SOLICITA_PRESUPUESTO - Pide cotización o presupuesto
            4. AGENDA_CITA - Quiere programar una reunión
            5. COMPARACION - Compara con otras empresas
            6. NO_INTERESADO - No está interesado
            
            También proporciona:
            - Nivel de urgencia (1-5)
            - Probabilidad de conversión (1-5)
            - Acción recomendada
            - Respuesta sugerida
            
            Responde en formato JSON.
            """
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error analizando intención: {e}")
            return self._fallback_intent_analysis(message_content, lead_data)
    
    def _fallback_intent_analysis(self, message_content: str, lead_data: Dict) -> Dict:
        """Análisis de intención sin IA como fallback"""
        content_lower = message_content.lower()
        
        # Análisis basado en palabras clave
        intent = "CONSULTA_GENERAL"
        urgency = 3
        conversion_prob = 3
        action = "Responder consulta general"
        
        if any(word in content_lower for word in ['precio', 'costo', 'presupuesto', 'cotización']):
            intent = "SOLICITA_PRESUPUESTO"
            urgency = 4
            conversion_prob = 4
            action = "Enviar cotización personalizada"
        
        elif any(word in content_lower for word in ['cita', 'reunión', 'visita', 'agenda']):
            intent = "AGENDA_CITA"
            urgency = 5
            conversion_prob = 5
            action = "Agendar cita inmediatamente"
        
        elif any(word in content_lower for word in ['proyecto', 'construir', 'edificio', 'casa']):
            intent = "INTERESADO_PROYECTO"
            urgency = 4
            conversion_prob = 4
            action = "Solicitar detalles del proyecto"
        
        elif any(word in content_lower for word in ['otra empresa', 'competencia', 'comparar']):
            intent = "COMPARACION"
            urgency = 3
            conversion_prob = 3
            action = "Destacar ventajas competitivas"
        
        return {
            'intent': intent,
            'urgency': urgency,
            'conversion_probability': conversion_prob,
            'recommended_action': action,
            'suggested_response': self._generate_suggested_response(intent, lead_data)
        }
    
    def _generate_suggested_response(self, intent: str, lead_data: Dict) -> str:
        """Generar respuesta sugerida basada en la intención"""
        name = lead_data.get('name', 'Estimado cliente')
        
        responses = {
            'CONSULTA_GENERAL': f"¡Hola {name}! Gracias por tu consulta. Somos Nexa Constructora, especialistas en construcción y desarrollo inmobiliario. ¿En qué podemos ayudarte específicamente?",
            'SOLICITA_PRESUPUESTO': f"Hola {name}, entiendo que necesitas un presupuesto. Para darte la mejor cotización, necesito algunos detalles de tu proyecto. ¿Podrías contarme más sobre lo que tienes en mente?",
            'AGENDA_CITA': f"¡Perfecto {name}! Me encantaría agendar una cita para discutir tu proyecto en detalle. ¿Qué día y horario te resulta más conveniente?",
            'INTERESADO_PROYECTO': f"Excelente {name}, veo que tienes un proyecto en mente. ¿Podrías describirme qué tipo de construcción estás pensando? Así podré asesorarte mejor.",
            'COMPARACION': f"Hola {name}, entiendo que estás evaluando opciones. En Nexa Constructora nos destacamos por nuestra calidad, experiencia y compromiso con el cliente. ¿Te gustaría conocer algunos de nuestros proyectos realizados?",
            'NO_INTERESADO': f"Entiendo {name}. Si en el futuro cambias de opinión o conoces a alguien que necesite nuestros servicios, no dudes en contactarnos. ¡Que tengas un excelente día!"
        }
        
        return responses.get(intent, responses['CONSULTA_GENERAL'])
    
    def predict_lead_conversion(self, lead: Lead) -> Dict:
        """Predecir probabilidad de conversión del lead"""
        try:
            # Análisis basado en múltiples factores
            factors = {
                'source_score': self._get_source_score(lead.source),
                'interaction_score': self._get_interaction_score(lead.id),
                'response_time_score': self._get_response_time_score(lead),
                'interest_level_score': lead.interest_level / 5.0,
                'company_score': 1.0 if lead.company else 0.5,
                'email_score': 1.0 if lead.email else 0.5
            }
            
            # Calcular score total
            total_score = sum(factors.values()) / len(factors)
            conversion_prob = min(total_score * 100, 95)  # Máximo 95%
            
            # Determinar recomendaciones
            recommendations = self._get_conversion_recommendations(factors, conversion_prob)
            
            return {
                'conversion_probability': round(conversion_prob, 1),
                'factors': factors,
                'recommendations': recommendations,
                'next_best_action': self._get_next_best_action(lead, conversion_prob)
            }
            
        except Exception as e:
            logger.error(f"Error prediciendo conversión: {e}")
            return {'conversion_probability': 50, 'error': str(e)}
    
    def _get_source_score(self, source: LeadSource) -> float:
        """Calcular score basado en la fuente del lead"""
        source_scores = {
            LeadSource.WEBSITE: 0.8,
            LeadSource.WHATSAPP: 0.9,
            LeadSource.REFERIDO: 0.95,
            LeadSource.REDES_SOCIALES: 0.7,
            LeadSource.EVENTO: 0.85,
            LeadSource.OTRO: 0.6
        }
        return source_scores.get(source, 0.6)
    
    def _get_interaction_score(self, lead_id: int) -> float:
        """Calcular score basado en interacciones"""
        interactions = Interaction.query.filter_by(lead_id=lead_id).count()
        if interactions == 0:
            return 0.3
        elif interactions == 1:
            return 0.6
        elif interactions <= 3:
            return 0.8
        else:
            return 0.9
    
    def _get_response_time_score(self, lead: Lead) -> float:
        """Calcular score basado en tiempo de respuesta"""
        if not lead.last_contact_date:
            return 0.2
        
        days_since_contact = (datetime.utcnow() - lead.last_contact_date).days
        
        if days_since_contact <= 1:
            return 1.0
        elif days_since_contact <= 3:
            return 0.8
        elif days_since_contact <= 7:
            return 0.6
        elif days_since_contact <= 14:
            return 0.4
        else:
            return 0.2
    
    def _get_conversion_recommendations(self, factors: Dict, conversion_prob: float) -> List[str]:
        """Generar recomendaciones para mejorar conversión"""
        recommendations = []
        
        if factors['response_time_score'] < 0.5:
            recommendations.append("Contactar al lead inmediatamente")
        
        if factors['interaction_score'] < 0.5:
            recommendations.append("Aumentar frecuencia de interacciones")
        
        if factors['interest_level_score'] < 0.6:
            recommendations.append("Enviar contenido de valor para aumentar interés")
        
        if conversion_prob < 30:
            recommendations.append("Revisar estrategia de seguimiento")
        elif conversion_prob < 60:
            recommendations.append("Personalizar mensajes según intereses")
        else:
            recommendations.append("Mantener momentum actual")
        
        return recommendations
    
    def _get_next_best_action(self, lead: Lead, conversion_prob: float) -> str:
        """Determinar la siguiente mejor acción"""
        if conversion_prob >= 80:
            return "Solicitar cierre de venta"
        elif conversion_prob >= 60:
            return "Agendar cita de presentación"
        elif conversion_prob >= 40:
            return "Enviar propuesta personalizada"
        elif conversion_prob >= 20:
            return "Enviar contenido educativo"
        else:
            return "Revisar si el lead está calificado"
    
    def generate_personalized_message(self, lead: Lead, template_type: str) -> str:
        """Generar mensaje personalizado usando IA"""
        try:
            if not self.openai_client:
                return self._generate_fallback_message(lead, template_type)
            
            prompt = f"""
            Genera un mensaje personalizado de WhatsApp para un lead de construcción:
            
            Lead: {lead.name} - {lead.company or 'Sin empresa'}
            Estado: {lead.status.value}
            Fuente: {lead.source.value}
            Nivel de interés: {lead.interest_level}/5
            
            Tipo de mensaje: {template_type}
            
            El mensaje debe ser:
            - Personal y amigable
            - Relevante para su situación
            - Incluir call-to-action claro
            - Máximo 3 párrafos
            - Usar emojis apropiados
            
            Responde solo con el mensaje, sin formato adicional.
            """
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generando mensaje personalizado: {e}")
            return self._generate_fallback_message(lead, template_type)
    
    def _generate_fallback_message(self, lead: Lead, template_type: str) -> str:
        """Generar mensaje sin IA como fallback"""
        name = lead.name or "Estimado cliente"
        
        messages = {
            'welcome': f"¡Hola {name}! 👋\n\nGracias por tu interés en Nexa Constructora. Somos especialistas en construcción y desarrollo inmobiliario.\n\n¿En qué proyecto estás pensando? Estamos aquí para ayudarte.",
            'follow_up': f"Hola {name}, ¿cómo estás?\n\nTe escribo para hacer seguimiento de tu interés en nuestros servicios de construcción.\n\n¿Te gustaría que conversemos sobre tu proyecto?",
            'offer': f"¡{name}! 🏗️\n\nTenemos una oferta especial para ti: 15% de descuento en proyectos de construcción que se inicien este mes.\n\n¿Te interesa aprovechar esta promoción?",
            'reminder': f"Hola {name},\n\nTe recordamos que tenemos una cita programada para discutir tu proyecto de construcción.\n\n¿Confirmas que podemos proceder?"
        }
        
        return messages.get(template_type, messages['welcome'])
    
    def analyze_campaign_performance(self, campaign_id: int) -> Dict:
        """Analizar rendimiento de campaña usando IA"""
        try:
            campaign = Campaign.query.get(campaign_id)
            if not campaign:
                return {'error': 'Campaña no encontrada'}
            
            # Obtener resultados de la campaña
            results = CampaignResult.query.filter_by(campaign_id=campaign_id).all()
            
            if not results:
                return {'error': 'No hay resultados para analizar'}
            
            # Calcular métricas
            total_sent = len(results)
            delivered = sum(1 for r in results if r.status in ['delivered', 'read'])
            read = sum(1 for r in results if r.status == 'read')
            responded = sum(1 for r in results if r.status == 'responded')
            
            delivery_rate = (delivered / total_sent) * 100 if total_sent > 0 else 0
            read_rate = (read / total_sent) * 100 if total_sent > 0 else 0
            response_rate = (responded / total_sent) * 100 if total_sent > 0 else 0
            
            # Análisis de rendimiento
            performance_score = (delivery_rate * 0.3 + read_rate * 0.4 + response_rate * 0.3)
            
            # Recomendaciones
            recommendations = []
            if delivery_rate < 80:
                recommendations.append("Revisar números de teléfono y formato de mensajes")
            if read_rate < 60:
                recommendations.append("Optimizar horarios de envío y contenido de mensajes")
            if response_rate < 20:
                recommendations.append("Mejorar call-to-action y personalización")
            
            return {
                'campaign_id': campaign_id,
                'campaign_name': campaign.name,
                'total_sent': total_sent,
                'delivery_rate': round(delivery_rate, 1),
                'read_rate': round(read_rate, 1),
                'response_rate': round(response_rate, 1),
                'performance_score': round(performance_score, 1),
                'recommendations': recommendations,
                'next_campaign_optimization': self._get_campaign_optimization_suggestions(performance_score)
            }
            
        except Exception as e:
            logger.error(f"Error analizando campaña: {e}")
            return {'error': str(e)}
    
    def _get_campaign_optimization_suggestions(self, performance_score: float) -> List[str]:
        """Obtener sugerencias de optimización de campaña"""
        if performance_score >= 80:
            return ["Mantener estrategia actual", "Escalar a más leads"]
        elif performance_score >= 60:
            return ["A/B testing de mensajes", "Optimizar horarios de envío"]
        elif performance_score >= 40:
            return ["Revisar segmentación", "Mejorar personalización"]
        else:
            return ["Rediseñar campaña completa", "Revisar base de datos de leads"]

# Instancia global de IA
ai_features = NexaAI()
