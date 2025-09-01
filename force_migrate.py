#!/usr/bin/env python3
"""
Script de migración forzada para Render.com
Elimina y recrea completamente la base de datos con la estructura correcta
"""

import os
import sqlite3
from datetime import datetime

def create_directories():
    """Crear directorios necesarios"""
    directories = ['logs', 'uploads', 'instance']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio {directory} creado/verificado")

def force_migrate_database():
    """Migración forzada: eliminar y recrear toda la base de datos"""
    db_path = os.path.join('instance', 'nexa_leads.db')
    
    print(f"🗄️ Iniciando migración forzada: {db_path}")
    
    # Eliminar base de datos existente
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("🗑️ Base de datos anterior eliminada")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar BD anterior: {e}")
    
    try:
        # Crear nueva conexión
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📝 Creando todas las tablas desde cero...")
        
        # 1. Crear tabla user
        cursor.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                role TEXT DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                last_login DATETIME,
                password_changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'user' creada")
        
        # 2. Crear tabla lead
        cursor.execute("""
            CREATE TABLE lead (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT UNIQUE NOT NULL,
                email TEXT,
                company TEXT,
                status TEXT DEFAULT 'NUEVO',
                source TEXT DEFAULT 'OTRO',
                interest_level INTEGER DEFAULT 3,
                notes TEXT,
                next_follow_up DATETIME,
                last_contact_date DATETIME,
                priority TEXT DEFAULT 'medium',
                estimated_value REAL,
                project_type TEXT,
                location TEXT,
                created_by_id INTEGER,
                assigned_to_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'lead' creada")
        
        # 3. Crear tabla message
        cursor.execute("""
            CREATE TABLE message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                message_type TEXT DEFAULT 'outbound',
                status TEXT DEFAULT 'pending',
                scheduled_at DATETIME,
                sent_at DATETIME,
                delivered_at DATETIME,
                read_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES lead (id)
            )
        """)
        print("✅ Tabla 'message' creada")
        
        # 4. Crear tabla message_template
        cursor.execute("""
            CREATE TABLE message_template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                variables TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'message_template' creada")
        
        # 5. Crear tabla campaign
        cursor.execute("""
            CREATE TABLE campaign (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                template_id INTEGER,
                target_status TEXT,
                target_source TEXT,
                scheduled_date DATETIME,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES message_template (id)
            )
        """)
        print("✅ Tabla 'campaign' creada")
        
        # 6. Crear tabla campaign_result
        cursor.execute("""
            CREATE TABLE campaign_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                lead_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                sent_at DATETIME,
                delivered_at DATETIME,
                read_at DATETIME,
                FOREIGN KEY (campaign_id) REFERENCES campaign (id),
                FOREIGN KEY (lead_id) REFERENCES lead (id),
                FOREIGN KEY (message_id) REFERENCES message (id)
            )
        """)
        print("✅ Tabla 'campaign_result' creada")
        
        # 7. Crear tabla interaction
        cursor.execute("""
            CREATE TABLE interaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                interaction_type TEXT NOT NULL,
                description TEXT,
                outcome TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES lead (id)
            )
        """)
        print("✅ Tabla 'interaction' creada")
        
        # Insertar datos iniciales
        print("📝 Insertando datos iniciales...")
        
        # Usuario administrador
        from werkzeug.security import generate_password_hash
        admin_password = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO user (username, email, password_hash, first_name, last_name, role, is_active)
            VALUES ('admin', 'admin@nexa.com', ?, 'Administrador', 'Sistema', 'admin', 1)
        """, (admin_password,))
        print("✅ Usuario administrador creado: admin/admin123")
        
        # Plantillas de mensaje
        cursor.execute("""
            INSERT INTO message_template (name, category, content, is_active) VALUES 
            ('Bienvenida', 'welcome', '¡Hola {name}! Gracias por tu interés en Nexa Constructora. ¿En qué proyecto estás pensando?', 1),
            ('Seguimiento', 'follow_up', 'Hola {name}, ¿cómo estás? Te escribo para hacer seguimiento de tu interés en nuestros servicios.', 1),
            ('Oferta', 'offer', '¡{name}! Tenemos una oferta especial para ti: 15% de descuento en proyectos de construcción.', 1)
        """)
        print("✅ Plantillas de mensaje creadas")
        
        # Commit y verificación
        conn.commit()
        
        # Verificar estructura final
        print("\n📊 Verificando estructura de la base de datos...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Tablas creadas:")
        for table in tables:
            print(f"  - {table[0]}")
            
            # Verificar columnas de cada tabla
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print(f"    Columnas: {[col[1] for col in columns]}")
        
        print("\n✅ Migración forzada completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def setup_environment():
    """Configurar variables de entorno por defecto"""
    env_vars = {
        'FLASK_ENV': 'production',
        'FLASK_DEBUG': 'False',
        'SECRET_KEY': 'dev-secret-key-change-in-production',
        'DATABASE_URL': 'sqlite:///instance/nexa_leads.db',
        'TWILIO_ACCOUNT_SID': '',
        'TWILIO_AUTH_TOKEN': '',
        'TWILIO_PHONE_NUMBER': '',
        'OPENAI_API_KEY': '',
        'LOG_LEVEL': 'INFO'
    }
    
    print("🔧 Configurando variables de entorno...")
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
            print(f"✅ {key} = {value}")
        else:
            print(f"ℹ️ {key} ya configurado")

def main():
    """Función principal"""
    print("🚀 Nexa Project - Migración Forzada en Render")
    print("=" * 60)
    print("⚠️  ADVERTENCIA: Este script eliminará toda la base de datos existente")
    print("⚠️  y la recreará desde cero. Todos los datos se perderán.")
    print("=" * 60)
    
    create_directories()
    setup_environment()
    force_migrate_database()
    
    print("\n🎉 Migración forzada completada!")
    print("📝 La aplicación ahora debería funcionar correctamente.")

if __name__ == "__main__":
    main()
