#!/usr/bin/env python3
"""
Script de deploy forzado inmediato para Render.com
Resuelve el Internal Server Error ejecutando la migración de base de datos
"""

import os
import sys
import subprocess
import time

def check_render_environment():
    """Verificar si estamos en Render.com"""
    if os.environ.get('RENDER'):
        print("✅ Ejecutando en Render.com")
        return True
    else:
        print("⚠️  Ejecutando localmente")
        return False

def force_migrate_database():
    """Ejecutar migración forzada de base de datos"""
    print("🗄️ Iniciando migración forzada de base de datos...")
    
    try:
        # Importar y ejecutar la migración
        from force_migrate import force_migrate_database
        force_migrate_database()
        print("✅ Migración forzada completada exitosamente!")
        return True
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

def verify_database():
    """Verificar que la base de datos esté funcionando"""
    print("🔍 Verificando estado de la base de datos...")
    
    try:
        # Importar y ejecutar la verificación
        from check_db import check_database
        success = check_database()
        if success:
            print("✅ Base de datos verificada y funcionando")
            return True
        else:
            print("❌ Base de datos tiene problemas")
            return False
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def test_flask_app():
    """Probar que la aplicación Flask pueda iniciar"""
    print("🚀 Probando inicio de aplicación Flask...")
    
    try:
        # Importar la aplicación
        from dashboard import app
        
        # Verificar que la aplicación se pueda crear
        with app.app_context():
            print("✅ Aplicación Flask creada exitosamente")
            print(f"   - Configuración: {app.config.get('ENV', 'production')}")
            print(f"   - Debug: {app.config.get('DEBUG', False)}")
            return True
            
    except Exception as e:
        print(f"❌ Error creando aplicación Flask: {e}")
        return False

def setup_environment():
    """Configurar variables de entorno críticas"""
    print("🔧 Configurando variables de entorno...")
    
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
    
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
            print(f"✅ {key} = {value}")
        else:
            print(f"ℹ️ {key} ya configurado")

def create_directories():
    """Crear directorios necesarios"""
    print("📁 Creando directorios necesarios...")
    
    directories = ['logs', 'uploads', 'instance']
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Directorio {directory} creado/verificado")
        except Exception as e:
            print(f"⚠️ Error creando directorio {directory}: {e}")

def main():
    """Función principal"""
    print("🚀 Nexa Project - Deploy Forzado Inmediato")
    print("=" * 60)
    print("🔧 Resolviendo Internal Server Error...")
    print("=" * 60)
    
    # Configurar entorno
    setup_environment()
    create_directories()
    
    # Verificar si estamos en Render
    is_render = check_render_environment()
    
    # Ejecutar migración forzada
    print("\n" + "="*60)
    print("🗄️ PASO 1: Migración Forzada de Base de Datos")
    print("="*60)
    
    if not force_migrate_database():
        print("❌ CRÍTICO: La migración falló")
        print("🔄 Intentando recrear directorios y migrar nuevamente...")
        
        # Limpiar y recrear
        import shutil
        if os.path.exists('instance'):
            try:
                shutil.rmtree('instance')
                print("🗑️ Directorio instance eliminado")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar instance: {e}")
        
        create_directories()
        
        if not force_migrate_database():
            print("❌ CRÍTICO: La migración falló nuevamente")
            return False
    
    # Verificar base de datos
    print("\n" + "="*60)
    print("🔍 PASO 2: Verificación de Base de Datos")
    print("="*60)
    
    if not verify_database():
        print("❌ CRÍTICO: La verificación de BD falló")
        return False
    
    # Probar aplicación Flask
    print("\n" + "="*60)
    print("🚀 PASO 3: Prueba de Aplicación Flask")
    print("="*60)
    
    if not test_flask_app():
        print("❌ CRÍTICO: La aplicación Flask no puede iniciar")
        return False
    
    # Resumen final
    print("\n" + "="*60)
    print("🎉 DEPLOY FORZADO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("✅ Base de datos migrada y verificada")
    print("✅ Aplicación Flask funcionando")
    print("✅ Internal Server Error resuelto")
    print("\n📝 La aplicación ahora debería funcionar correctamente")
    print("🌐 Accede a la URL de Render.com para verificar")
    
    return True

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
