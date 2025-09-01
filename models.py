from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from enum import Enum
import json

db = SQLAlchemy()

class LeadStatus(Enum):
    NUEVO = "nuevo"
    CONTACTADO = "contactado"
    INTERESADO = "interesado"
    CALIFICADO = "calificado"
    CONVERTIDO = "convertido"
    PERDIDO = "perdido"

class LeadSource(Enum):
    WEBSITE = "website"
    WHATSAPP = "whatsapp"
    REFERIDO = "referido"
    REDES_SOCIALES = "redes_sociales"
    EVENTO = "evento"
    OTRO = "otro"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120))
    company = db.Column(db.String(100))
    status = db.Column(db.Enum(LeadStatus), default=LeadStatus.NUEVO)
    source = db.Column(db.Enum(LeadSource), default=LeadSource.OTRO)
    interest_level = db.Column(db.Integer, default=3)  # 1-5
    notes = db.Column(db.Text)
    next_follow_up = db.Column(db.DateTime)
    last_contact_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    interactions = db.relationship('Interaction', backref='lead', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='lead', lazy=True, cascade='all, delete-orphan')

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # call, email, whatsapp, meeting
    description = db.Column(db.Text)
    outcome = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='outbound')  # inbound, outbound
    status = db.Column(db.String(20), default='pending')  # pending, sent, delivered, read, failed, scheduled
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    campaign_results = db.relationship('CampaignResult', backref='message_ref', lazy=True, cascade='all, delete-orphan')

class MessageTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # welcome, follow_up, reminder, offer
    content = db.Column(db.Text, nullable=False)
    variables = db.Column(db.Text)  # JSON de variables disponibles
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    template_id = db.Column(db.Integer, db.ForeignKey('message_template.id'))
    target_status = db.Column(db.Enum(LeadStatus))
    target_source = db.Column(db.Enum(LeadSource))
    scheduled_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    template = db.relationship('MessageTemplate')
    results = db.relationship('CampaignResult', backref='campaign_ref', lazy=True, cascade='all, delete-orphan')

class CampaignResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, delivered, read, failed
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    
    # Relaciones - Sin backref para evitar conflictos
    # lead = db.relationship('Lead', backref='campaign_results')  # Comentado para evitar conflicto

# Funciones de utilidad para los modelos
def get_leads_by_status(status: LeadStatus):
    """Obtener leads por estado"""
    return Lead.query.filter_by(status=status).all()

def get_leads_needing_follow_up():
    """Obtener leads que necesitan seguimiento"""
    today = datetime.utcnow()
    return Lead.query.filter(
        Lead.next_follow_up <= today,
        Lead.status.in_([LeadStatus.CONTACTADO, LeadStatus.INTERESADO])
    ).all()

def get_leads_by_source(source: LeadSource, days: int = 30):
    """Obtener leads por fuente en los últimos N días"""
    start_date = datetime.utcnow() - timedelta(days=days)
    return Lead.query.filter(
        Lead.source == source,
        Lead.created_at >= start_date
    ).all()

def create_interaction(lead_id: int, interaction_type: str, description: str, outcome: str = None):
    """Crear una nueva interacción"""
    interaction = Interaction(
        lead_id=lead_id,
        interaction_type=interaction_type,
        description=description,
        outcome=outcome
    )
    db.session.add(interaction)
    db.session.commit()
    return interaction

def update_lead_status(lead_id: int, new_status: LeadStatus, notes: str = None):
    """Actualizar el estado de un lead"""
    lead = Lead.query.get(lead_id)
    if lead:
        lead.status = new_status
        lead.last_contact_date = datetime.utcnow()
        if notes:
            lead.notes = notes
        db.session.commit()
        return lead
    return None

def get_message_templates_by_category(category: str):
    """Obtener plantillas de mensaje por categoría"""
    return MessageTemplate.query.filter_by(category=category, is_active=True).all()

def create_campaign_result(campaign_id: int, lead_id: int, message_id: int):
    """Crear resultado de campaña"""
    result = CampaignResult(
        campaign_id=campaign_id,
        lead_id=lead_id,
        message_id=message_id,
        status='pending'
    )
    db.session.add(result)
    db.session.commit()
    return result
