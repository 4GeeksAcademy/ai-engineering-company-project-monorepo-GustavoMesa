#!/bin/sh

# Arrancamos website en el puerto 3000 si la carpeta existe
if [ -d "website" ]; then
  cd website && npm run dev -- -p 3000 &
fi

# Arrancamos backoffice en el puerto 3001 si la carpeta existe
if [ -d "backoffice" ]; then
  cd ../backoffice && npm run dev -- -p 3001
fi

# Mantiene el contenedor activo
wait