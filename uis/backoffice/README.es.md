# Backoffice de Brasaland

Panel interno para consultar existencias por local, revisar movimientos y registrar entradas, salidas y mermas. Sigue los criterios `INV-001` a `INV-006` de `../../specs/inventory-manager/spec.md`. No permite editar el stock directamente.

## Comunicación con la API

El navegador llama rutas same-origin bajo `/api/inventory`. `next.config.mjs` las reescribe al servicio indicado por `INVENTORY_API_URL`, evitando exponer el nombre DNS de Docker al navegador:

- En local: `http://localhost:8000/api/v1/inventory` (valor por defecto).
- En Docker Compose: `http://services:8000/api/v1/inventory`.

Se esperan `GET /products`, `GET /locations`, `GET /stock?product_id=…&location_id=…`, `GET /movements?product_id=…&location_id=…` y `POST /movements`.

## Desarrollo

```bash
npm install
npm run dev
```

Abre `http://localhost:3001`. Para levantar con el resto del stack, ejecuta desde la raíz `docker compose up --build backoffice services`.

## Producción y auditoría

Desde la raíz del monorepo, con Docker Compose 2.24.4 o posterior:

```powershell
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d --build
```

El frontend se compila en una imagen multi-stage y arranca con el servidor
standalone (`node server.js`), sin montajes de desarrollo. Sigue disponible en
`http://localhost:3001`.

La redirección `/api/inventory` se genera durante `next build`: el argumento de
construcción `INVENTORY_API_URL` apunta a `http://services:8000/api/v1/inventory`.
Si cambia el destino, actualiza el argumento y reconstruye la imagen; cambiar
solo la variable del contenedor no regenera las redirecciones.

Para volver a desarrollo, ejecuta `docker compose up -d --build`.
