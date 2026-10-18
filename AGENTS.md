# AGENTS.md — Brasaland Digital

## ¿Qué es Brasaland?
Cadena de 14 restaurantes de cocina a la brasa en Colombia y Florida. Este repositorio contiene el ecosistema digital del equipo **Brasaland Digital** para centralizar operaciones, automatizar procesos y habilitar decisiones basadas en datos.

---

## Reglas Imperativas de Desarrollo

### 1. STOCK_DERIVED
**Directiva:** El stock NO es un campo CRUD editable. Siempre se calcula como `SUM(entradas) - SUM(salidas) - SUM(mermas)`. Ningún endpoint debe permitir escribir un valor de stock directamente.

### 2. MOVEMENTS_IMMUTABLE
**Directiva:** Los movimientos de inventario son inmutables. Una vez registrados no se modifican ni eliminan. Para corregir errores, registrar un movimiento compensatorio.

### 3. NEGATIVE_STOCK_FORBIDDEN
**Directiva:** Validar stock suficiente antes de cada SALIDA o MERMA. Si `cantidad > stock_actual`, rechazar con error 422.

### 4. EARS_FIRST
**Directiva:** Todo nuevo módulo debe comenzar con especificación EARS en `specs/` antes de escribir código. Los criterios de aceptación usan identificadores únicos (INV-001, etc.).

### 5. MONOREPO_LAYERS
**Directiva:** Cada directorio raíz tiene responsabilidad única. No mezclar capas. `src/` para implementación, `specs/` para especificaciones, `docs/` para documentación.

### 6. COMMIT_CONVENTION
**Directiva:** Usar prefijos convencionales: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.

---

## Archivos/Carpetas que el Agente NO Debe Modificar Sin Confirmación

| Ruta | Motivo |
|---|---|
| `CONTEXT.md` | Briefing oficial de Brasaland — solo actualizar con contenido proporcionado por el usuario |
| `docker-compose.yml` | Orquestación de servicios — cambios sin coordinación pueden romper el entorno dev |
| `services/Dockerfile` | Configuración del backend — requiere coordinación con el equipo |
| `uis/Dockerfile` | Configuración del frontend — requiere coordinación con el equipo |
| `data/raw/` | Datos crudos de entrada — no modificar sin autorización |
| `src/inventory/` | Código del Gestor de Inventario — solo modificar siguiendo las reglas EARS y con validación |

---

## Política de Commits
- Un commit por fase/entregable
- Mensajes en español con prefijo convencional
- No hacer push directo a main sin merge desde rama feature
- Mantener ramas feature con nombre `feature/<nombre>`