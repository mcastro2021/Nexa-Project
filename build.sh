#!/bin/bash

echo "🚀 Iniciando build de Nexa Project..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar deploy forzado inmediato
echo "🔧 Ejecutando deploy forzado inmediato..."
python force_deploy_now.py

# Verificar el resultado del deploy
if [ $? -eq 0 ]; then
    echo "✅ Deploy forzado completado exitosamente!"
else
    echo "❌ Deploy forzado falló - revisar logs"
    exit 1
fi

echo "✅ Build completado exitosamente!"
