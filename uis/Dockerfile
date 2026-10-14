# 1. Imagen base oficial de Node.js Alpine
FROM node:18-alpine

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos todo el contenido de la carpeta uis al contenedor
COPY . .

# 4. Instalamos dependencias de manera segura (si existen las carpetas)
RUN if [ -d "website" ]; then cd website && npm install; fi
RUN if [ -d "backoffice" ]; then cd backoffice && npm install; fi

# 5. Damos permisos de ejecución al script start.sh
RUN chmod +x start.sh

# 6. Exponemos los puertos correspondientes (3000 y 3001)
EXPOSE 3000 3001

# 7. Comando por defecto para arrancar
CMD ["./start.sh"]