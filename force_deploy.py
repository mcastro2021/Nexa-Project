#!/usr/bin/env python3
"""
Script para forzar el deploy en Render
Útil cuando el auto-deploy no funciona correctamente
"""

import os
import requests
import json
from datetime import datetime

def force_render_deploy():
    """Forzar deploy en Render usando webhook"""
    
    # Obtener credenciales desde variables de entorno
    RENDER_TOKEN = os.getenv('RENDER_TOKEN')
    RENDER_SERVICE_ID = os.getenv('RENDER_SERVICE_ID')
    
    if not RENDER_TOKEN:
        print("❌ Error: RENDER_TOKEN no configurado")
        print("Configura la variable de entorno RENDER_TOKEN")
        print("Obtén tu token desde: https://dashboard.render.com/account/tokens")
        return False
    
    if not RENDER_SERVICE_ID:
        print("❌ Error: RENDER_SERVICE_ID no configurado")
        print("Configura la variable de entorno RENDER_SERVICE_ID")
        print("Obtén el ID desde la URL de tu servicio en Render")
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
        print(f"🚀 Forzando deploy en Render...")
        print(f"📅 Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Servicio: {RENDER_SERVICE_ID}")
        
        # Hacer la petición POST
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            deploy_data = response.json()
            print("✅ Deploy forzado iniciado correctamente!")
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

def check_deploy_status():
    """Verificar estado del último deploy"""
    
    RENDER_TOKEN = os.getenv('RENDER_TOKEN')
    RENDER_SERVICE_ID = os.getenv('RENDER_SERVICE_ID')
    
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
    print("🚀 Render Force Deploy")
    print("=" * 40)
    
    print("Selecciona una opción:")
    print("1. Forzar Deploy")
    print("2. Ver Estado del Deploy")
    
    choice = input("\nOpción (1-2): ").strip()
    
    if choice == "1":
        force_render_deploy()
    elif choice == "2":
        check_deploy_status()
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()
