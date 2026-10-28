# Sitio público de Brasaland

Sitio de presentación de marca. No consume datos de inventario: las cantidades, alertas y movimientos son información operativa privada y se gestionan desde `../backoffice`.

## Desarrollo

```bash
npm install
npm run dev
```

Abre `http://localhost:3000`. La app usa Next.js y React, con estilos propios en `app/globals.css`.

## Docker Compose

Desde la raíz del monorepo, `docker compose up --build web` construye esta app. El sitio se sirve en el puerto 3000.

### Producción y auditoría

Requiere Docker Compose 2.24.4 o posterior para eliminar los montajes de desarrollo.
Desde la raíz, ejecuta:

```powershell
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d --build
```

Los frontends se compilan en imágenes multi-stage y ejecutan el servidor de
producción standalone (`node server.js`), sin `next dev` ni montajes sobre `/app`.
El backend se inicia sin recarga automática. Website: `http://localhost:3000`;
backoffice: `http://localhost:3001`.

Antes de medir con Lighthouse, comprueba los contenedores y las páginas:

```powershell
docker compose -f docker-compose.yml -f docker-compose.production.yml ps
curl.exe -I http://localhost:3000
curl.exe -I http://localhost:3001
```

Para volver a desarrollo, ejecuta `docker compose up -d --build`.
