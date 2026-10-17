# Inventory Manager — Tareas Atómicas

## Fase 3: Desglose de Tareas Verificables

---

### T001 — Modelo Product
- **Archivo:** `src/inventory/models.py`
- **Verificación:** `Product` tiene campos `id`, `name`, `sku`, `stock_minimo`, `unit`, `created_at`
- **Criterio:** ✅ Clase SQLAlchemy o dataclass con tipos correctos

### T002 — Modelo Location
- **Archivo:** `src/inventory/models.py`
- **Verificación:** `Location` tiene campos `id`, `name`, `country`, `city`
- **Criterio:** ✅ Clase definida

### T003 — Modelo InventoryMovement
- **Archivo:** `src/inventory/models.py`
- **Verificación:** `InventoryMovement` tiene campos `id`, `product_id`, `location_id`, `movement_type` (enum: ENTRADA, SALIDA, MERMA), `quantity`, `unit_price`, `reference`, `notes`, `created_at`
- **Criterio:** ✅ Clase y enum definidos

### T004 — Schema Pydantic para requests/responses
- **Archivo:** `src/inventory/schemas.py`
- **Verificación:** Schemas para crear movimiento, consultar stock, historial
- **Criterio:** ✅ Schemas con validación de tipos

### T005 — Lógica de cálculo de stock
- **Archivo:** `src/inventory/service.py`
- **Verificación:** Función `calcular_stock(product_id, location_id)` devuelve `SUM(entradas) - SUM(salidas) - SUM(mermas)`
- **Criterio:** ✅ Stock calculado como agregación SQL, no campo directo

### T006 — Validación de stock negativo
- **Archivo:** `src/inventory/service.py`
- **Verificación:** Antes de INSERT de SALIDA o MERMA, verificar `stock_actual >= cantidad`
- **Criterio:** ✅ Rechaza con error 422 si stock insuficiente

### T007 — Endpoint POST /movements
- **Archivo:** `src/inventory/router.py`
- **Verificación:** Registra movimiento y devuelve el objeto creado
- **Criterio:** ✅ INV-001

### T008 — Endpoint GET /stock
- **Archivo:** `src/inventory/router.py`
- **Verificación:** Devuelve `{ product_id, location_id, current_stock, alert }`
- **Criterio:** ✅ INV-002, INV-003, INV-005

### T009 — Endpoint GET /movements (historial)
- **Archivo:** `src/inventory/router.py`
- **Verificación:** Devuelve movimientos ordenados por fecha DESC
- **Criterio:** ✅ INV-004

### T010 — Alerta de stock mínimo
- **Archivo:** `src/inventory/service.py`
- **Verificación:** Si `current_stock < stock_minimo`, incluir `alert: true` en respuesta
- **Criterio:** ✅ INV-005

### T011 — Endpoints CRUD para Product y Location
- **Archivo:** `src/inventory/router.py`
- **Verificación:** POST/GET para products y locations
- **Criterio:** ✅ Operaciones básicas funcionales

### T012 — Script de datos iniciales
- **Archivo:** `docs/inventario/entrada-inicial.md`
- **Verificación:** Documenta productos, locales y movimientos de ejemplo
- **Criterio:** ✅ Datos semilla listos para pruebas

### T013 — Tests EARS (Fase 5)
- **Archivo:** `src/inventory/tests.py`
- **Verificación:** Tests automatizados para cada criterio INV-001 a INV-006
- **Criterio:** ✅ Todos los tests pasan

---

*Documento generado como parte de la Fase 3 — Tasks.*