#!/usr/bin/env python3
"""
Script de prueba para verificar la estructura de la base de datos
"""

import os
import sqlite3
from pathlib import Path

def test_database_structure():
    """Probar la estructura de la base de datos"""
    print("🧪 Probando estructura de base de datos...")
    
    # Ruta de la base de datos
    db_path = 'nexa_leads.db'
    print(f"🗄️ Ruta de BD: {Path(db_path).absolute()}")
    
    try:
        # Crear conexión
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Conexión a BD exitosa")
        
        # Verificar tabla user
        cursor.execute("PRAGMA table_info(user)")
        user_columns = {col[1]: col[2] for col in cursor.fetchall()}
        print(f"📋 Columnas en tabla user: {list(user_columns.keys())}")
        
        # Verificar columnas críticas
        critical_columns = ['id', 'username', 'email', 'password_hash', 'first_name', 'last_name']
        missing_critical = [col for col in critical_columns if col not in user_columns]
        
        if missing_critical:
            print(f"❌ Columnas críticas faltantes: {missing_critical}")
            return False
        else:
            print("✅ Todas las columnas críticas están presentes")
        
        # Verificar que se puede hacer una consulta
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        print(f"👥 Usuarios en la BD: {user_count}")
        
        # Verificar usuario admin
        cursor.execute("SELECT username, role FROM user WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        if admin_user:
            print(f"✅ Usuario admin encontrado: {admin_user}")
        else:
            print("❌ Usuario admin no encontrado")
        
        conn.close()
        print("✅ Prueba de estructura completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_database_structure()
    if success:
        print("🎉 Base de datos está funcionando correctamente")
    else:
        print("💥 Hay problemas con la base de datos")
