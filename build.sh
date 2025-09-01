#!/usr/bin/env bash
# Script de build para Render
# Maneja la instalación de dependencias de manera más robusta

echo "🚀 Iniciando build en Render..."

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias de Python (sin pandas)
echo "📦 Instalando dependencias de Python..."
pip install -r requirements.txt

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "import flask; print(f'Flask version: {flask.__version__}')"
python -c "import twilio; print('Twilio instalado correctamente')"
python -c "import openai; print('OpenAI instalado correctamente')"

# Configurar entorno para Render
echo "🔧 Configurando entorno para Render..."
python init_render.py

echo "🎉 Build completado exitosamente!"
