# Incidencia: Falta de registro centralizado de incidencias

**Fecha:** 17 de octubre de 2026
**Detectada por:** Auditoría Paso 1
**Canal de origen:** Sistema local
**Tipo:** violacion_regla
**Regla aplicable:** TRAZABILIDAD_INCIDENCIAS (regla 4 de `.agent/rules/agent-rules.md`)
**Severidad:** 🔴 Alta

## Descripción
El repositorio no cuenta con un sistema de registro centralizado de incidencias. No existe `docs/incidencias/`, `SKILL_LOG.md` ni ningún mecanismo de trazabilidad para problemas detectados en el workspace. Cualquier hallazgo se pierde sin seguimiento.

## Acción correctiva aplicada
1. ✅ Creado el directorio `docs/incidencias/` para almacenar incidencias
2. ✅ Creado `SKILL_LOG.md` como bitácora de integraciones
3. ✅ Creada la skill `skills/gestionar-incidencias/SKILL.md` con clasificación por canal, tipo y severidad
4. ✅ Definidas reglas en `.agent/rules/agent-rules.md` que exigen trazabilidad
5. ✅ Actualizado `memory-bank/README.md` con catálogo de incidencias

## Estado
**Resuelta** — sistema de trazabilidad implementado.