#!/bin/bash

echo "🚀 Iniciando build de Nexa Project..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migración forzada de base de datos
echo "🗄️ Ejecutando migración forzada de base de datos..."
python force_migrate.py

# Verificar que la base de datos se creó correctamente
echo "🔍 Verificando estado de la base de datos..."
python check_db.py

echo "✅ Build completado exitosamente!"
