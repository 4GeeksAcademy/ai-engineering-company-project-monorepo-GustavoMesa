# Informe de auditoria y optimizacion frontend

Fecha: 28 de octubre de 2026

## Diagnostico del backoffice

El navegador mostro inicialmente el estado de carga, pero las respuestas de FastAPI y del proxy Next.js fueron correctas: `GET /locations` y `GET /stock` devolvieron HTTP 200. Al terminar las peticiones, el backoffice presento dos locales, cinco productos y sus existencias. No fue necesario modificar endpoints ni variables de entorno.

La imagen que servia el navegador ejecutaba `node server.js` y no tenia volumenes montados, por lo que no reflejaba el codigo actual del workspace. Se reconstruyeron y recrearon solo los contenedores `web` y `backoffice` con el override de produccion. FastAPI y PostgreSQL permanecieron en ejecucion.

## Cambio aplicado

Las dos apps cambiaron `@import` de Google Fonts por `next/font/google` para DM Sans y Playfair Display, conservando familias, pesos y estilos usados. Next autoaloja los archivos generados, evitando solicitudes del navegador a Google Fonts. No se extrajo un componente o hook compartido: el website y el backoffice no tienen logica de negocio comun, y compartir sus layouts simples no reduciria el trabajo del navegador.

## Resultados Lighthouse

Una ejecucion por app y fase, Lighthouse CLI 13.6.0, escritorio emulado y `throttlingMethod=simulate`:

| App | Fase | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS | Speed Index |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Website | Antes | 100 | 95 | 96 | 100 | 0,4 s | 0,4 s | 20 ms | 0 | 0,8 s |
| Website | Despues | 100 | 95 | 96 | 100 | 0,5 s | 0,5 s | 10 ms | 0 | 0,7 s |
| Backoffice | Antes | 92 | 96 | 96 | 100 | 1,2 s | 1,2 s | 60 ms | 0,053 | 1,7 s |
| Backoffice | Despues | 100 | 96 | 96 | 100 | 0,4 s | 0,4 s | 30 ms | 0,049 | 0,6 s |

En el informe local del backoffice, las solicitudes de fuentes de Google pasaron de tres a cero; el ahorro estimado por recursos bloqueantes paso de 530 ms a 30 ms. Es una estimacion de Lighthouse, no una medicion aislada de la latencia de fuente. Website mantuvo 100 de rendimiento; no se atribuye una mejora de puntuacion.

## Evidencia

Capturas del estado final y de la linea base:

- [Website antes](docs/lighthouse-website-before.jpg)
- [Website despues](docs/lighthouse-website-after.jpg)
- [Backoffice antes](docs/lighthouse-backoffice-before.jpg)
- [Backoffice despues](docs/lighthouse-backoffice-after.jpg)

Cada auditoria conserva tambien su informe completo HTML y JSON en `docs/`, con metricas, diagnosticos y captura integrada.

## Validacion y limites

- `docker compose -f docker-compose.yml -f docker-compose.production.yml build web backoffice`: compilacion, TypeScript y generacion estatica completados para ambas apps.
- `http://localhost:3000/`: HTTP 200. Backoffice: proxy de locales y stock HTTP 200; el navegador mostro dos locales y cinco stocks.
- Las paginas reconstruidas no hicieron solicitudes del navegador a `fonts.googleapis.com` ni a `fonts.gstatic.com`.
- La linea base se obtuvo de los contenedores locales previos, que no montaban el workspace; no se registro el digest de esas imagenes. Las mediciones comparten URL, dispositivo y opciones, pero la revision exacta del contenedor anterior no esta verificada. Una ejecucion por fase deja variabilidad de laboratorio.
- No hay datos CrUX/RUM ni una medicion de INP en estas pruebas. Los resultados localhost no se deben comparar directamente con PageSpeed remoto: HTTPS, red y revision de despliegue difieren.
- El CLS del backoffice sigue en 0,049, principalmente por la llegada asincrona de contenido de movimientos. La consulta de stock continua siendo una peticion por producto; no se amplio el contrato de FastAPI sin una necesidad medida que justifique ese cambio.
