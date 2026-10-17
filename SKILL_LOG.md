# SKILL_LOG.md — Registro de Integración

## Proyecto: Backoffice de Operaciones – Gestor de Incidencias

---

## Skills Registradas

### Skill 1: Gestor de Incidencias
- **Prompt:** "Evalúa, clasifica y centraliza incidencias críticas del workspace usando las reglas de .agent/rules/."
- **Descripción:** Skill de infraestructura que ejecuta healthcheck del entorno, clasifica incidencias por canal (Telegram, API, MCP, sistema), tipo (skill_obsoleta, integracion_caida, violacion_regla, archivo_huertano) y severidad (🔴 Alta, 🟡 Media, 🔵 Baja), registrando cada hallazgo en `docs/incidencias/` con trazabilidad completa.
- **Fecha de creación:** 17 de octubre de 2026
- **Rama:** `feature/incident-manager`
- **Archivo de skill:** `skills/gestionar-incidencias/SKILL.md`

---

## Incidencias Documentadas

| ID | Fecha | Tipo | Severidad | Archivo | Estado |
|---|---|---|---|---|---|
| INC-001 | 17 oct 2026 | violacion_regla | 🔴 Alta | `docs/incidencias/2026-10-17--falta-registro-incidencias.md` | Resuelta |

---

## Skills Registradas (Inventory Manager)

### Skill 2: Inventory Manager
- **Prompt:** "Gestiona el inventario de Brasaland calculando el stock exclusivamente a partir de movimientos (entradas, salidas, mermas)."
- **Descripción:** Sistema de gestión de inventario con stock derivado de movimientos. Implementa endpoints REST para registrar movimientos, consultar stock calculado en tiempo real, y obtener historial. Valida stock negativo antes de salidas/mermas.
- **Fecha de creación:** 17 de octubre de 2026
- **Rama:** `feature/inventory-manager`
- **Archivos:** `src/inventory/` (models.py, service.py, router.py)
- **Especificación EARS:** `specs/inventory-manager/spec.md` (INV-001 a INV-006)

---

## Incidencias Documentadas

| ID | Fecha | Tipo | Severidad | Archivo | Estado |
|---|---|---|---|---|---|
| INC-001 | 17 oct 2026 | violacion_regla | 🔴 Alta | `docs/incidencias/2026-10-17--falta-registro-incidencias.md` | Resuelta |

---

## Reglas Aplicables

Las reglas del proyecto están definidas en `.agent/rules/agent-rules.md`:
1. ESQUEMA_ESTRICTO_FRONTMATTER
2. CLASIFICACION_INCIDENCIAS
3. HEALTHCHECK_OBLIGATORIO
4. TRAZABILIDAD_INCIDENCIAS
5. SKILL_LOG_ACTUALIZADO
6. RESTRICCION_DATOS
7. COMMIT_CONVENTION