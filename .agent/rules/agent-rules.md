# Reglas de Comportamiento — Gestor de Incidencias

## 1. ESQUEMA_ESTRICTO_FRONTMATTER
**Directiva:** Todo archivo SKILL.md debe incluir obligatoriamente en su YAML frontmatter los campos `name`, `description` y `emoji`. Ninguna skill puede crearse sin estos tres campos.

## 2. CLASIFICACION_INCIDENCIAS
**Directiva:** Toda incidencia debe clasificarse por: canal de origen (Telegram, API, MCP, sistema), tipo (skill_obsoleta, integracion_caida, violacion_regla, archivo_huertano) y severidad (🔴 Alta, 🟡 Media, 🔵 Baja).

## 3. HEALTHCHECK_OBLIGATORIO
**Directiva:** Toda skill que dependa de servicios externos debe incluir un paso 0 de verificación de conectividad antes del procedimiento principal. Si falla, abortar.

## 4. TRAZABILIDAD_INCIDENCIAS
**Directiva:** Cada incidencia detectada debe registrarse en `docs/incidencias/` con fecha, descripción, regla aplicable, criticidad y estado. No cerrar sin verificación.

## 5. SKILL_LOG_ACTUALIZADO
**Directiva:** Toda skill creada debe registrarse en `SKILL_LOG.md` con prompt, endpoint, resultado de prueba y archivo de skill.

## 6. RESTRICCION_DATOS
**Directiva:** No exponer tokens, URLs internas ni datos sensibles en archivos visibles, logs o commits. Usar siempre Secrets Store.

## 7. COMMIT_CONVENTION
**Directiva:** Usar prefijos convencionales (`feat:`, `fix:`, `docs:`, `chore:`, `test:`) en mensajes de commit.