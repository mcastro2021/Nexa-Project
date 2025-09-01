#!/usr/bin/env python3
"""
Script de inicialización para Render
Configura el entorno y crea directorios necesarios
"""

import os
import sys
from pathlib import Path

def setup_render_environment():
    """Configurar entorno para Render"""
    print("🚀 Configurando entorno para Render...")
    
    # Crear directorios necesarios si no existen
    directories = ['logs', 'uploads', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio {directory} creado/verificado")
    
    # Configurar variables de entorno por defecto
    if not os.getenv('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        print("⚠️ SECRET_KEY configurada por defecto")
    
    if not os.getenv('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'production'
        print("✅ FLASK_ENV configurado como production")
    
    if not os.getenv('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///nexa_leads.db'
        print("✅ DATABASE_URL configurado")
    
    print("🎉 Entorno configurado correctamente para Render")

if __name__ == '__main__':
    setup_render_environment()
