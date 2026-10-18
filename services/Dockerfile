# Imagen base oficial de Python ligera
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos herramientas del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalamos 'uv' globalmente
RUN pip install --no-cache-dir uv

# Copiamos solo requirements.txt primero (capa cacheable)
COPY requirements.txt .

# Instalamos dependencias usando uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copiamos el resto del código del backend
COPY . .

# Exponemos el puerto 8000 del backend
EXPOSE 8000

# Comando por defecto ejecutando Uvicorn con hot-reload en desarrollo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
