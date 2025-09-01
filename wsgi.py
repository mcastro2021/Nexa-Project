#!/usr/bin/env python3
"""
WSGI entry point para Render
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Importar la aplicación Flask
from dashboard import app

# Configurar variables de entorno por defecto si no están definidas
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'

if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///nexa_leads.db'

# Crear directorios necesarios
directories = ['logs', 'uploads', 'temp']
for directory in directories:
    Path(directory).mkdir(exist_ok=True)

# La aplicación Flask está disponible como 'app'
if __name__ == '__main__':
    app.run()
