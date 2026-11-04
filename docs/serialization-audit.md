# Auditoría de Serialización del Backend — Brasaland API

**Fecha:** 4 de noviembre de 2026  
**Auditor:** Senior Backend Developer  
**Proyecto:** MVP Brasaland — Monorepo 4Geeks  
**Rama:** `feature/serialization-audit`

---

## 1. RESUMEN EJECUTIVO

Se ha realizado una auditoría exhaustiva de los endpoints del backend FastAPI en las carpetas `./services` y `./src`. El análisis identificó **7 vulnerabilidades críticas y de alto riesgo** relacionadas con **sobreexposición de datos en respuestas JSON**.

**Estado:** 🔴 **REQUIERE REMEDIACIÓN INMEDIATA**

### Problemas Identificados (por Severidad)

| # | Severidad | Endpoint | Problema | Causa |
|---|-----------|----------|---------|-------|
| 1 | 🔴 CRÍTICO | `POST /api/v1/inventory/movements` | Exposición de `unit_price` sensible | Sin `response_model` definido |
| 2 | 🔴 CRÍTICO | `GET /api/v1/inventory/movements` | Exposición de historial financiero completo | Retorna directamente `dict(r)` |
| 3 | 🔴 CRÍTICO | `GET /api/v1/inventory/stock` | Sin filtrado de datos internos | Retorna estructura sin validar |
| 4 | 🟠 ALTO | `POST /api/v1/inventory/products` | Sin validación de respuesta (response_model) | Retorna raw dict |
| 5 | 🟠 ALTO | `GET /api/v1/inventory/products` | Datos sin serialización explícita | Convierte directamente row a dict |
| 6 | 🟠 ALTO | `POST /api/v1/inventory/locations` | Sin response_model | Devuelve solo `id` y `name` inconsistentemente |
| 7 | 🟠 ALTO | `GET /api/v1/inventory/locations` | Exposición de todas las columnas | Sin filtrado de campos sensibles |

---

## 2. ANÁLISIS DETALLADO POR COMPONENTE

### 2.1 `services/main.py` — Aplicación Principal

#### Hallazgos:

✅ **SEGURO:**
- Los endpoints `/status` y `/health` retornan solo información genérica
- No exponen detalles de la base de datos internos
- Utilizan estructura fija sin riesgo de sobreexposición

#### Recomendaciones:
- Estado actual: **ACEPTABLE** para health checks
- No requiere cambios

---

### 2.2 `src/inventory/router.py` — Rutas de API

#### 🔴 PROBLEMA 1: Endpoint `POST /api/v1/inventory/movements`

**Código actual:**
```python
@router.post("/movements")
def create_movement(m: MovementCreate):
    """Register a new inventory movement."""
    result = service.registrar_movimiento(...)
    return result  # ❌ VULNERABILIDAD: Sin response_model
```

**Vulnerabilidad:**
- La función retorna el diccionario completo de `service.registrar_movimiento()`
- **Campo sensible expuesto:** `unit_price` (información financiera confidencial)
- Un cliente no autorizado puede conocer los costos unitarios de proveedores
- No hay separación entre el modelo interno (para BD) y el modelo público (para cliente)

**Causa raíz:**
1. Falta de decorador `response_model` en el endpoint
2. Reutilización del mismo diccionario para datos internos y externos
3. Sin modelos Pydantic de respuesta exclusivos

**Impacto:**
- 🔴 **CRÍTICO**: Información financiera privada expuesta
- Cumple trazabilidad de costos (violación de confidencialidad)

---

#### 🔴 PROBLEMA 2: Endpoint `GET /api/v1/inventory/movements`

**Código actual:**
```python
@router.get("/movements")
def get_movements(product_id: str, location_id: str):
    """Get movement history for a product at a location."""
    return service.get_historial(product_id, location_id)
    # ❌ VULNERABILIDAD: Sin response_model
```

**Vulnerabilidad:**
- Retorna lista de diccionarios directamente de la BD
- **Campos sensibles:** `unit_price`, `reference` (trazabilidad de costos)
- Historial financiero completo es accesible sin filtro
- No hay validación de qué campos deben ser públicos

**Causa raíz:**
1. Ausencia de `response_model` con schema de respuesta pública
2. Conversión directa `dict(r)` sin transformación de datos
3. Reutilización de modelo de BD como modelo de API

**Impacto:**
- 🔴 **CRÍTICO**: Filtración de información financiera histórica
- Auditoría fiscal/compliance comprometida

---

#### 🔴 PROBLEMA 3: Endpoint `GET /api/v1/inventory/stock`

**Código actual:**
```python
@router.get("/stock")
def get_stock(product_id: str, location_id: str):
    """Get calculated stock for a product at a location."""
    info = service.get_stock_info(product_id, location_id)
    return info  # ❌ Sin response_model
```

**Vulnerabilidad:**
- Retorna estructura interna sin validación de esquema
- Campo `alert` es lógica interna que podría ser modificada
- Sin contrato explícito de respuesta

**Causa raíz:**
1. Falta de `response_model` Pydantic
2. Retorno de diccionario crudo

**Impacto:**
- 🔴 **CRÍTICO**: Contrato de API no garantizado
- Posible sobreexposición de campos futuros si se añaden

---

#### 🟠 PROBLEMA 4: Endpoint `POST /api/v1/inventory/products`

**Código actual:**
```python
@router.post("/products")
def create_product(p: ProductCreate):
    # ... insert logic ...
    return {"id": pid, "name": p.name, "sku": p.sku}  # ❌ Sin response_model
```

**Vulnerabilidad:**
- Sin `response_model` explícito
- Estructura de respuesta no validada
- Si se añaden campos a la BD, podrían exponerse accidentalmente

**Causa raíz:**
1. Respuesta manual sin schema Pydantic
2. Campos seleccionados manualmente sin formalismo

**Impacto:**
- 🟠 **ALTO**: Riesgo de sobreexposición futura

---

#### 🟠 PROBLEMA 5: Endpoint `GET /api/v1/inventory/products`

**Código actual:**
```python
@router.get("/products")
def list_products(category: Optional[str] = None):
    rows = conn.execute("SELECT * FROM products").fetchall()
    return [dict(r) for r in rows]  # ❌ Expone todas las columnas
```

**Vulnerabilidad:**
- `SELECT * FROM products` devuelve todas las columnas de la BD
- Si en el futuro se añaden campos internos (ej: `internal_cost`, `supplier_margin`), se expondrían automáticamente
- Sin validación de respuesta

**Causa raíz:**
1. Query SQL con `SELECT *` en lugar de columnas explícitas
2. Conversión a `dict(r)` sin filtrado
3. Sin `response_model` Pydantic

**Impacto:**
- 🟠 **ALTO**: Riesgo latente de filtración de datos

---

#### 🟠 PROBLEMA 6: Endpoint `POST /api/v1/inventory/locations`

**Código actual:**
```python
@router.post("/locations")
def create_location(l: LocationCreate):
    # ...
    return {"id": lid, "name": l.name}  # ❌ Sin response_model
```

**Vulnerabilidad:**
- Respuesta inconsistente (manual en lugar de modelo)
- Sin validación de estructura

**Causa raíz:**
1. Falta de `response_model` Pydantic
2. Hardcoding de respuesta

**Impacto:**
- 🟠 **ALTO**: Inconsistencia de API

---

#### 🟠 PROBLEMA 7: Endpoint `GET /api/v1/inventory/locations`

**Código actual:**
```python
@router.get("/locations")
def list_locations():
    rows = conn.execute("SELECT * FROM locations").fetchall()
    return [dict(r) for r in rows]  # ❌ Expone todas las columnas
```

**Vulnerabilidad:**
- Igual que en `/products`: `SELECT *` expone todas las columnas sin filtrado
- Sin validación de respuesta

**Causa raíz:**
1. `SELECT *` sin columnas explícitas
2. Sin `response_model`

**Impacto:**
- 🟠 **ALTO**: Riesgo de sobreexposición futura

---

### 2.3 `src/inventory/service.py` — Capa de Servicios

#### Hallazgos:

✅ **ACEPTABLE:**
- La lógica de negocio en la capa de servicios es correcta
- Las funciones `registrar_movimiento()`, `calcular_stock()`, `get_stock_info()`, `get_historial()` son funciones puras sin efectos secundarios de seguridad
- **PERO:** El problema está en que los datos crudos de estas funciones se exponen directamente en los endpoints

#### Recomendación:
- No es necesario modificar `service.py`
- **El filtrado debe ocurrir en la capa de API** mediante `response_model` de Pydantic

---

### 2.4 `src/inventory/models.py` — Modelos de Dominio

#### Hallazgos:

✅ **BIEN:**
- Esquema de BD está correctamente definido
- Campos sensibles están en la BD (correcto: es el almacenamiento)
- Índices de performance están optimizados

⚠️ **FALTA CRÍTICA:**
- No existen modelos Pydantic de **Respuesta (Response/Public)**
- Todos los modelos son de **Entrada (Request)** o modelos de BD

#### Necesidades Identificadas:

1. **Modelos de Request:** ✅ Ya existen (`MovementCreate`, `ProductCreate`, `LocationCreate`)
2. **Modelos de Response/Public:** ❌ **NO EXISTEN** — DEBEN CREARSE

---

## 3. MATRIZ DE PROBLEMAS Y SOLUCIONES

### Tabla de Sobreexposición de Datos

| Endpoint | Método | Datos Sensibles Expuestos | Solución |
|----------|--------|--------------------------|----------|
| `/api/v1/inventory/movements` | POST | `unit_price`, `notes` | `response_model=MovementResponse` |
| `/api/v1/inventory/movements` | GET | `unit_price`, `reference`, `notes` | `response_model=List[MovementHistoryPublic]` |
| `/api/v1/inventory/stock` | GET | Estructura interna | `response_model=StockInfoPublic` |
| `/api/v1/inventory/products` | POST | Ninguno (pero sin validación) | `response_model=ProductResponse` |
| `/api/v1/inventory/products` | GET | Potencial exposición futura | `response_model=List[ProductPublic]` |
| `/api/v1/inventory/locations` | POST | Ninguno (pero sin validación) | `response_model=LocationResponse` |
| `/api/v1/inventory/locations` | GET | Ninguno (pero sin validación) | `response_model=List[LocationPublic]` |

---

## 4. RECOMENDACIONES DE REMEDIACIÓN (FASE 2)

### 4.1 Estrategia de Refactorización

**Separación clara de responsabilidades:**

```
BD (interno)              Servicios (lógica)        API (público)
├─ products              ├─ get_stock_info()      ├─ ProductPublic
├─ locations             ├─ calcular_stock()      ├─ LocationPublic
└─ movements             └─ registrar_movimiento()└─ MovementResponse
```

### 4.2 Modelo Pydantic Recomendado

```python
# INPUTS (Request Models) — Ya existen
class MovementCreate(BaseModel):
    product_id: str
    location_id: str
    movement_type: str
    quantity: float
    unit_price: Optional[float] = None  # ✓ Permitido en entrada
    reference: Optional[str] = None
    notes: Optional[str] = None

# OUTPUTS (Response Models) — DEBEN CREARSE
class MovementResponse(BaseModel):
    id: str
    product_id: str
    location_id: str
    movement_type: str
    quantity: float
    # ❌ unit_price NO se incluye en respuesta pública
    # ❌ reference NO se incluye en respuesta pública
    # ❌ notes NO se incluye en respuesta pública
    created_at: str

class MovementHistoryPublic(BaseModel):
    id: str
    product_id: str
    location_id: str
    movement_type: str
    quantity: float
    created_at: str

class StockInfoPublic(BaseModel):
    product_id: str
    location_id: str
    current_stock: float
    alert: bool

class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    stock_minimo: float
    unit: str
    created_at: str

class ProductPublic(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    unit: str

class LocationResponse(BaseModel):
    id: str
    name: str
    country: str
    city: str

class LocationPublic(BaseModel):
    id: str
    name: str
    country: str
    city: str
```

### 4.3 Implementación en Endpoints

Cada endpoint debe declarar explícitamente su `response_model`:

```python
@router.post("/movements", response_model=MovementResponse)
def create_movement(m: MovementCreate):
    result = service.registrar_movimiento(...)
    return result  # ✓ Automáticamente filtrado por Pydantic

@router.get("/movements", response_model=List[MovementHistoryPublic])
def get_movements(product_id: str, location_id: str):
    return service.get_historial(...)  # ✓ Filtrado automáticamente
```

---

## 5. CONFORMIDAD CON ESTÁNDARES

### 5.1 OWASP Top 10 — Aplicabilidad

| OWASP Risk | Aplicable | Estatus |
|-----------|-----------|--------|
| A01:2021 – Broken Access Control | Parcial | ⚠️ Sin autenticación, pero datos expuestos |
| A04:2021 – Insecure Deserialization | Sí | 🔴 Datos sensibles sin filtrado |
| A05:2021 – Security Misconfiguration | Sí | 🔴 Sin validación de respuesta |

### 5.2 Mejores Prácticas API

| Práctica | Implementado | Estado |
|----------|-------------|--------|
| Separación Request/Response Models | NO | 🔴 Crítico |
| `response_model` en todos los endpoints | NO | 🔴 Crítico |
| Validación Pydantic explícita | Parcial | 🟠 Alto |
| Principio de Least Privilege en datos | NO | 🔴 Crítico |

---

## 6. IMPACTO OPERACIONAL

### 6.1 Riesgos Actuales

- **Confidencialidad:** 🔴 ALTA — Información financiera expuesta
- **Integridad:** 🟢 BAJA — No hay manipulación de datos
- **Disponibilidad:** 🟢 BAJA — No afecta disponibilidad
- **Cumplimiento Legal:** 🔴 ALTA — Posible violación de privacidad de datos

### 6.2 Clientes Afectados

1. **Usuarios externos del API:** Pueden acceder a información financiera sensible
2. **Auditorías internas:** Datos de costos expuestos comprometería auditorías
3. **Competencia:** Información de proveedores y costos filtrada

---

## 7. HOJA DE RUTA DE REMEDIACIÓN

| Fase | Tarea | Tiempo | Prioridad |
|------|-------|--------|-----------|
| 2 | Crear modelos Pydantic de Response | 30 min | 🔴 CRÍTICO |
| 2 | Añadir `response_model` a todos los endpoints | 30 min | 🔴 CRÍTICO |
| 2 | Refactorizar endpoints para filtrar datos | 45 min | 🔴 CRÍTICO |
| 3 | Testing en Docker Compose | 20 min | 🔴 CRÍTICO |
| 4 | Commit y push a `main` | 10 min | 🟠 ALTO |

**Tiempo total estimado:** 2-3 horas

---

## 8. CHECKLIST DE VALIDACIÓN POST-REMEDIACIÓN

- [ ] Modelos de Response creados y documentados
- [ ] Todos los endpoints tienen `response_model` definido
- [ ] No se exponen campos sensibles en respuestas
- [ ] API compila sin errores
- [ ] Endpoints retornan estructura limpia validada
- [ ] Tests de serialización pasan
- [ ] Documentación de API actualizada
- [ ] Commit realizado en `feature/serialization-audit`
- [ ] Pull request abierto a `main`

---

## 9. REFERENCIAS Y DOCUMENTACIÓN

- **FastAPI Docs:** https://fastapi.tiangolo.com/tutorial/response-model/
- **Pydantic:** https://docs.pydantic.dev/
- **OWASP Data Exposure:** https://owasp.org/www-project-top-ten/
- **API Security Best Practices:** https://cheatsheetseries.owasp.org/

---

**Documento preparado por:** Senior Backend Developer  
**Fecha:** 4 de noviembre de 2026  
**Estado:** ✅ AUDITORÍA COMPLETADA  
**Próximo paso:** FASE 2 — IMPLEMENTACIÓN DE REMEDIACIÓN
