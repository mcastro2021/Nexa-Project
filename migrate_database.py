#!/usr/bin/env python3
"""
Script de migración para actualizar la base de datos de Nexa Project
Agrega las columnas faltantes y corrige la estructura de las tablas
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrar la base de datos a la estructura más reciente"""
    
    db_path = 'nexa_leads.db'
    
    # Verificar si la base de datos existe
    if not os.path.exists(db_path):
        print(f"❌ Base de datos {db_path} no encontrada")
        print("Creando nueva base de datos...")
        create_new_database(db_path)
        return
    
    print(f"🔄 Migrando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura actual de la tabla message
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
                elif column == 'message_type':
                    cursor.execute(f"ALTER TABLE message ADD COLUMN {column} VARCHAR(20) DEFAULT 'outbound'")
                elif column == 'status':
                    cursor.execute(f"ALTER TABLE message ADD COLUMN {column} VARCHAR(20) DEFAULT 'pending'")
                
                print(f"✅ Columna '{column}' agregada exitosamente")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"ℹ️ Columna '{column}' ya existe")
                else:
                    print(f"❌ Error agregando columna '{column}': {e}")
        
        # Verificar estructura de la tabla lead
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
        print("✅ Migración completada exitosamente")
        
        # Verificar estructura final
        print("\n📊 Estructura final de la base de datos:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_new_database(db_path):
    """Crear una nueva base de datos con la estructura correcta"""
    print("🆕 Creando nueva base de datos...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla user
        cursor.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(120) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla lead
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
        
        # Crear tabla message
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
        
        # Crear tabla message_template
        cursor.execute("""
            CREATE TABLE message_template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                variables TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla campaign
        cursor.execute("""
            CREATE TABLE campaign (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                template_id INTEGER,
                target_status VARCHAR(20),
                target_source VARCHAR(20),
                scheduled_date DATETIME,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES message_template (id)
            )
        """)
        
        # Crear tabla campaign_result
        cursor.execute("""
            CREATE TABLE campaign_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                lead_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                sent_at DATETIME,
                delivered_at DATETIME,
                read_at DATETIME,
                FOREIGN KEY (campaign_id) REFERENCES campaign (id),
                FOREIGN KEY (lead_id) REFERENCES lead (id),
                FOREIGN KEY (message_id) REFERENCES message (id)
            )
        """)
        
        # Crear tabla interaction
        cursor.execute("""
            CREATE TABLE interaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                interaction_type VARCHAR(50) NOT NULL,
                description TEXT,
                outcome VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES lead (id)
            )
        """)
        
        # Crear usuario admin por defecto
        cursor.execute("""
            INSERT INTO user (username, password_hash, is_admin) 
            VALUES ('admin', 'pbkdf2:sha256:600000$dev-secret-key-change-in-production$hash', TRUE)
        """)
        
        # Crear plantillas de mensaje por defecto
        cursor.execute("""
            INSERT INTO message_template (name, category, content, is_active) VALUES 
            ('Bienvenida', 'welcome', '¡Hola {name}! Gracias por tu interés en Nexa Constructora. ¿En qué proyecto estás pensando?', TRUE),
            ('Seguimiento', 'follow_up', 'Hola {name}, ¿cómo estás? Te escribo para hacer seguimiento de tu interés en nuestros servicios.', TRUE),
            ('Oferta', 'offer', '¡{name}! Tenemos una oferta especial para ti: 15% de descuento en proyectos de construcción.', TRUE)
        """)
        
        conn.commit()
        print("✅ Nueva base de datos creada exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando nueva base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_message_template_table(cursor):
    """Crear tabla message_template"""
    cursor.execute("""
        CREATE TABLE message_template (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            variables TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insertar plantillas por defecto
    cursor.execute("""
        INSERT INTO message_template (name, category, content, is_active) VALUES 
        ('Bienvenida', 'welcome', '¡Hola {name}! Gracias por tu interés en Nexa Constructora. ¿En qué proyecto estás pensando?', TRUE),
        ('Seguimiento', 'follow_up', 'Hola {name}, ¿cómo estás? Te escribo para hacer seguimiento de tu interés en nuestros servicios.', TRUE),
        ('Oferta', 'offer', '¡{name}! Tenemos una oferta especial para ti: 15% de descuento en proyectos de construcción.', TRUE)
    """)

def create_campaign_table(cursor):
    """Crear tabla campaign"""
    cursor.execute("""
        CREATE TABLE campaign (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            template_id INTEGER,
            target_status VARCHAR(20),
            target_source VARCHAR(20),
            scheduled_date DATETIME,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

def create_campaign_result_table(cursor):
    """Crear tabla campaign_result"""
    cursor.execute("""
        CREATE TABLE campaign_result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            lead_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            sent_at DATETIME,
            delivered_at DATETIME,
            read_at DATETIME
        )
    """)

def create_interaction_table(cursor):
    """Crear tabla interaction"""
    cursor.execute("""
        CREATE TABLE interaction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            interaction_type VARCHAR(50) NOT NULL,
            description TEXT,
            outcome VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

if __name__ == "__main__":
    print("🚀 Nexa Project - Migración de Base de Datos")
    print("=" * 50)
    migrate_database()
    print("\n✅ Proceso completado!")
