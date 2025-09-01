#!/usr/bin/env python3
"""
Script para verificar el estado de la base de datos
Útil para debugging y verificación post-migración
"""

import os
import sqlite3
from datetime import datetime

def check_database():
    """Verificar el estado de la base de datos"""
    db_path = os.path.join('instance', 'nexa_leads.db')
    
    print(f"🔍 Verificando base de datos: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no existe")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tablas encontradas: {len(tables)}")
        
        required_tables = [
            'user', 'lead', 'message', 'message_template', 
            'campaign', 'campaign_result', 'interaction'
        ]
        
        for table_name in required_tables:
            if any(table[0] == table_name for table in tables):
                print(f"✅ Tabla '{table_name}' existe")
                
                # Verificar columnas de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                print(f"   Columnas: {column_names}")
                
                # Verificar columnas críticas según la tabla
                if table_name == 'user':
                    critical_columns = ['id', 'username', 'email', 'password_hash', 'first_name', 'last_name', 'role']
                elif table_name == 'lead':
                    critical_columns = ['id', 'name', 'phone_number', 'status', 'source']
                elif table_name == 'message':
                    critical_columns = ['id', 'lead_id', 'content', 'message_type', 'status']
                elif table_name == 'message_template':
                    critical_columns = ['id', 'name', 'category', 'content', 'is_active']
                else:
                    critical_columns = ['id']
                
                missing_columns = [col for col in critical_columns if col not in column_names]
                if missing_columns:
                    print(f"   ⚠️  Columnas faltantes: {missing_columns}")
                else:
                    print(f"   ✅ Todas las columnas críticas están presentes")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📝 Registros: {count}")
                
            else:
                print(f"❌ Tabla '{table_name}' NO existe")
        
        # Verificar datos críticos
        print(f"\n🔍 Verificando datos críticos...")
        
        # Usuario administrador
        cursor.execute("SELECT username, role, is_active FROM user WHERE role = 'admin'")
        admin_users = cursor.fetchall()
        if admin_users:
            print(f"✅ Usuario administrador encontrado: {admin_users[0][0]}")
        else:
            print("❌ No hay usuario administrador")
        
        # Plantillas de mensaje
        cursor.execute("SELECT COUNT(*) FROM message_template WHERE is_active = 1")
        template_count = cursor.fetchone()[0]
        print(f"✅ Plantillas activas: {template_count}")
        
        print(f"\n✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Función principal"""
    print("🔍 Nexa Project - Verificador de Base de Datos")
    print("=" * 50)
    
    success = check_database()
    
    if success:
        print("\n🎉 Base de datos está en buen estado!")
    else:
        print("\n❌ Base de datos tiene problemas que requieren atención.")

if __name__ == "__main__":
    main()
