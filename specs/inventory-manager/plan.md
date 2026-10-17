# Inventory Manager — Plan Técnico

## Objetivo
Implementar un sistema de gestión de inventario para Brasaland donde el stock se calcula exclusivamente a partir de movimientos (entradas, salidas, mermas). NO hay campo de stock editable.

---

## Arquitectura

```
src/inventory/
├── models.py          # Entidades Product, Location, InventoryMovement
├── schemas.py         # Pydantic schemas para requests/responses
├── service.py         # Lógica de negocio (cálculo de stock, validaciones)
├── router.py          # Endpoints FastAPI
└── database.py        # Conexión y operaciones SQLite

data/raw/inventario/   # Datos de entrada (CSV de ejemplo)
docs/inventario/       # Documentación y registro inicial
specs/inventory-manager/  # Especificaciones EARS, plan y tareas
```

---

## Stack Técnico

| Componente | Tecnología |
|---|---|
| Backend API | FastAPI 0.110 (Python 3.11) |
| Base de datos | SQLite (sqlite3, sin ORM pesado) |
| Validación | Pydantic 2.6 |
| Testing | pytest (a implementar) |

---

## Fases de Desarrollo

| Fase | Actividades | Entregables |
|---|---|---|
| **Fase 1 (Specify)** | Definir entidades, reglas de dominio, criterios EARS | `specs/inventory-manager/spec.md` ✅ |
| **Fase 2 (Plan)** | Desglose técnico, arquitectura, fases | `specs/inventory-manager/plan.md` 🔄 |
| **Fase 3 (Tasks)** | Tareas atómicas verificables | `specs/inventory-manager/tasks.md` |
| **Fase 4 (Implement)** | Código: modelos, endpoints, lógica de stock | `src/inventory/`, `docs/inventario/` |
| **Fase 5 (Verify)** | Tests EARS, reporte, cambio de requisito | Actualización de specs y código |

---

## Decisiones Técnicas

1. **SQLite** para simplicidad. En producción sería PostgreSQL, pero para este ejercicio SQLite basta.
2. **Stock = función agregada** de la tabla `inventory_movements`. No hay tabla `stock`.
3. **Movimientos inmutables.** Una vez insertados no se modifican ni eliminan. Para corregir, movimiento compensatorio.
4. **Validación de stock negativo** en la capa de servicio antes de insertar SALIDA o MERMA.
5. **Endpoints REST** bajo el prefijo `/api/v1/inventory/`.

---

## Endpoints Planeados

| Método | Ruta | Descripción | Requisito EARS |
|---|---|---|---|
| POST | `/api/v1/inventory/movements` | Registrar movimiento | INV-001 |
| GET | `/api/v1/inventory/stock` | Consultar stock calculado | INV-002, INV-003, INV-005 |
| GET | `/api/v1/inventory/movements` | Historial de movimientos | INV-004 |
| POST | `/api/v1/inventory/products` | Crear producto | — |
| GET | `/api/v1/inventory/products` | Listar productos | — |
| POST | `/api/v1/inventory/locations` | Crear local | — |
| GET | `/api/v1/inventory/locations` | Listar locales | — |

---

*Documento generado como parte de la Fase 2 — Plan.*