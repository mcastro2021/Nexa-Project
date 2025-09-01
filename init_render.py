#!/usr/bin/env python3
"""
Script de inicialización para Render.com
Configura el entorno y migra la base de datos si es necesario
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

def setup_database():
    """Configurar y migrar la base de datos"""
    db_path = os.path.join('instance', 'nexa_leads.db')
    
    print(f"🗄️ Configurando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla message existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message'")
        if cursor.fetchone():
            print("📝 Tabla 'message' existe, verificando estructura...")
            
            # Verificar columnas de la tabla message
            cursor.execute("PRAGMA table_info(message)")
            columns = [column[1] for column in cursor.fetchall()]
            
            print(f"📊 Columnas actuales en tabla 'message': {columns}")
            
            # Agregar columnas faltantes
            missing_columns = []
            if 'scheduled_at' not in columns:
                missing_columns.append("scheduled_at")
            if 'sent_at' not in columns:
                missing_columns.append("sent_at")
            if 'delivered_at' not in columns:
                missing_columns.append("delivered_at")
            if 'read_at' not in columns:
                missing_columns.append("read_at")
            if 'message_type' not in columns:
                missing_columns.append("message_type")
            if 'status' not in columns:
                missing_columns.append("status")
            
            # Agregar columnas faltantes
            for column in missing_columns:
                try:
                    if column in ['scheduled_at', 'sent_at', 'delivered_at', 'read_at']:
                        cursor.execute(f"ALTER TABLE message ADD COLUMN {column} DATETIME")
                        print(f"✅ Columna '{column}' agregada exitosamente")
                    elif column == 'message_type':
                        cursor.execute(f"ALTER TABLE message ADD COLUMN {column} VARCHAR(20) DEFAULT 'outbound'")
                        print(f"✅ Columna '{column}' agregada exitosamente")
                    elif column == 'status':
                        cursor.execute(f"ALTER TABLE message ADD COLUMN {column} VARCHAR(20) DEFAULT 'pending'")
                        print(f"✅ Columna '{column}' agregada exitosamente")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"ℹ️ Columna '{column}' ya existe")
                    else:
                        print(f"❌ Error agregando columna '{column}': {e}")
                        # Si hay error, recrear la tabla
                        print("🔄 Recreando tabla 'message'...")
                        recreate_message_table(cursor)
                        break
        else:
            # Crear tabla message si no existe
            print("📝 Creando tabla 'message'...")
            create_message_table(cursor)
        
        # Verificar estructura de la tabla lead
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lead'")
        if cursor.fetchone():
            print("📝 Tabla 'lead' existe, verificando estructura...")
            
            cursor.execute("PRAGMA table_info(lead)")
            lead_columns = [column[1] for column in cursor.fetchall()]
            
            print(f"📊 Columnas actuales en tabla 'lead': {lead_columns}")
            
            # Agregar columnas faltantes en lead
            if 'interest_level' not in lead_columns:
                try:
                    cursor.execute("ALTER TABLE lead ADD COLUMN interest_level INTEGER DEFAULT 3")
                    print("✅ Columna 'interest_level' agregada exitosamente")
                except sqlite3.OperationalError as e:
                    print(f"ℹ️ Columna 'interest_level' ya existe o no se pudo agregar: {e}")
            
            if 'next_follow_up' not in lead_columns:
                try:
                    cursor.execute("ALTER TABLE lead ADD COLUMN next_follow_up DATETIME")
                    print("✅ Columna 'next_follow_up' agregada exitosamente")
                except sqlite3.OperationalError as e:
                    print(f"ℹ️ Columna 'next_follow_up' ya existe o no se pudo agregar: {e}")
            
            if 'last_contact_date' not in lead_columns:
                try:
                    cursor.execute("ALTER TABLE lead ADD COLUMN last_contact_date DATETIME")
                    print("✅ Columna 'last_contact_date' agregada exitosamente")
                except sqlite3.OperationalError as e:
                    print(f"ℹ️ Columna 'last_contact_date' ya existe o no se pudo agregar: {e}")
        else:
            print("📝 Creando tabla 'lead'...")
            create_lead_table(cursor)
        
        # Verificar si existe la tabla message_template
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message_template'")
        if not cursor.fetchone():
            print("📝 Creando tabla 'message_template'...")
            create_message_template_table(cursor)
        
        # Verificar si existe la tabla campaign
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='campaign'")
        if not cursor.fetchone():
            print("📝 Creando tabla 'campaign'...")
            create_campaign_table(cursor)
        
        # Verificar si existe la tabla campaign_result
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='campaign_result'")
        if not cursor.fetchone():
            print("📝 Creando tabla 'campaign_result'...")
            create_campaign_result_table(cursor)
        
        # Verificar si existe la tabla interaction
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='interaction'")
        if not cursor.fetchone():
            print("📝 Creando tabla 'interaction'...")
            create_interaction_table(cursor)
        
        # Commit de cambios
        conn.commit()
        print("✅ Base de datos configurada exitosamente")
        
        # Verificar estructura final
        print("\n📊 Estructura final de la base de datos:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

def recreate_message_table(cursor):
    """Recrear la tabla message con la estructura correcta"""
    try:
        # Eliminar tabla existente
        cursor.execute("DROP TABLE IF EXISTS message")
        
        # Crear nueva tabla
        cursor.execute("""
            CREATE TABLE message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                message_type VARCHAR(20) DEFAULT 'outbound',
                status VARCHAR(20) DEFAULT 'pending',
                scheduled_at DATETIME,
                sent_at DATETIME,
                delivered_at DATETIME,
                read_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES lead (id)
            )
        """)
        print("✅ Tabla 'message' recreada exitosamente")
        
    except Exception as e:
        print(f"❌ Error recreando tabla 'message': {e}")

def create_message_table(cursor):
    """Crear tabla message"""
    cursor.execute("""
        CREATE TABLE message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            message_type VARCHAR(20) DEFAULT 'outbound',
            status VARCHAR(20) DEFAULT 'pending',
            scheduled_at DATETIME,
            sent_at DATETIME,
            delivered_at DATETIME,
            read_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES lead (id)
        )
    """)
    print("✅ Tabla 'message' creada exitosamente")

def create_lead_table(cursor):
    """Crear tabla lead"""
    cursor.execute("""
        CREATE TABLE lead (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(120),
            company VARCHAR(100),
            status VARCHAR(20) DEFAULT 'NUEVO',
            source VARCHAR(20) DEFAULT 'OTRO',
            interest_level INTEGER DEFAULT 3,
            notes TEXT,
            next_follow_up DATETIME,
            last_contact_date DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabla 'lead' creada exitosamente")

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
    print("🚀 Nexa Project - Inicialización en Render")
    print("=" * 50)
    
    create_directories()
    setup_environment()
    setup_database()
    
    print("\n✅ Inicialización completada exitosamente!")

if __name__ == "__main__":
    main()
