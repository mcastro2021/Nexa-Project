@echo off
echo ========================================
echo    Nexa WhatsApp Bot - Iniciando
echo ========================================
echo.

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo ❌ Error: No se encontró el archivo .env
    echo.
    echo 📝 Por favor:
    echo 1. Copia el archivo env_example a .env
    echo 2. Configura tus credenciales en .env
    echo.
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo 🔧 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias si no están instaladas
echo 📦 Verificando dependencias...
pip install -r requirements.txt

REM Verificar que las variables de entorno estén configuradas
echo 🔍 Verificando configuración...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Configuración cargada')" 2>nul
if errorlevel 1 (
    echo ❌ Error: Problema con la configuración
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Nexa WhatsApp Bot...
echo.
echo 📡 El bot estará disponible en: http://localhost:5000
echo 📱 Webhook URL: http://localhost:5000/webhook
echo 📊 Estadísticas: http://localhost:5000/stats
echo.
echo 💡 Para detener el bot, presiona Ctrl+C
echo.

REM Iniciar la aplicación
python app.py

echo.
echo 👋 Nexa WhatsApp Bot detenido
pause
