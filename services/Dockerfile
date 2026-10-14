# 1. Imagen base oficial de Python ligera
FROM python:3.11-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Instalamos herramientas del sistema necesarias y pip por si acaso
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalamos 'uv' globalmente tal como pide el ejercicio
RUN pip install --no-cache-dir uv

# 5. Copiamos el archivo de requerimientos
COPY requirements.txt .

# 6. Instalamos dependencias usando uv pip install como requiere la guía
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 7. Copiamos el resto del código del backend
COPY . .

# 8. Exponemos el puerto 8000 del backend
EXPOSE 8000

# 9. Comando por defecto ejecutando Uvicorn con --reload habilitado
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]