---
name: gestionar-incidencias
description: "Evalúa, clasifica y centraliza incidencias críticas del workspace usando las reglas de .agent/rules/."
metadata: { "openclaw": { "emoji": "🚨" } }
status: active
---

# Gestor de Incidencias

Usar para detectar, clasificar, registrar y dar trazabilidad a incidencias técnicas del workspace. Clasifica por canal de origen, tipo y severidad.

## Procedimiento

0. **Healthcheck del entorno:** Verificar que `.agent/rules/agent-rules.md` existe, que `docs/incidencias/` es accesible y que el repositorio está limpio (git status). Si falla, abortar.

1. Clasificar la incidencia:
   a) **Canal de origen:** Telegram, API BreatheCode, Zapier MCP, sistema local.
   b) **Tipo:** skill_obsoleta, integracion_caida, violacion_regla, archivo_huertano.
   c) **Severidad:** 🔴 Alta (bloqueante), 🟡 Media (funcionalidad afectada), 🔵 Baja (cosmética).

2. Crear archivo en `docs/incidencias/` con formato `YYYY-MM-DD--<tipo>.md` incluyendo:
   - Fecha, descripción, regla aplicable de `.agent/rules/`, criticidad, acción tomada y estado.

3. Si la incidencia es `skill_obsoleta`: verificar metadato `status` en frontmatter del SKILL.md. Si es `obsolete`, no ejecutar e informar.

4. Si es `integracion_caida`: ejecutar healthcheck de conectividad (curl, ping o MCP). Informar código de error exacto.

5. Cerrar la incidencia actualizando su estado a "resuelta" cuando se verifique la corrección.

## Salida esperada
Reporte estructurado con tipo, fecha, regla violada, criticidad, acción y estado final.

## Notes
- No duplicar incidencias para el mismo hallazgo.
- Respetar el formato de nombre de archivo `YYYY-MM-DD--<tipo>.md`.
- Esta skill cumple con ESQUEMA_ESTRICTO_FRONTMATTER (regla 1) y HEALTHCHECK_OBLIGATORIO (regla 3).