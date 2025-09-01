# 🚀 Configuración de Auto-Deploy en Render

## Problema Identificado
Render no detecta automáticamente los cambios en el repositorio, requiriendo deploys manuales.

## Soluciones Implementadas

### 1. Configuración del render.yaml
```yaml
services:
  - type: web
    name: nexa-lead-manager
    env: python
    plan: starter
    autoDeploy: true                    # ✅ Habilita auto-deploy
    repo: https://github.com/yourusername/Nexa-Project.git  # ✅ URL del repositorio
    branch: main                        # ✅ Rama a monitorear
    buildCommand: chmod +x build.sh && ./build.sh
    startCommand: gunicorn app:app
```

### 2. GitHub Actions Workflow
Archivo: `.github/workflows/render-deploy.yml`

**Configuración requerida:**
1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Agrega estos secrets:
   - `RENDER_TOKEN`: Token de autenticación de Render
   - `RENDER_SERVICE_ID`: ID de tu servicio en Render

### 3. Script de Deploy Forzado
Archivo: `webhook-render.py`

**Uso:**
```bash
# Modo interactivo
python webhook-render.py

# Comandos directos
python webhook-render.py deploy
python webhook-render.py status
python webhook-render.py help
```

## Pasos para Configurar Auto-Deploy

### Paso 1: Obtener RENDER_TOKEN
1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Account → Tokens
3. Create new token
4. Copia el token generado

### Paso 2: Obtener RENDER_SERVICE_ID
1. Ve a tu servicio en Render
2. La URL será: `https://dashboard.render.com/web/nexa-lead-manager`
3. El ID es: `nexa-lead-manager`

### Paso 3: Configurar Variables de Entorno
```bash
# En tu sistema local
export RENDER_TOKEN="tu_token_aqui"
export RENDER_SERVICE_ID="nexa-lead-manager"

# O en Render Dashboard
# Environment Variables:
# RENDER_TOKEN = tu_token_aqui
# RENDER_SERVICE_ID = nexa-lead-manager
```

### Paso 4: Configurar GitHub Secrets
1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Agrega:
   - Name: `RENDER_TOKEN`
   - Value: `tu_token_aqui`
5. Repite para `RENDER_SERVICE_ID`

### Paso 5: Verificar Configuración
```bash
# Probar el script
python webhook-render.py status

# Deberías ver el estado del último deploy
```

## Verificación del Auto-Deploy

### 1. Hacer un cambio en el código
```bash
# Editar cualquier archivo
echo "# Test auto-deploy" >> README.md
```

### 2. Commit y Push
```bash
git add .
git commit -m "Test auto-deploy"
git push origin main
```

### 3. Verificar en Render
- Ve a tu servicio en Render
- Deberías ver "Deploy in progress" automáticamente
- Si no funciona, usa el script de deploy forzado

## Troubleshooting

### El auto-deploy no funciona
1. Verifica que `autoDeploy: true` esté en `render.yaml`
2. Confirma que la URL del repositorio sea correcta
3. Verifica que la rama sea `main` o `master`
4. Usa el script de deploy forzado como respaldo

### Error en GitHub Actions
1. Verifica que los secrets estén configurados
2. Confirma que el workflow esté en la rama correcta
3. Revisa los logs de Actions en GitHub

### Error en Render
1. Verifica las variables de entorno
2. Confirma que el buildCommand y startCommand sean correctos
3. Revisa los logs de build en Render

## Comandos Útiles

### Deploy Forzado
```bash
# Usando variables de entorno
python webhook-render.py deploy

# Pasando parámetros directamente
python webhook-render.py deploy nexa-lead-manager tu_token_aqui
```

### Ver Estado
```bash
python webhook-render.py status
```

### Ayuda
```bash
python webhook-render.py help
```

## Configuración Recomendada

### Para Desarrollo
- `autoDeploy: true` en `render.yaml`
- GitHub Actions para deploys automáticos
- Script de deploy forzado como respaldo

### Para Producción
- `autoDeploy: false` para control manual
- GitHub Actions para deploys controlados
- Script de deploy forzado para emergencias

## Notas Importantes

1. **Seguridad**: Nunca compartas tu `RENDER_TOKEN`
2. **Ramas**: Asegúrate de que la rama configurada sea la correcta
3. **Permisos**: El repositorio debe ser público o Render debe tener acceso
4. **Webhooks**: Render usa webhooks de GitHub para detectar cambios

## Soporte

Si el auto-deploy sigue sin funcionar:
1. Revisa los logs de Render
2. Verifica la configuración de GitHub
3. Usa el script de deploy forzado
4. Contacta al soporte de Render

---

**¡Con esta configuración, Render debería detectar automáticamente los cambios y hacer redeploy!** 🎉
