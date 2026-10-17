# Inventory Manager — Especificación del Sistema

## Contexto
Sistema de gestión de inventario para **Brasaland** (cadena de 14 restaurantes en Colombia y Florida). El stock NO es un campo CRUD editable directamente, sino un cálculo derivado exclusivamente de los movimientos de inventario (entradas, salidas, mermas).

---

## Requerimientos Funcionales

### INV-001 — Registro de movimientos de inventario
- **Descripción:** El sistema debe permitir registrar movimientos de inventario de tres tipos: entrada (compra/transferencia), salida (venta/consumo) y merma (pérdida/desperdicio).
- **Criterio de aceptación:** Dado un producto, local y tipo de movimiento, cuando se registra un movimiento con cantidad y fecha, entonces el sistema almacena el movimiento y actualiza el stock calculado.

### INV-002 — Cálculo de stock derivado de movimientos
- **Descripción:** El stock actual de un producto en un local debe calcularse como la suma de todas las entradas menos la suma de todas las salidas y mermas.
- **Criterio de aceptación:** Dado un producto con movimientos registrados, cuando se consulta el stock actual, entonces el sistema devuelve `SUM(entradas) - SUM(salidas) - SUM(mermas)`.

### INV-003 — Consulta de stock por local y producto
- **Descripción:** El sistema debe exponer un endpoint que devuelva el stock calculado para un producto específico en un local específico.
- **Criterio de aceptación:** Dado un `product_id` y `location_id` válidos, cuando se consulta el stock, entonces el sistema retorna el stock calculado en tiempo real.

### INV-004 — Historial de movimientos
- **Descripción:** El sistema debe permitir consultar el historial completo de movimientos de un producto en un local, ordenado por fecha descendente.
- **Criterio de aceptación:** Dado un `product_id` y `location_id`, cuando se solicita el historial, entonces se retorna la lista de movimientos ordenados del más reciente al más antiguo.

### INV-005 — Alerta de stock mínimo
- **Descripción:** El sistema debe generar una alerta cuando el stock calculado de un producto en un local esté por debajo de un umbral mínimo configurable por producto.
- **Criterio de aceptación:** Dado un producto con `stock_calculado < stock_minimo`, cuando se consulta el stock, entonces el sistema incluye una alerta en la respuesta.

### INV-006 — Restricción de stock negativo
- **Descripción:** El sistema NO debe permitir registrar un movimiento de salida o merma que resulte en stock negativo para ese producto en ese local.
- **Criterio de aceptación:** Dado un producto con stock actual 5, cuando se intenta registrar una salida de 10, entonces el sistema rechaza la operación con error "stock insuficiente".

---

## Entidades del Dominio

### Product
| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador único |
| name | string | Nombre del producto |
| sku | string | Código SKU |
| category | enum | Categoría del producto (`CARNE`, `BEBIDA`, `LACTEO`, `VEGETAL`, `OTRO`) |
| stock_minimo | float | Umbral mínimo para alertas |
| unit | string | Unidad de medida (kg, L, unidades) |
| created_at | datetime | Fecha de creación |

### Location (Local)
| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador único |
| name | string | Nombre del local |
| country | string | País (Colombia / USA) |
| city | string | Ciudad |

### InventoryMovement
| Campo | Tipo | Descripción |
|---|---|---|
| id | UUID | Identificador único |
| product_id | UUID | Producto asociado |
| location_id | UUID | Local asociado |
| movement_type | enum | `ENTRADA`, `SALIDA`, `MERMA` |
| quantity | float | Cantidad (positiva) |
| unit_price | float | Precio unitario (opcional) |
| reference | string | Factura, orden o nota |
| notes | text | Observaciones |
| created_at | datetime | Fecha del movimiento |

### Stock (Vista calculada — NO es tabla)
| Campo | Tipo | Cálculo |
|---|---|---|
| product_id | UUID | — |
| location_id | UUID | — |
| current_stock | float | `SUM(entradas) - SUM(salidas) - SUM(mermas)` |
| alert | boolean | `current_stock < stock_minimo` |

---

## Reglas de Dominio

1. **El stock NO es un campo editable.** Ningún endpoint permite crear, actualizar o eliminar un valor de stock directamente. El stock es siempre una función agregada de los movimientos.
2. **Los movimientos son inmutables.** Una vez registrado un movimiento, no se puede modificar ni eliminar. Para corregir errores, se debe registrar un movimiento compensatorio.
3. **Stock negativo está prohibido.** Validar antes de cada salida/merma que `stock_actual - cantidad >= 0`.
4. **Trazabilidad completa.** Todo movimiento tiene `created_at`, `reference` y `notes` para auditoría.

---

## EARS — Criterios de Aceptación Formales

```
INV-001: MOVIMIENTO_REGISTRADO
  WHEN se registra un movimiento de tipo (ENTRADA | SALIDA | MERMA)
  WITH product_id, location_id, quantity, movement_type válidos
  THEN el sistema almacena el movimiento
  AND el stock calculado se actualiza automáticamente

INV-002: STOCK_CALCULADO
  GIVEN un producto con movimientos registrados en un local
  WHEN se consulta el stock actual
  THEN el resultado = SUM(entradas) - SUM(salidas) - SUM(mermas)
  AND el resultado NO proviene de un campo almacenado

INV-003: CONSULTA_STOCK
  WHEN se solicita GET /inventory/stock?product_id=X&location_id=Y
  THEN el sistema retorna { product_id, location_id, current_stock, alert }

INV-004: HISTORIAL_MOVIMIENTOS
  WHEN se solicita GET /inventory/movements?product_id=X&location_id=Y
  THEN el sistema retorna los movimientos ordenados por created_at DESC

INV-005: ALERTA_STOCK_MINIMO
  GIVEN current_stock < stock_minimo
  WHEN se consulta el stock
  THEN la respuesta incluye alert: true

INV-006: STOCK_NEGATIVO_RECHAZADO
  GIVEN current_stock = 5
  WHEN se registra una SALIDA o MERMA con quantity > current_stock
  THEN el sistema rechaza con error 422 "stock_insuficiente"
  AND no se modifica ningún movimiento

INV-007: FILTRO_POR_CATEGORIA
  WHEN se consulta GET /api/v1/inventory/products?category=Carne
  THEN el sistema retorna solo los productos cuya category coincide
  AND excluye productos de otras categorías
```

---

*Documento generado como parte de la Fase 1 — Specify (EARS).*