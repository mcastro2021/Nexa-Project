#!/usr/bin/env python3
"""
Script para forzar el deploy en Render usando webhooks
Útil cuando el auto-deploy no funciona correctamente
"""

import os
import requests
import json
from datetime import datetime

def trigger_render_deploy(service_id=None, token=None):
    """Forzar deploy en Render"""
    
    # Obtener credenciales desde variables de entorno
    RENDER_TOKEN = token or os.getenv('RENDER_TOKEN')
    RENDER_SERVICE_ID = service_id or os.getenv('RENDER_SERVICE_ID')
    
    if not RENDER_TOKEN:
        print("❌ Error: RENDER_TOKEN no configurado")
        print("Configura la variable de entorno RENDER_TOKEN o pásala como parámetro")
        return False
    
    if not RENDER_SERVICE_ID:
        print("❌ Error: RENDER_SERVICE_ID no configurado")
        print("Configura la variable de entorno RENDER_SERVICE_ID o pásala como parámetro")
        return False
    
    # URL de la API de Render
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/deploys"
    
    # Headers de autenticación
    headers = {
        "Authorization": f"Bearer {RENDER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Datos del deploy
    data = {
        "clearCache": "do_not_clear"
    }
    
    try:
        print(f"🚀 Iniciando deploy forzado en Render...")
        print(f"📅 Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Servicio: {RENDER_SERVICE_ID}")
        
        # Hacer la petición POST
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            deploy_data = response.json()
            print("✅ Deploy iniciado correctamente!")
            print(f"🆔 ID del Deploy: {deploy_data.get('id')}")
            print(f"📊 Estado: {deploy_data.get('status')}")
            print(f"🔗 URL del Deploy: {deploy_data.get('deployUrl')}")
            return True
        else:
            print(f"❌ Error iniciando deploy: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def check_deploy_status(service_id=None, token=None):
    """Verificar estado del último deploy"""
    
    RENDER_TOKEN = token or os.getenv('RENDER_TOKEN')
    RENDER_SERVICE_ID = service_id or os.getenv('RENDER_SERVICE_ID')
    
    if not RENDER_TOKEN or not RENDER_SERVICE_ID:
        print("❌ Error: RENDER_TOKEN y RENDER_SERVICE_ID son requeridos")
        return False
    
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/deploys"
    headers = {"Authorization": f"Bearer {RENDER_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            deploys = response.json()
            if deploys:
                latest = deploys[0]
                print(f"📊 Estado del último deploy:")
                print(f"🆔 ID: {latest.get('id')}")
                print(f"📅 Creado: {latest.get('createdAt')}")
                print(f"📊 Estado: {latest.get('status')}")
                print(f"🔗 URL: {latest.get('deployUrl')}")
                return latest
            else:
                print("ℹ️ No hay deploys disponibles")
                return None
        else:
            print(f"❌ Error obteniendo deploys: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Render Deploy Manager")
    print("=" * 40)
    
    # Verificar si se pasaron argumentos
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "deploy":
            service_id = sys.argv[2] if len(sys.argv) > 2 else None
            token = sys.argv[3] if len(sys.argv) > 3 else None
            trigger_render_deploy(service_id, token)
            
        elif command == "status":
            service_id = sys.argv[2] if len(sys.argv) > 2 else None
            token = sys.argv[3] if len(sys.argv) > 3 else None
            check_deploy_status(service_id, token)
            
        elif command == "help":
            print_help()
            
        else:
            print(f"❌ Comando desconocido: {command}")
            print_help()
    else:
        # Modo interactivo
        print("Selecciona una opción:")
        print("1. Forzar Deploy")
        print("2. Ver Estado del Deploy")
        print("3. Ayuda")
        
        choice = input("\nOpción (1-3): ").strip()
        
        if choice == "1":
            trigger_render_deploy()
        elif choice == "2":
            check_deploy_status()
        elif choice == "3":
            print_help()
        else:
            print("❌ Opción inválida")

def print_help():
    """Mostrar ayuda"""
    print("\n📖 Ayuda - Render Deploy Manager")
    print("=" * 40)
    print("\nUso:")
    print("  python webhook-render.py [comando] [servicio_id] [token]")
    print("\nComandos:")
    print("  deploy    - Forzar deploy en Render")
    print("  status   - Ver estado del último deploy")
    print("  help     - Mostrar esta ayuda")
    print("\nEjemplos:")
    print("  python webhook-render.py deploy")
    print("  python webhook-render.py deploy abc123 xyz789")
    print("  python webhook-render.py status")
    print("\nVariables de entorno:")
    print("  RENDER_TOKEN      - Token de autenticación de Render")
    print("  RENDER_SERVICE_ID - ID del servicio en Render")
    print("\nConfiguración:")
    print("1. Obtén tu RENDER_TOKEN desde: https://dashboard.render.com/account/tokens")
    print("2. Obtén tu RENDER_SERVICE_ID desde la URL de tu servicio")
    print("3. Configura las variables de entorno o pásalas como parámetros")

if __name__ == "__main__":
    main()
