#!/usr/bin/env python3
"""
Script para verificar el estado actual de la aplicación
Útil para diagnosticar problemas antes y después del deploy
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_environment():
    """Verificar variables de entorno"""
    print("🔧 Verificando variables de entorno...")
    
    required_vars = ['FLASK_ENV', 'SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if var not in os.environ:
            missing_vars.append(var)
            print(f"❌ {var}: NO configurado")
        else:
            print(f"✅ {var}: {os.environ[var]}")
    
    if missing_vars:
        print(f"⚠️  Variables faltantes: {missing_vars}")
        return False
    
    return True

def check_directories():
    """Verificar directorios necesarios"""
    print("\n📁 Verificando directorios...")
    
    required_dirs = ['logs', 'uploads', 'instance']
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}: Existe")
        else:
            missing_dirs.append(directory)
            print(f"❌ {directory}: NO existe")
    
    if missing_dirs:
        print(f"⚠️  Directorios faltantes: {missing_dirs}")
        return False
    
    return True

def check_database_file():
    """Verificar archivo de base de datos"""
    print("\n🗄️ Verificando archivo de base de datos...")
    
    db_path = os.path.join('instance', 'nexa_leads.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos NO existe: {db_path}")
        return False
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(db_path)
    print(f"✅ Base de datos existe: {db_path}")
    print(f"   Tamaño: {file_size} bytes")
    
    if file_size == 0:
        print("⚠️  Base de datos está vacía")
        return False
    
    return True

def check_database_structure():
    """Verificar estructura de la base de datos"""
    print("\n📊 Verificando estructura de base de datos...")
    
    db_path = os.path.join('instance', 'nexa_leads.db')
    
    if not os.path.exists(db_path):
        print("❌ No se puede verificar estructura - BD no existe")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No hay tablas en la base de datos")
            return False
        
        print(f"✅ Tablas encontradas: {len(tables)}")
        
        required_tables = [
            'user', 'lead', 'message', 'message_template', 
            'campaign', 'campaign_result', 'interaction'
        ]
        
        missing_tables = []
        for table_name in required_tables:
            if any(table[0] == table_name for table in tables):
                print(f"   ✅ {table_name}")
                
                # Verificar columnas críticas
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                if table_name == 'user' and 'first_name' not in columns:
                    print(f"      ⚠️  Columna 'first_name' faltante en tabla user")
                    missing_tables.append(f"{table_name}.first_name")
                
            else:
                print(f"   ❌ {table_name}")
                missing_tables.append(table_name)
        
        if missing_tables:
            print(f"\n⚠️  Problemas encontrados: {missing_tables}")
            return False
        
        print("✅ Todas las tablas y columnas críticas están presentes")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_flask_app():
    """Verificar que la aplicación Flask pueda importarse"""
    print("\n🚀 Verificando aplicación Flask...")
    
    try:
        # Intentar importar la aplicación
        from dashboard import app
        
        print("✅ Aplicación Flask importada exitosamente")
        print(f"   - Configuración: {app.config.get('ENV', 'production')}")
        print(f"   - Debug: {app.config.get('DEBUG', False)}")
        
        # Verificar que tenga las rutas básicas
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"   - Rutas disponibles: {len(routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importando aplicación Flask: {e}")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_login', 
        'werkzeug', 'sqlite3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
            print(f"✅ {package}: Instalado")
        except ImportError:
            print(f"❌ {package}: NO instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Paquetes faltantes: {missing_packages}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🔍 Nexa Project - Verificador de Estado")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 Entorno: {'Render.com' if os.environ.get('RENDER') else 'Local'}")
    print("=" * 50)
    
    checks = [
        ("Variables de Entorno", check_environment),
        ("Directorios", check_directories),
        ("Archivo de Base de Datos", check_database_file),
        ("Estructura de Base de Datos", check_database_structure),
        ("Aplicación Flask", check_flask_app),
        ("Dependencias", check_dependencies)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error durante verificación: {e}")
            results.append((check_name, False))
    
    # Resumen final
    print("\n" + "="*50)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Resultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        print("✅ La aplicación debería funcionar correctamente")
        return True
    else:
        print(f"\n⚠️  {total - passed} verificaciones fallaron")
        print("❌ La aplicación puede tener problemas")
        print("🔧 Ejecuta 'python force_deploy_now.py' para resolver")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        sys.exit(1)
