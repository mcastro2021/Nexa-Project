#!/usr/bin/env python3
"""
Script de inicialización para Nexa Lead Manager
Configura la base de datos y crea plantillas por defecto
"""

import os
import sys
from datetime import datetime, timedelta
from models import db, User, Lead, LeadStatus, LeadSource, MessageTemplate, Campaign
from lead_manager import lead_manager
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializar la base de datos"""
    print("🔧 Inicializando base de datos...")
    
    # Crear todas las tablas
    db.create_all()
    print("✅ Tablas creadas correctamente")
    
    # Crear usuario administrador
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@nexaconstructora.com.ar',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        print("✅ Usuario administrador creado: admin / admin123")
    
    # Crear plantillas de mensajes por defecto
    create_default_templates()
    
    # Crear algunos leads de ejemplo
    create_sample_leads()
    
    db.session.commit()
    print("✅ Base de datos inicializada correctamente")

def create_default_templates():
    """Crear plantillas de mensajes por defecto"""
    print("📝 Creando plantillas por defecto...")
    
    templates = [
        {
            'name': 'Bienvenida Nexa',
            'category': 'welcome',
            'content': """🏗️ ¡Hola! Gracias por tu interés en Nexa Constructora.

Somos especialistas en construcción y desarrollo inmobiliario con más de 10 años de experiencia.

¿En qué proyecto estás pensando? Te ayudo a hacerlo realidad.

📞 Llámanos: +54 9 11 1234-5678
🌐 Visítanos: {website}

Saludos,
Equipo Nexa Constructora""",
            'variables': '{"name": "Nombre del cliente", "website": "https://nexaconstructora.com.ar"}'
        },
        {
            'name': 'Seguimiento General',
            'category': 'follow_up',
            'content': """🏗️ Hola {name},

Esperamos que estés bien. Te escribimos para recordarte que estamos aquí para ayudarte con tu proyecto de construcción.

¿Has tenido tiempo de revisar nuestras propuestas? ¿Tienes alguna pregunta?

Estamos disponibles para una consulta gratuita.

Saludos,
Equipo Nexa Constructora""",
            'variables': '{"name": "Nombre del cliente"}'
        },
        {
            'name': 'Recordatorio de Seguimiento',
            'category': 'reminder',
            'content': """🏗️ Hola {name},

Esperamos que estés bien. Te escribimos para recordarte que estamos aquí para ayudarte con tu proyecto de construcción.

¿Has tenido tiempo de revisar nuestras propuestas? ¿Tienes alguna pregunta?

Estamos disponibles para una consulta gratuita.

Saludos,
Equipo Nexa Constructora""",
            'variables': '{"name": "Nombre del cliente"}'
        },
        {
            'name': 'Oferta Especial',
            'category': 'offer',
            'content': """🏗️ ¡Oferta Especial para {name}!

Por ser cliente de Nexa Constructora, te ofrecemos un descuento especial del 10% en tu próximo proyecto.

Esta oferta es válida hasta el {date}.

📞 Llámanos: +54 9 11 1234-5678
🌐 Visítanos: {website}

Saludos,
Equipo Nexa Constructora""",
            'variables': '{"name": "Nombre del cliente", "date": "Fecha límite", "website": "https://nexaconstructora.com.ar"}'
        },
        {
            'name': 'Consulta de Proyecto',
            'category': 'consultation',
            'content': """🏗️ Hola {name},

Gracias por tu interés en nuestros servicios. Nos gustaría conocer más detalles sobre tu proyecto.

¿Podrías contarnos:
- Tipo de proyecto (casa, edificio, remodelación)
- Superficie aproximada
- Presupuesto estimado
- Timeline deseado

Con esta información podemos preparar una propuesta personalizada.

📞 Llámanos: +54 9 11 1234-5678

Saludos,
Equipo Nexa Constructora""",
            'variables': '{"name": "Nombre del cliente"}'
        }
    ]
    
    for template_data in templates:
        existing = MessageTemplate.query.filter_by(
            name=template_data['name'],
            category=template_data['category']
        ).first()
        
        if not existing:
            template = MessageTemplate(
                name=template_data['name'],
                category=template_data['category'],
                content=template_data['content'],
                variables=template_data['variables'],
                is_active=True
            )
            db.session.add(template)
            print(f"✅ Plantilla creada: {template_data['name']}")

def create_sample_leads():
    """Crear algunos leads de ejemplo"""
    print("👥 Creando leads de ejemplo...")
    
    sample_leads = [
        {
            'phone_number': '5491112345678',
            'name': 'Juan Pérez',
            'email': 'juan.perez@email.com',
            'company': 'Constructora ABC',
            'source': LeadSource.WEBSITE,
            'status': LeadStatus.NUEVO,
            'notes': 'Interesado en construcción de casa de 200m²'
        },
        {
            'phone_number': '5491123456789',
            'name': 'María González',
            'email': 'maria.gonzalez@email.com',
            'company': 'Desarrollos XYZ',
            'source': LeadSource.WHATSAPP,
            'status': LeadStatus.CONTACTADO,
            'notes': 'Consulta sobre remodelación de oficinas'
        },
        {
            'phone_number': '5491134567890',
            'name': 'Carlos Rodríguez',
            'email': 'carlos.rodriguez@email.com',
            'company': 'Inversiones 123',
            'source': LeadSource.REFERIDO,
            'status': LeadStatus.INTERESADO,
            'notes': 'Proyecto de edificio de 10 pisos'
        },
        {
            'phone_number': '5491145678901',
            'name': 'Ana Martínez',
            'email': 'ana.martinez@email.com',
            'company': 'Propiedades DEF',
            'source': LeadSource.WEBSITE,
            'status': LeadStatus.CALIFICADO,
            'notes': 'Construcción de complejo residencial'
        },
        {
            'phone_number': '5491156789012',
            'name': 'Roberto López',
            'email': 'roberto.lopez@email.com',
            'company': 'Constructora GHI',
            'source': LeadSource.REDES_SOCIALES,
            'status': LeadStatus.CONVERTIDO,
            'notes': 'Proyecto aprobado - Inicio en 2 semanas'
        }
    ]
    
    for lead_data in sample_leads:
        existing = Lead.query.filter_by(phone_number=lead_data['phone_number']).first()
        if not existing:
            lead = Lead(**lead_data)
            db.session.add(lead)
            print(f"✅ Lead creado: {lead_data['name']}")

def create_sample_campaigns():
    """Crear campañas de ejemplo"""
    print("📢 Creando campañas de ejemplo...")
    
    # Obtener plantilla de seguimiento
    follow_up_template = MessageTemplate.query.filter_by(category='follow_up').first()
    
    if follow_up_template:
        campaigns = [
            {
                'name': 'Seguimiento Semanal',
                'description': 'Campaña automática de seguimiento semanal',
                'template_id': follow_up_template.id,
                'target_status': LeadStatus.CONTACTADO,
                'scheduled_date': datetime.utcnow() + timedelta(days=7)
            },
            {
                'name': 'Recordatorio Mensual',
                'description': 'Recordatorio para leads que no han respondido',
                'template_id': follow_up_template.id,
                'target_status': LeadStatus.NUEVO,
                'scheduled_date': datetime.utcnow() + timedelta(days=30)
            }
        ]
        
        for campaign_data in campaigns:
            existing = Campaign.query.filter_by(name=campaign_data['name']).first()
            if not existing:
                campaign = Campaign(**campaign_data)
                db.session.add(campaign)
                print(f"✅ Campaña creada: {campaign_data['name']}")

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de Nexa Lead Manager...")
    
    try:
        # Configurar variables de entorno si no existen
        if not os.getenv('SECRET_KEY'):
            os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
            print("⚠️  SECRET_KEY configurada (cambiar en producción)")
        
        # Crear aplicación Flask temporal para el contexto
        from flask import Flask
        temp_app = Flask(__name__)
        temp_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexa_leads.db'
        temp_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Inicializar la base de datos con el contexto de la aplicación
        db.init_app(temp_app)
        
        with temp_app.app_context():
            # Inicializar base de datos
            init_database()
            
            # Crear campañas de ejemplo
            create_sample_campaigns()
        
        print("\n🎉 ¡Configuración completada!")
        print("\n📋 Información de acceso:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("\n🌐 Para iniciar el dashboard:")
        print("   python dashboard.py")
        print("\n🤖 Para iniciar el bot de WhatsApp:")
        print("   python app.py")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
