#!/usr/bin/env python3
"""
Script para configurar automáticamente el auto-deploy en Render
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return result.stdout
        else:
            print(f"❌ Error en {description}: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return None

def setup_auto_deploy():
    """Configurar auto-deploy automáticamente"""
    print("🚀 Configurando Auto-Deploy para Nexa Project")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('render.yaml'):
        print("❌ Error: No se encontró render.yaml en el directorio actual")
        print("Asegúrate de estar en el directorio raíz del proyecto")
        return False
    
    # Verificar estado de git
    print("\n📊 Verificando estado de Git...")
    
    # Verificar si hay cambios pendientes
    status = run_command("git status --porcelain", "Verificando estado de Git")
    if status and status.strip():
        print("⚠️ Hay cambios pendientes en Git:")
        print(status)
        choice = input("¿Deseas hacer commit y push de estos cambios? (y/n): ").lower()
        if choice == 'y':
            run_command("git add .", "Agregando cambios")
            run_command("git commit -m 'Auto-deploy setup and fixes'", "Haciendo commit")
        else:
            print("❌ No se puede continuar con cambios pendientes")
            return False
    
    # Verificar rama actual
    branch = run_command("git branch --show-current", "Obteniendo rama actual")
    if branch and branch.strip() != "main":
        print(f"⚠️ Estás en la rama '{branch.strip()}', no en 'main'")
        choice = input("¿Deseas cambiar a la rama main? (y/n): ").lower()
        if choice == 'y':
            run_command("git checkout main", "Cambiando a rama main")
        else:
            print("❌ El auto-deploy solo funciona en la rama main")
            return False
    
    # Verificar configuración del repositorio
    print("\n🔗 Verificando configuración del repositorio...")
    remote_url = run_command("git remote get-url origin", "Obteniendo URL del repositorio")
    
    if remote_url:
        remote_url = remote_url.strip()
        print(f"📍 Repositorio remoto: {remote_url}")
        
        # Verificar que la URL en render.yaml coincida
        with open('render.yaml', 'r') as f:
            render_content = f.read()
        
        if 'yourusername' in render_content:
            print("⚠️ La URL del repositorio en render.yaml no está configurada correctamente")
            print("Actualizando render.yaml...")
            
            # Extraer username del remote URL
            if 'github.com' in remote_url:
                username = remote_url.split('github.com/')[1].split('/')[0]
                new_repo_url = f"https://github.com/{username}/Nexa-Project.git"
                
                # Actualizar render.yaml
                render_content = render_content.replace(
                    'https://github.com/yourusername/Nexa-Project.git',
                    new_repo_url
                )
                
                with open('render.yaml', 'w') as f:
                    f.write(render_content)
                
                print(f"✅ render.yaml actualizado con: {new_repo_url}")
                
                # Commit del cambio
                run_command("git add render.yaml", "Agregando render.yaml actualizado")
                run_command("git commit -m 'Update repository URL for auto-deploy'", "Commit de URL actualizada")
            else:
                print("❌ No se pudo determinar la URL del repositorio")
                return False
    
    # Verificar que autoDeploy esté habilitado
    if 'autoDeploy: true' not in render_content:
        print("⚠️ autoDeploy no está habilitado en render.yaml")
        print("Habilitando autoDeploy...")
        
        render_content = render_content.replace(
            'autoDeploy: false',
            'autoDeploy: true'
        )
        
        with open('render.yaml', 'w') as f:
            f.write(render_content)
        
        print("✅ autoDeploy habilitado en render.yaml")
        
        # Commit del cambio
        run_command("git add render.yaml", "Agregando render.yaml con autoDeploy")
        run_command("git commit -m 'Enable autoDeploy in render.yaml'", "Commit de autoDeploy")
    
    # Push a GitHub
    print("\n🚀 Enviando cambios a GitHub...")
    push_result = run_command("git push origin main", "Enviando cambios a GitHub")
    
    if push_result:
        print("✅ Cambios enviados a GitHub exitosamente")
        print("\n🎉 Configuración de auto-deploy completada!")
        print("\n📋 Pasos siguientes:")
        print("1. Ve a tu servicio en Render.com")
        print("2. Verifica que 'Auto-Deploy' esté habilitado")
        print("3. Haz un cambio en el código y haz push")
        print("4. Render debería detectar automáticamente los cambios")
        print("\n🔧 Si el auto-deploy no funciona:")
        print("- Verifica que el repositorio sea público o Render tenga acceso")
        print("- Confirma que la rama sea 'main'")
        print("- Usa el script webhook-render.py como respaldo")
        
        return True
    else:
        print("❌ Error enviando cambios a GitHub")
        return False

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("🚀 Nexa Project - Configurador de Auto-Deploy")
        print("=" * 50)
        print("\nUso:")
        print("  python setup_auto_deploy.py")
        print("\nEste script:")
        print("1. Verifica la configuración de Git")
        print("2. Actualiza render.yaml con la URL correcta del repositorio")
        print("3. Habilita autoDeploy si no está habilitado")
        print("4. Hace commit y push de los cambios")
        print("5. Proporciona instrucciones para verificar el auto-deploy")
        return
    
    try:
        success = setup_auto_deploy()
        if success:
            print("\n🎯 ¡Configuración completada! El auto-deploy debería funcionar ahora.")
        else:
            print("\n❌ La configuración no se pudo completar. Revisa los errores arriba.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
