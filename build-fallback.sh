#!/usr/bin/env bash
# Script de build alternativo para Render
# Maneja errores de pandas de manera más robusta

echo "🚀 Iniciando build alternativo en Render..."

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Intentar instalar pandas con wheels precompilados
echo "📊 Intentando instalar pandas con wheels precompilados..."
if pip install --only-binary=all pandas==2.0.3; then
    echo "✅ Pandas instalado exitosamente"
    PANDAS_INSTALLED=true
else
    echo "⚠️ Error instalando pandas, intentando versión alternativa..."
    if pip install --only-binary=all pandas==1.5.3; then
        echo "✅ Pandas 1.5.3 instalado exitosamente"
        PANDAS_INSTALLED=true
    else
        echo "❌ No se pudo instalar pandas, continuando sin él..."
        PANDAS_INSTALLED=false
    fi
fi

# Instalar dependencias básicas
echo "📦 Instalando dependencias básicas..."
pip install -r requirements-minimal.txt

# Si pandas se instaló, intentar instalar plotly
if [ "$PANDAS_INSTALLED" = true ]; then
    echo "📊 Instalando plotly..."
    pip install plotly==5.15.0 kaleido==0.2.1
else
    echo "⚠️ Saltando plotly (requiere pandas)"
fi

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "import flask; print(f'Flask version: {flask.__version__}')"
python -c "import twilio; print('Twilio instalado correctamente')"

if [ "$PANDAS_INSTALLED" = true ]; then
    python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
    python -c "import plotly; print(f'Plotly version: {plotly.__version__}')"
else
    echo "⚠️ Pandas no disponible - algunas funcionalidades estarán limitadas"
fi

echo "🎉 Build alternativo completado!"
