#!/usr/bin/env python3
"""
Dashboard Web para Nexa Lead Manager
Interfaz moderna para gestión de leads y campañas de WhatsApp
"""

import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# import plotly.graph_objs as go
# import plotly.utils
import json
from datetime import datetime, timedelta
from models import db, User, Lead, LeadStatus, LeadSource, Message, MessageTemplate, Campaign, CampaignResult, Interaction
from lead_manager import lead_manager
import os

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexa_leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_interaction(lead_id, interaction_type, description, outcome):
    """Crear una nueva interacción para un lead"""
    try:
        interaction = Interaction(
            lead_id=lead_id,
            interaction_type=interaction_type,
            description=description,
            outcome=outcome
        )
        db.session.add(interaction)
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Error creando interacción: {e}")
        return False

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rutas principales
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
@login_required
def get_stats():
    """Obtener estadísticas para el dashboard"""
    try:
        # Estadísticas generales
        total_leads = Lead.query.count()
        new_leads = Lead.query.filter_by(status=LeadStatus.NUEVO).count()
        contacted_leads = Lead.query.filter_by(status=LeadStatus.CONTACTADO).count()
        interested_leads = Lead.query.filter_by(status=LeadStatus.INTERESADO).count()
        converted_leads = Lead.query.filter_by(status=LeadStatus.CONVERTIDO).count()
        
        # Leads que necesitan seguimiento
        today = datetime.utcnow()
        leads_needing_follow_up = Lead.query.filter(
            Lead.next_follow_up <= today,
            Lead.status.in_([LeadStatus.NUEVO, LeadStatus.CONTACTADO, LeadStatus.INTERESADO])
        ).count()
        
        # Mensajes enviados hoy
        messages_today = Message.query.filter(
            Message.created_at >= today.replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        
        # Conversiones de la semana
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_conversions = Lead.query.filter(
            Lead.status == LeadStatus.CONVERTIDO,
            Lead.updated_at >= week_ago
        ).count()
        
        return jsonify({
            'total_leads': total_leads,
            'new_leads': new_leads,
            'contacted_leads': contacted_leads,
            'interested_leads': interested_leads,
            'converted_leads': converted_leads,
            'leads_needing_follow_up': leads_needing_follow_up,
            'messages_today': messages_today,
            'weekly_conversions': weekly_conversions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads')
@login_required
def get_leads():
    """Obtener lista de leads con filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        source = request.args.get('source')
        search = request.args.get('search')
        
        query = Lead.query
        
        if status:
            query = query.filter_by(status=status)
        if source:
            query = query.filter_by(source=source)
        if search:
            query = query.filter(
                db.or_(
                    Lead.name.contains(search),
                    Lead.phone_number.contains(search),
                    Lead.email.contains(search),
                    Lead.company.contains(search)
                )
            )
        
        leads = query.order_by(Lead.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'leads': [{
                'id': lead.id,
                'name': lead.name,
                'phone_number': lead.phone_number,
                'email': lead.email,
                'company': lead.company,
                'status': lead.status.value,
                'source': lead.source.value,
                'created_at': lead.created_at.isoformat(),
                'last_contact_date': lead.last_contact_date.isoformat() if lead.last_contact_date else None,
                'next_follow_up': lead.next_follow_up.isoformat() if lead.next_follow_up else None
            } for lead in leads.items],
            'total': leads.total,
            'pages': leads.pages,
            'current_page': leads.page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>')
@login_required
def get_lead_detail(lead_id):
    """Obtener detalles de un lead específico"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        
        # Obtener mensajes del lead
        messages = Message.query.filter_by(lead_id=lead_id).order_by(Message.created_at.desc()).limit(10).all()
        
        # Obtener interacciones del lead
        interactions = Interaction.query.filter_by(lead_id=lead_id).order_by(Interaction.created_at.desc()).limit(10).all()
        
        return jsonify({
            'lead': {
                'id': lead.id,
                'name': lead.name,
                'phone_number': lead.phone_number,
                'email': lead.email,
                'company': lead.company,
                'status': lead.status.value,
                'source': lead.source.value,
                'interest_level': lead.interest_level,
                'notes': lead.notes,
                'created_at': lead.created_at.isoformat(),
                'last_contact_date': lead.last_contact_date.isoformat() if lead.last_contact_date else None,
                'next_follow_up': lead.next_follow_up.isoformat() if lead.next_follow_up else None
            },
            'messages': [{
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'status': msg.status,
                'created_at': msg.created_at.isoformat()
            } for msg in messages],
            'interactions': [{
                'id': interaction.id,
                'type': interaction.interaction_type,
                'description': interaction.description,
                'outcome': interaction.outcome,
                'created_at': interaction.created_at.isoformat()
            } for interaction in interactions]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>/send-message', methods=['POST'])
@login_required
def send_message_to_lead(lead_id):
    """Enviar mensaje a un lead específico"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        message_content = data.get('message')
        template_category = data.get('template_category', 'custom')
        
        if not message_content:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        success = False
        if template_category != 'custom':
            success = lead_manager.send_follow_up_message(lead, template_category)
        else:
            success = lead_manager.send_whatsapp_message(lead.phone_number, message_content, lead.id)
        
        if success:
            return jsonify({'success': True, 'message': 'Mensaje enviado correctamente'})
        else:
            return jsonify({'error': 'Error enviando mensaje'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>/update-status', methods=['POST'])
@login_required
def update_lead_status(lead_id):
    """Actualizar estado de un lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        new_status = data.get('status')
        notes = data.get('notes')
        
        if new_status:
            lead.status = LeadStatus(new_status)
            lead.last_contact_date = datetime.utcnow()
            if notes:
                lead.notes = notes
            db.session.commit()
            
            # Crear interacción
            create_interaction(
                lead.id,
                'status_update',
                f'Estado actualizado a: {new_status}',
                'completed'
            )
            
            return jsonify({'success': True, 'message': 'Estado actualizado correctamente'})
        else:
            return jsonify({'error': 'Estado requerido'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns')
@login_required
def get_campaigns():
    """Obtener lista de campañas"""
    try:
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        
        return jsonify({
            'campaigns': [{
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'template_name': campaign.template.name if campaign.template else None,
                'target_status': campaign.target_status.value if campaign.target_status else None,
                'target_source': campaign.target_source.value if campaign.target_source else None,
                'scheduled_date': campaign.scheduled_date.isoformat() if campaign.scheduled_date else None,
                'is_active': campaign.is_active,
                'created_at': campaign.created_at.isoformat()
            } for campaign in campaigns]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns', methods=['POST'])
@login_required
def create_campaign():
    """Crear nueva campaña"""
    try:
        data = request.get_json()
        
        campaign = Campaign(
            name=data['name'],
            description=data.get('description'),
            template_id=data.get('template_id'),
            target_status=LeadStatus(data['target_status']) if data.get('target_status') else None,
            target_source=LeadSource(data['target_source']) if data.get('target_source') else None,
            scheduled_date=datetime.fromisoformat(data['scheduled_date']) if data.get('scheduled_date') else None
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({'success': True, 'campaign_id': campaign.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates')
@login_required
def get_templates():
    """Obtener plantillas de mensajes"""
    try:
        templates = MessageTemplate.query.filter_by(is_active=True).all()
        
        return jsonify({
            'templates': [{
                'id': template.id,
                'name': template.name,
                'category': template.category,
                'content': template.content,
                'variables': template.variables
            } for template in templates]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
@login_required
def get_analytics():
    """Obtener datos para gráficos de analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        analytics = lead_manager.get_lead_analytics(days)
        
        # Verificar que analytics no esté vacío
        if not analytics:
            analytics = {
                'status_distribution': {},
                'source_distribution': {},
                'conversion_rate': 0,
                'total_leads': 0,
                'conversions': 0
            }
        
        # Retornar solo los datos sin gráficos (plotly removido)
        return jsonify({
            'analytics': analytics,
            'status_chart': None,  # Gráfico deshabilitado temporalmente
            'source_chart': None   # Gráfico deshabilitado temporalmente
        })
        
    except Exception as e:
        print(f"Error en analytics: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/import-leads', methods=['POST'])
@login_required
def import_leads():
    """Importar leads desde archivo CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Guardar archivo temporalmente
        temp_path = f'temp_import_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        file.save(temp_path)
        
        # Importar leads
        imported, skipped = lead_manager.import_leads_from_csv(temp_path)
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'imported': imported,
            'skipped': skipped
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads', methods=['POST'])
@login_required
def create_lead():
    """Crear nuevo lead manualmente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('phone_number'):
            return jsonify({'error': 'Número de teléfono es requerido'}), 400
        
        # Verificar si el lead ya existe
        existing_lead = Lead.query.filter_by(phone_number=data['phone_number']).first()
        if existing_lead:
            return jsonify({'error': 'Ya existe un lead con este número de teléfono'}), 400
        
        # Crear nuevo lead
        lead = Lead(
            phone_number=data['phone_number'],
            name=data.get('name'),
            email=data.get('email'),
            company=data.get('company'),
            source=LeadSource(data.get('source', 'otro')),
            status=LeadStatus(data.get('status', 'nuevo')),
            interest_level=data.get('interest_level', 1),
            notes=data.get('notes'),
            next_follow_up=datetime.utcnow() + timedelta(days=7)  # Seguimiento en 7 días
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Crear interacción inicial
        create_interaction(
            lead.id,
            'lead_created',
            'Lead creado manualmente desde el dashboard',
            'completed'
        )
        
        return jsonify({
            'success': True,
            'lead_id': lead.id,
            'message': 'Lead creado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
@login_required
def update_lead(lead_id):
    """Actualizar lead existente"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            lead.name = data['name']
        if 'email' in data:
            lead.email = data['email']
        if 'company' in data:
            lead.company = data['company']
        if 'source' in data:
            lead.source = LeadSource(data['source'])
        if 'status' in data:
            lead.status = LeadStatus(data['status'])
        if 'interest_level' in data:
            lead.interest_level = data['interest_level']
        if 'notes' in data:
            lead.notes = data['notes']
        if 'next_follow_up' in data and data['next_follow_up']:
            lead.next_follow_up = datetime.fromisoformat(data['next_follow_up'])
        
        lead.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Crear interacción de actualización
        create_interaction(
            lead.id,
            'lead_updated',
            'Lead actualizado desde el dashboard',
            'completed'
        )
        
        return jsonify({
            'success': True,
            'message': 'Lead actualizado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
@login_required
def delete_lead(lead_id):
    """Eliminar lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        
        # Crear interacción antes de eliminar
        create_interaction(
            lead.id,
            'lead_deleted',
            'Lead eliminado desde el dashboard',
            'completed'
        )
        
        db.session.delete(lead)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Lead eliminado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>/interaction', methods=['POST'])
@login_required
def create_lead_interaction(lead_id):
    """Crear una nueva interacción para un lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        interaction = Interaction(
            lead_id=lead_id,
            interaction_type=data.get('type', 'general'),
            description=data.get('description', ''),
            outcome=data.get('outcome', 'completed')
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Interacción creada correctamente',
            'interaction_id': interaction.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>/send-message', methods=['POST'])
@login_required
def send_lead_message(lead_id):
    """Enviar mensaje a un lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        message_content = data.get('message')
        scheduled_time = data.get('scheduled')
        
        if not message_content:
            return jsonify({'error': 'Contenido del mensaje requerido'}), 400
        
        # Crear el mensaje
        message = Message(
            lead_id=lead_id,
            content=message_content,
            message_type='outbound',
            status='pending'
        )
        
        # Si hay programación, establecer la fecha
        if scheduled_time:
            try:
                scheduled_datetime = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
                message.scheduled_at = scheduled_datetime
                message.status = 'scheduled'
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido'}), 400
        
        db.session.add(message)
        
        # Crear interacción
        interaction = Interaction(
            lead_id=lead_id,
            interaction_type='message_sent',
            description=f'Mensaje enviado: {message_content[:50]}...',
            outcome='completed'
        )
        db.session.add(interaction)
        
        # Actualizar fecha de último contacto
        lead.last_contact_date = datetime.utcnow()
        
        db.session.commit()
        
        # Aquí se integraría con Twilio para envío real
        # Por ahora solo simulamos el envío
        try:
            from lead_manager import send_whatsapp_message
            if not scheduled_time:  # Solo enviar inmediatamente
                send_whatsapp_message(lead.phone_number, message_content)
                message.status = 'sent'
                db.session.commit()
        except Exception as e:
            logger.warning(f"No se pudo enviar mensaje real: {e}")
            # El mensaje se marca como enviado aunque no se haya enviado físicamente
        
        return jsonify({
            'success': True,
            'message': 'Mensaje enviado correctamente',
            'message_id': message.id,
            'status': message.status
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error enviando mensaje: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze-intent', methods=['POST'])
@login_required
def analyze_lead_intent():
    """Analizar intención del lead usando IA"""
    try:
        from ai_features import ai_features
        
        data = request.get_json()
        message_content = data.get('message')
        lead_data = data.get('lead_data', {})
        
        if not message_content:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        analysis = ai_features.analyze_lead_intent(message_content, lead_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/predict-conversion/<int:lead_id>')
@login_required
def predict_lead_conversion(lead_id):
    """Predecir probabilidad de conversión del lead"""
    try:
        from ai_features import ai_features
        
        lead = Lead.query.get_or_404(lead_id)
        prediction = ai_features.predict_lead_conversion(lead)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/generate-message', methods=['POST'])
@login_required
def generate_personalized_message():
    """Generar mensaje personalizado usando IA"""
    try:
        from ai_features import ai_features
        
        data = request.get_json()
        lead_id = data.get('lead_id')
        template_type = data.get('template_type', 'welcome')
        
        if not lead_id:
            return jsonify({'error': 'ID de lead requerido'}), 400
        
        lead = Lead.query.get_or_404(lead_id)
        message = ai_features.generate_personalized_message(lead, template_type)
        
        return jsonify({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze-campaign/<int:campaign_id>')
@login_required
def analyze_campaign_performance(campaign_id):
    """Analizar rendimiento de campaña usando IA"""
    try:
        from ai_features import ai_features
        
        analysis = ai_features.analyze_campaign_performance(campaign_id)
        
        if 'error' in analysis:
            return jsonify(analysis), 400
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas para templates HTML
@app.route('/leads')
@login_required
def leads_page():
    return render_template('leads.html')

@app.route('/campaigns')
@login_required
def campaigns_page():
    return render_template('campaigns.html')

@app.route('/analytics')
@login_required
def analytics_page():
    return render_template('analytics.html')

@app.route('/templates')
@login_required
def templates_page():
    return render_template('templates.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@nexaconstructora.com.ar',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario admin creado: admin / admin123")
    
    # Configuración para producción
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
