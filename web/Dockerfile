# Imagen base oficial de Node.js Alpine
FROM node:18-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias primero (para cachear capa)
COPY package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos el resto del código fuente
COPY . .

# Compilamos la aplicación (next)
RUN if [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then npm run build; fi

# Exponemos el puerto 3000
EXPOSE 3000

# Comando para servir la web
CMD ["npm", "run", "dev", "--", "-p", "3000"]