#!/usr/bin/env python3
"""
Gestor de Leads para Nexa Constructora
Sistema especializado para seguimiento de clientes potenciales y reenvío de mensajes
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import json
import re
from models import db, Lead, LeadStatus, LeadSource, Message, MessageTemplate, Campaign, CampaignResult, Interaction
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger(__name__)

class NexaLeadManager:
    def __init__(self, app=None):
        self.app = app
        self.twilio_client = None
        self.scheduler = BackgroundScheduler()
        self.setup_twilio()
        self.setup_scheduler()
        
    def setup_twilio(self):
        """Configurar cliente de Twilio"""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            if account_sid and auth_token:
                self.twilio_client = Client(account_sid, auth_token)
                self.whatsapp_from = os.getenv('WHATSAPP_FROM')
                logger.info("Twilio configurado correctamente")
            else:
                logger.warning("Credenciales de Twilio no encontradas")
        except Exception as e:
            logger.error(f"Error configurando Twilio: {e}")
    
    def setup_scheduler(self):
        """Configurar programador de tareas"""
        try:
            self.scheduler.start()
            # Programar tareas diarias
            self.scheduler.add_job(
                self.send_follow_up_reminders,
                'cron',
                hour=9,
                minute=0,
                id='follow_up_reminders'
            )
            self.scheduler.add_job(
                self.send_weekly_summary,
                'cron',
                day_of_week='mon',
                hour=8,
                minute=0,
                id='weekly_summary'
            )
            logger.info("Programador de tareas configurado")
        except Exception as e:
            logger.error(f"Error configurando programador: {e}")
    
    def create_lead_from_website(self, phone_number: str, name: str = None, 
                                email: str = None, company: str = None, 
                                interest_details: str = None) -> Lead:
        """Crear lead desde el sitio web de Nexa"""
        try:
            # Verificar si el lead ya existe
            existing_lead = Lead.query.filter_by(phone_number=phone_number).first()
            if existing_lead:
                logger.info(f"Lead existente encontrado: {phone_number}")
                return existing_lead
            
            lead = Lead(
                phone_number=phone_number,
                name=name,
                email=email,
                company=company,
                source=LeadSource.WEBSITE,
                status=LeadStatus.NUEVO,
                notes=interest_details
            )
            
            db.session.add(lead)
            db.session.commit()
            
            logger.info(f"Nuevo lead creado: {phone_number}")
            
            # Enviar mensaje de bienvenida automático
            self.send_welcome_message(lead)
            
            return lead
            
        except Exception as e:
            logger.error(f"Error creando lead: {e}")
            db.session.rollback()
            return None
    
    def send_welcome_message(self, lead: Lead) -> bool:
        """Enviar mensaje de bienvenida a un nuevo lead"""
        try:
            template = MessageTemplate.query.filter_by(
                category='welcome',
                is_active=True
            ).first()
            
            if not template:
                # Plantilla por defecto
                message_content = f"""🏗️ ¡Hola! Gracias por tu interés en Nexa Constructora.

Somos especialistas en construcción y desarrollo inmobiliario con más de 10 años de experiencia.

¿En qué proyecto estás pensando? Te ayudo a hacerlo realidad.

📞 Llámanos: +54 9 11 1234-5678
🌐 Visítanos: https://nexaconstructora.com.ar

Saludos,
Equipo Nexa Constructora"""
            else:
                message_content = self.format_template(template.content, lead)
            
            return self.send_whatsapp_message(lead.phone_number, message_content, lead.id)
            
        except Exception as e:
            logger.error(f"Error enviando mensaje de bienvenida: {e}")
            return False
    
    def send_follow_up_message(self, lead: Lead, template_category: str = 'follow_up') -> bool:
        """Enviar mensaje de seguimiento"""
        try:
            template = MessageTemplate.query.filter_by(
                category=template_category,
                is_active=True
            ).first()
            
            if not template:
                # Plantilla por defecto de seguimiento
                message_content = f"""🏗️ Hola {lead.name or 'estimado cliente'},

Esperamos que estés bien. Te escribimos para recordarte que estamos aquí para ayudarte con tu proyecto de construcción.

¿Has tenido tiempo de revisar nuestras propuestas? ¿Tienes alguna pregunta?

Estamos disponibles para una consulta gratuita.

Saludos,
Equipo Nexa Constructora"""
            else:
                message_content = self.format_template(template.content, lead)
            
            success = self.send_whatsapp_message(lead.phone_number, message_content, lead.id)
            
            if success:
                # Actualizar estado del lead
                lead.status = LeadStatus.CONTACTADO
                lead.last_contact_date = datetime.utcnow()
                lead.next_follow_up = datetime.utcnow() + timedelta(days=3)
                db.session.commit()
                
                # Crear interacción
                create_interaction(
                    lead.id,
                    'whatsapp_follow_up',
                    f'Mensaje de seguimiento enviado: {template_category}',
                    'sent'
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error enviando mensaje de seguimiento: {e}")
            return False
    
    def send_whatsapp_message(self, phone_number: str, message: str, lead_id: int = None) -> bool:
        """Enviar mensaje de WhatsApp"""
        try:
            if not self.twilio_client:
                logger.error("Cliente de Twilio no configurado")
                return False
            
            # Formatear número de teléfono
            formatted_number = self.format_phone_number(phone_number)
            
            # Enviar mensaje
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=f"whatsapp:{formatted_number}"
            )
            
            # Guardar mensaje en base de datos
            if lead_id:
                db_message = Message(
                    lead_id=lead_id,
                    message_type='sent',
                    content=message,
                    status='sent',
                    twilio_sid=message_obj.sid
                )
                db.session.add(db_message)
                db.session.commit()
            
            logger.info(f"Mensaje enviado a {formatted_number}: {message_obj.sid}")
            return True
            
        except TwilioException as e:
            logger.error(f"Error de Twilio: {e}")
            return False
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False
    
    def format_phone_number(self, phone_number: str) -> str:
        """Formatear número de teléfono para Twilio"""
        # Remover caracteres no numéricos
        clean_number = re.sub(r'[^\d]', '', phone_number)
        
        # Agregar código de país si no está presente
        if clean_number.startswith('54'):
            return clean_number
        elif clean_number.startswith('9') and len(clean_number) == 10:
            return f"54{clean_number}"
        elif len(clean_number) == 10:
            return f"54{clean_number}"
        else:
            return clean_number
    
    def format_template(self, template_content: str, lead: Lead) -> str:
        """Formatear plantilla con datos del lead"""
        replacements = {
            '{name}': lead.name or 'estimado cliente',
            '{company}': lead.company or 'tu empresa',
            '{phone}': lead.phone_number,
            '{email}': lead.email or 'tu email',
            '{date}': datetime.now().strftime('%d/%m/%Y'),
            '{website}': 'https://nexaconstructora.com.ar'
        }
        
        formatted_content = template_content
        for placeholder, value in replacements.items():
            formatted_content = formatted_content.replace(placeholder, str(value))
        
        return formatted_content
    
    def get_leads_needing_follow_up(self) -> List[Lead]:
        """Obtener leads que necesitan seguimiento"""
        today = datetime.utcnow()
        return Lead.query.filter(
            Lead.next_follow_up <= today,
            Lead.status.in_([LeadStatus.NUEVO, LeadStatus.CONTACTADO, LeadStatus.INTERESADO])
        ).all()
    
    def send_follow_up_reminders(self):
        """Enviar recordatorios de seguimiento programados"""
        try:
            leads = self.get_leads_needing_follow_up()
            logger.info(f"Enviando recordatorios a {len(leads)} leads")
            
            for lead in leads:
                self.send_follow_up_message(lead, 'reminder')
                
        except Exception as e:
            logger.error(f"Error en recordatorios automáticos: {e}")
    
    def send_weekly_summary(self):
        """Enviar resumen semanal de leads"""
        try:
            # Obtener estadísticas de la semana
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            new_leads = Lead.query.filter(
                Lead.created_at >= week_ago,
                Lead.source == LeadSource.WEBSITE
            ).count()
            
            converted_leads = Lead.query.filter(
                Lead.status == LeadStatus.CONVERTIDO,
                Lead.updated_at >= week_ago
            ).count()
            
            # Enviar resumen al administrador
            summary_message = f"""📊 Resumen Semanal - Nexa Constructora

Nuevos leads: {new_leads}
Leads convertidos: {converted_leads}
Tasa de conversión: {(converted_leads/new_leads*100) if new_leads > 0 else 0:.1f}%

Revisa el dashboard para más detalles:
https://tu-dominio.com/dashboard"""
            
            # Enviar a número de administrador
            admin_number = os.getenv('ADMIN_WHATSAPP')
            if admin_number:
                self.send_whatsapp_message(admin_number, summary_message)
                
        except Exception as e:
            logger.error(f"Error enviando resumen semanal: {e}")
    
    def create_campaign(self, name: str, template_id: int, target_status: LeadStatus = None,
                       target_source: LeadSource = None, scheduled_date: datetime = None) -> Campaign:
        """Crear una nueva campaña de mensajes"""
        try:
            campaign = Campaign(
                name=name,
                template_id=template_id,
                target_status=target_status,
                target_source=target_source,
                scheduled_date=scheduled_date
            )
            
            db.session.add(campaign)
            db.session.commit()
            
            # Programar campaña si tiene fecha programada
            if scheduled_date:
                self.scheduler.add_job(
                    self.execute_campaign,
                    DateTrigger(run_date=scheduled_date),
                    args=[campaign.id],
                    id=f'campaign_{campaign.id}'
                )
            
            logger.info(f"Campaña creada: {name}")
            return campaign
            
        except Exception as e:
            logger.error(f"Error creando campaña: {e}")
            db.session.rollback()
            return None
    
    def execute_campaign(self, campaign_id: int):
        """Ejecutar una campaña"""
        try:
            campaign = Campaign.query.get(campaign_id)
            if not campaign or not campaign.is_active:
                return
            
            # Obtener leads objetivo
            query = Lead.query
            if campaign.target_status:
                query = query.filter_by(status=campaign.target_status)
            if campaign.target_source:
                query = query.filter_by(source=campaign.target_source)
            
            leads = query.all()
            
            logger.info(f"Ejecutando campaña '{campaign.name}' para {len(leads)} leads")
            
            for lead in leads:
                try:
                    template = MessageTemplate.query.get(campaign.template_id)
                    if template:
                        message_content = self.format_template(template.content, lead)
                        success = self.send_whatsapp_message(lead.phone_number, message_content, lead.id)
                        
                        if success:
                            # Crear resultado de campaña
                            message = Message.query.filter_by(lead_id=lead.id).order_by(Message.created_at.desc()).first()
                            if message:
                                create_campaign_result(campaign.id, lead.id, message.id)
                
                except Exception as e:
                    logger.error(f"Error procesando lead {lead.id} en campaña: {e}")
                    
        except Exception as e:
            logger.error(f"Error ejecutando campaña {campaign_id}: {e}")
    
    def get_lead_analytics(self, days: int = 30) -> Dict:
        """Obtener análisis de leads"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Obtener todos los leads (sin filtro de fecha por ahora)
            all_leads = Lead.query.all()
            
            # Leads por estado
            status_counts = {}
            for lead in all_leads:
                status = lead.status.value if hasattr(lead.status, 'value') else str(lead.status)
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Leads por fuente
            source_counts = {}
            for lead in all_leads:
                source = lead.source.value if hasattr(lead.source, 'value') else str(lead.source)
                source_counts[source] = source_counts.get(source, 0) + 1
            
            # Conversiones
            conversions = sum(1 for lead in all_leads if lead.status == LeadStatus.CONVERTIDO)
            
            # Total de leads
            total_leads = len(all_leads)
            
            return {
                'status_distribution': status_counts,
                'source_distribution': source_counts,
                'conversion_rate': (conversions / total_leads * 100) if total_leads > 0 else 0,
                'total_leads': total_leads,
                'conversions': conversions
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo analytics: {e}")
            return {
                'status_distribution': {},
                'source_distribution': {},
                'conversion_rate': 0,
                'total_leads': 0,
                'conversions': 0
            }
    
    def import_leads_from_csv(self, csv_file_path: str) -> Tuple[int, int]:
        """Importar leads desde archivo CSV usando Python nativo"""
        import csv
        
        try:
            imported = 0
            skipped = 0
            
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Verificar si el lead ya existe
                        phone_number = str(row.get('phone_number', '')).strip()
                        if not phone_number:
                            skipped += 1
                            continue
                            
                        existing = Lead.query.filter_by(phone_number=phone_number).first()
                        if existing:
                            skipped += 1
                            continue
                        
                        lead = Lead(
                            phone_number=phone_number,
                            name=row.get('name', '').strip(),
                            email=row.get('email', '').strip(),
                            company=row.get('company', '').strip(),
                            source=LeadSource.WEBSITE,
                            status=LeadStatus.NUEVO,
                            notes=row.get('notes', 'Importado desde CSV')
                        )
                        
                        db.session.add(lead)
                        imported += 1
                        
                    except Exception as e:
                        logger.error(f"Error importando fila: {e}")
                        skipped += 1
            
            db.session.commit()
            logger.info(f"Importación completada: {imported} importados, {skipped} omitidos")
            return imported, skipped
            
        except Exception as e:
            logger.error(f"Error importando CSV: {e}")
            db.session.rollback()
            return 0, 0

# Instancia global del gestor de leads
lead_manager = NexaLeadManager()
