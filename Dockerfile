# Dockerfile para Nexa Lead Manager
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements-render.txt .

# Instalar pandas primero con wheels precompilados
RUN pip install --upgrade pip && \
    pip install --only-binary=all pandas==2.0.3

# Instalar el resto de dependencias
RUN pip install -r requirements-render.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dashboard:app"]
