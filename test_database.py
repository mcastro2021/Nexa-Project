#!/usr/bin/env python3
"""
Script de prueba para verificar la base de datos
"""

import os
import sqlite3
from pathlib import Path

def test_database_creation():
    """Probar la creación de la base de datos"""
    print("🧪 Probando creación de base de datos...")
    
    # Crear directorio instance si no existe
    instance_dir = Path('instance')
    instance_dir.mkdir(exist_ok=True)
    print(f"✅ Directorio instance: {instance_dir.absolute()}")
    
    # Ruta de la base de datos
    db_path = instance_dir / 'nexa_leads.db'
    print(f"🗄️ Ruta de BD: {db_path.absolute()}")
    
    try:
        # Crear conexión
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Conexión a BD exitosa")
        
        # Crear tabla de prueba
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        print("✅ Tabla de prueba creada")
        
        # Insertar dato de prueba
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        print("✅ Dato de prueba insertado")
        
        # Verificar dato
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()
        print(f"✅ Dato recuperado: {result}")
        
        # Limpiar
        cursor.execute("DROP TABLE test_table")
        print("✅ Tabla de prueba eliminada")
        
        conn.commit()
        conn.close()
        print("✅ Conexión cerrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_table():
    """Probar la creación de la tabla user"""
    print("\n👤 Probando tabla user...")
    
    db_path = Path('instance') / 'nexa_leads.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla user
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
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
        print("✅ Tabla user creada")
        
        # Verificar estructura
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        print(f"📋 Columnas: {[col[1] for col in columns]}")
        
        # Crear usuario de prueba
        from werkzeug.security import generate_password_hash
        admin_password = generate_password_hash('admin123')
        cursor.execute("""
            INSERT OR REPLACE INTO user (username, email, password_hash, first_name, last_name, role, is_active)
            VALUES ('admin', 'admin@nexa.com', ?, 'Administrador', 'Sistema', 'admin', 1)
        """, (admin_password,))
        print("✅ Usuario admin creado")
        
        # Verificar usuario
        cursor.execute("SELECT username, role FROM user WHERE username = 'admin'")
        user = cursor.fetchone()
        print(f"✅ Usuario recuperado: {user}")
        
        conn.commit()
        conn.close()
        print("✅ Tabla user probada exitosamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en tabla user: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test de Base de Datos - Nexa Project")
    print("=" * 50)
    
    # Test 1: Creación básica
    if test_database_creation():
        print("\n✅ Test de creación básica: PASÓ")
    else:
        print("\n❌ Test de creación básica: FALLÓ")
        return
    
    # Test 2: Tabla user
    if test_user_table():
        print("\n✅ Test de tabla user: PASÓ")
    else:
        print("\n❌ Test de tabla user: FALLÓ")
        return
    
    print("\n🎉 Todos los tests pasaron!")
    print("📝 La base de datos está funcionando correctamente.")

if __name__ == '__main__':
    main()
