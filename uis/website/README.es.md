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
