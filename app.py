#!/usr/bin/env python3
"""
Archivo app.py para compatibilidad con Render
Simplemente importa la aplicación desde dashboard.py
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar variables de entorno por defecto si no están definidas
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'

if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

if not os.getenv('DATABASE_URL'):
    if os.getenv('RENDER'):
        os.environ['DATABASE_URL'] = 'sqlite:///nexa_leads.db'
    else:
        os.environ['DATABASE_URL'] = 'sqlite:///instance/nexa_leads.db'

# Crear directorios necesarios
directories = ['logs', 'uploads', 'temp']
if not os.getenv('RENDER'):
    directories.append('instance')  # Solo crear instance en entorno local

for directory in directories:
    Path(directory).mkdir(exist_ok=True)

# Importar la aplicación Flask desde dashboard.py
from dashboard import app

# La aplicación Flask está disponible como 'app'
if __name__ == '__main__':
    app.run()
