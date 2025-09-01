#!/bin/bash

echo "🚀 Iniciando build de Nexa Project..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar inicialización de Render (incluye migración de base de datos)
echo "⚙️ Configurando entorno de Render..."
python init_render.py

echo "✅ Build completado exitosamente!"
