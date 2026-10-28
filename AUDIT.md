# Auditoria frontend: linea base y analisis

## Alcance y estado

Aplicaciones: `uis/website` y `uis/backoffice`. Backend: `services`.
Esta fase documenta el analisis; no acredita optimizaciones ni resultados finales.
Se conserva la separacion entre las aplicaciones.

Las skills `core-web-vitals`, `performance` y `web-perf` se instalaron en
`.agents/skills/` y se consultaron para esta auditoria. Los hallazgos combinan
revision de codigo, Lighthouse local y los informes publicos facilitados.

## Linea base Lighthouse

Fecha: 28 de octubre de 2026. Lighthouse 13.5.0, escritorio emulado,
HeadlessChromium 153.0.8010.36, carga inicial y limitacion personalizada.
Una ejecucion por aplicacion; no son medianas de tres ejecuciones.

| Aplicacion | URL medida | Performance | Accessibility | Best Practices | SEO |
|---|---|---:|---:|---:|---:|
| Website | http://161.35.78.162:3000/ | 99 | 94 | 74 | 100 |
| Backoffice | http://161.35.78.162:3001/ | 99 | 95 | 74 | 100 |

| Metrica mostrada en el informe | Website | Backoffice |
|---|---:|---:|
| FCP | 0,2 s | 0,7 s |
| LCP | 0,4 s | 0,7 s |
| CLS | 0 | 0,006 |
| TBT | 110 ms | 70 ms |
| Speed Index | 0,4 s | 0,7 s |

Se transcriben los valores redondeados visibles, sin reconstruir cifras exactas
desde la calculadora de puntuaciones. No hay datos de usuarios reales en los
informes. INP queda sin datos: TBT no es INP ni lo sustituye.

Fuentes:

- [Website, 20:00:22](https://pagespeed.web.dev/analysis/http-161-35-78-162/vfq3c1fmkl?form_factor=desktop)
- [Backoffice, 20:03:53](https://pagespeed.web.dev/analysis/http-161-35-78-162/md37oa7kl5?form_factor=desktop)

No se ha verificado que el servidor remoto ejecute la misma revision y
configuracion de produccion que el entorno Docker local.

## Hallazgos de los informes

| Hallazgo | Evidencia | Causa raiz y limites de la conclusion |
|---|---|---|
| Contraste insuficiente | Ambos informes lo marcan como fallo. | Combinaciones de colores que no cumplen el contraste exigido. Falta identificar los elementos y estados concretos antes de modificar la paleta. |
| No usa HTTPS | Website: 17 solicitudes no seguras; backoffice: 19. | Las URLs auditadas se sirven mediante HTTP. Requiere configurar TLS en el despliegue; una refactorizacion React no lo corrige. |
| Recursos bloquean el renderizado | Ahorro estimado: 30 ms en website y 520 ms en backoffice. | Ambos CSS importan Google Fonts, creando una dependencia de red adicional. Falta desglosar los recursos del informe para atribuir que parte del ahorro corresponde a las fuentes. |
| JavaScript sin minificar | Ahorro estimado: 198 KiB en website y 203 KiB en backoffice. | Causa raiz pendiente de inspeccionar los recursos remotos y su modo de ejecucion. No prueba por si solo que nuestros componentes sean responsables. |
| JavaScript sin usar | Ahorro estimado: 480 KiB en cada aplicacion. | Codigo descargado no utilizado durante esa navegacion. Falta identificar bundles y cobertura; no debe eliminarse funcionalidad basandose solo en esta cifra. |
| JavaScript heredado | Ahorro estimado: 9 KiB en ambas aplicaciones. | Falta identificar el paquete o transformacion responsable antes de cambiar compatibilidad. |

Los ahorros son estimaciones de Lighthouse: no son mejoras medidas, no se suman
automaticamente y no garantizan un aumento de puntuacion.

## Hallazgos de codigo y duplicidades

### Fuentes en ambas aplicaciones

- Archivos: [website CSS](uis/website/app/globals.css) y
  [backoffice CSS](uis/backoffice/app/globals.css).
- Ambas cargan DM Sans y Playfair Display con `@import` de Google Fonts.
- Causa: descubrimiento de las fuentes despues de descargar y analizar el CSS.
- Propuesta: evaluar `next/font` con autoalojamiento, manteniendo familias, pesos
  y apariencia. La compilacion debe poder obtener las fuentes o disponer de
  archivos locales autorizados; no introducir una sustitucion silenciosa.
- Posible impacto: FCP/LCP y cambios de fuente; requiere medicion.

### Carga y refresco de inventario

Archivo: [pagina de inventario](uis/backoffice/app/page.tsx).

- El stock se solicita mediante una peticion por producto, despues de cargar
  el catalogo. El numero de peticiones crece con el catalogo. Un hook no elimina
  esta limitacion; una solucion por lotes requiere verificar el contrato del
  backend antes de ampliar alcance.
- `refreshKey` vuelve a cargar productos y locales tras registrar un movimiento.
  Tambien dispara stock e historial; la nueva referencia de productos vuelve a
  disparar stock. Propuesta: refrescar solo los datos afectados.
- Tres efectos repiten control `active`, propagacion de errores y limpieza.
  Las respuestas obsoletas se ignoran, pero las peticiones no se cancelan.
  Propuesta: hook de inventario con responsabilidades claras y AbortController,
  sin ocultar fallos de red como listas vacias.
- El estado de carga del catalogo se usa para las alertas aunque el stock siga
  pendiente. Puede mostrarse un mensaje favorable sin datos actualizados.
  Propuesta: estados explicitos de carga/error para stock e historial.

### Coste de renderizado

Archivo: [pagina de inventario](uis/backoffice/app/page.tsx).

- `stocks.find` se ejecuta por cada producto en cada render. En el caso general
  cuesta O(productos x stocks). Propuesta: indice memoizado por producto.
- Los helpers construyen formateadores Intl cada vez que se invocan.
  Propuesta: reutilizar instancias de formato.
- La pagina completa es cliente y contiene el estado de cada campo del modal.
  Escribir vuelve a ejecutar el componente padre. Propuesta: aislar el formulario
  y su estado sin cambiar validacion, envio ni mensajes.
- El beneficio sobre INP no esta medido; requiere probar interacciones reales.

### Componentes repetidos

- Los selectores de producto/local aparecen en controles y formulario.
- Las tres tarjetas de estadisticas repiten estructura.
- El website repite la marca en cabecera y pie.
- Extraer componentes pequenos dentro de cada aplicacion puede mejorar
  mantenimiento; no equivale por si mismo a mejorar Web Vitals.
- No se encontro logica de negocio comun entre website y backoffice que
  justifique un hook compartido entre aplicaciones. Sus layouts pequenos y sus
  metadatos distintos no justifican acoplar los dos proyectos.

### Accesibilidad e integridad visual

- El modal declara `aria-modal`, pero carece de gestion explicita del foco,
  restauracion del foco y cierre con Escape.
- La tabla sustituye una fila de carga por un numero variable de productos:
  existe riesgo de desplazamiento de contenido. El CLS observado es bajo;
  falta medir transiciones con datos y filtros antes de atribuir un problema.
- El website es una pagina de servidor sin hooks cliente. Conviene conservarlo.
  Su ilustracion principal usa CSS, no una imagen pendiente de `next/image`.

## Protocolo para las siguientes fases

1. Identificar los elementos de contraste y los bundles remotos senalados.
2. Aplicar mejoras acotadas, preservando arquitectura y funcionalidad.
3. Compilar ambos frontends y verificar lectura, filtros y modal; no crear
   movimientos reales sin necesidad ni autorizacion.
4. Desplegar la revision optimizada en el mismo servidor antes de comparar con
   estos informes. Registrar revision, modo de produccion y condiciones.
5. Repetir Lighthouse en escritorio con las mismas condiciones; preferiblemente
   tres ejecuciones por aplicacion y medianas, dejando clara la limitacion de
   esta linea base de una sola ejecucion.
6. Documentar en `REPORT.md` cambios, mediciones, diferencias y pendientes.
   No comparar puntuaciones de localhost o movil con esta linea base remota.
7. Conservar HTML/JSON y capturas reales de antes/despues en el repositorio.
   Las capturas aun no estan guardadas. No generar evidencia posterior ficticia.

## Actualizacion local: diagnostico y medicion

Fecha: 28 de octubre de 2026. Lighthouse CLI 13.6.0, escritorio emulado,
limitacion `simulate`; una ejecucion por app y fase. Los informes HTML/JSON y
capturas son evidencia de laboratorio, no datos de usuarios reales.

### Diagnostico del backoffice

- `INVENTORY_API_URL` dentro del contenedor apuntaba a
  `http://services:8000/api/v1/inventory`, que es el destino correcto en la red
  Compose. `GET /locations` y `GET /stock` devolvieron 200 tanto directamente
  en FastAPI como a traves de `/api/inventory`.
- La pagina termina cargando dos locales, cinco productos y sus existencias.
  La captura inicial se hizo mientras los fetch de catalogo y stock seguian
  pendientes; no se encontro un fallo del endpoint ni una variable incorrecta.
- El contenedor activo ejecutaba `node server.js` sin volumenes, mientras que
  el Compose por defecto define modo desarrollo. Por eso seguia sirviendo una
  imagen anterior y no reflejaba cambios del workspace. Se reconstruyeron y
  recrearon solo los dos frontends con el override de produccion; no se
  modificaron FastAPI ni PostgreSQL.

### Comparacion Lighthouse local

| App | Fase | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS | Speed Index |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Website | Antes | 100 | 95 | 96 | 100 | 0,4 s | 0,4 s | 20 ms | 0 | 0,8 s |
| Website | Despues | 100 | 95 | 96 | 100 | 0,5 s | 0,5 s | 10 ms | 0 | 0,7 s |
| Backoffice | Antes | 92 | 96 | 96 | 100 | 1,2 s | 1,2 s | 60 ms | 0,053 | 1,7 s |
| Backoffice | Despues | 100 | 96 | 96 | 100 | 0,4 s | 0,4 s | 30 ms | 0,049 | 0,6 s |

El contenedor anterior no montaba el workspace y su digest/revision exacta no
se registro; por ello, los valores antes/despues son comparables en URL,
dispositivo y configuracion Lighthouse, pero la atribucion causal no es un
experimento perfectamente controlado. Una sola ejecucion por fase tambien
deja variabilidad de laboratorio. No comparar estos valores localhost con la
linea base PageSpeed remota de la primera tabla como si fueran la misma muestra.

### Cambio aplicado y evidencia

- Ambas apps ahora configuran DM Sans y Playfair Display mediante `next/font`;
  Next las autoaloja y evita solicitudes del navegador a Google Fonts. En el
  backoffice, el informe paso de tres solicitudes Google Fonts y 530 ms de
  ahorro estimado por recursos bloqueantes a cero solicitudes y 30 ms
  estimados. El ahorro de Lighthouse es una estimacion, no una medicion aislada
  de latencia de fuente.
- El rendimiento del website ya era 100 y permanecio en 100; no se afirma una
  mejora de puntuacion. El backoffice paso de 92 a 100 en esta ejecucion.
- No se extrajo logica de negocio entre las apps: el inventario no tiene un
  consumidor equivalente en website, y compartir layouts simples acoplaria
  aplicaciones que conservan metadata y estilos distintos.
- Capturas: [website antes](docs/lighthouse-website-before.jpg),
  [website despues](docs/lighthouse-website-after.jpg),
  [backoffice antes](docs/lighthouse-backoffice-before.jpg) y
  [backoffice despues](docs/lighthouse-backoffice-after.jpg).
- Informes completos: `docs/lighthouse-{website,backoffice}-{before,after}.report.html`
  y `.json`.

## Control de versiones

Antes de esta fase ya habia cambios en Compose, Dockerfiles, documentacion de
ambas aplicaciones y `uis/website/tsconfig.json`. Deben revisarse antes de
seleccionar archivos para el commit; no usar `git add .` indiscriminadamente.
Esta fase no crea un commit ni acredita que existan evidencias finales.
