#!/usr/bin/env bash
# Script de build para Render
# Maneja la instalación de dependencias de manera más robusta

echo "🚀 Iniciando build en Render..."

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar pandas primero con wheels precompilados
echo "📊 Instalando pandas con wheels precompilados..."
pip install --only-binary=all pandas==2.2.0

# Instalar el resto de dependencias
echo "📦 Instalando dependencias de Python..."
pip install -r requirements-render.txt

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python -c "import flask; print(f'Flask version: {flask.__version__}')"
python -c "import plotly; print(f'Plotly version: {plotly.__version__}')"

echo "🎉 Build completado exitosamente!"
