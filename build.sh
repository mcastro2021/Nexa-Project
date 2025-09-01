#!/bin/bash

echo "🚀 Iniciando build de Nexa Project..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migración de base de datos
echo "🗄️ Ejecutando migración de base de datos..."
python migrate_database.py

# Ejecutar inicialización de Render
echo "⚙️ Configurando entorno de Render..."
python init_render.py

echo "✅ Build completado exitosamente!"
