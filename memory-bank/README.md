# 🚨 Brasaland — Gestor de Incidencias (Banco de Memoria)

## Contexto del Negocio

**Brasaland** es una cadena de restaurantes de cocina a la brasa con 14 locales en Colombia y Florida. Este proyecto implementa un **Backoffice de Operaciones – Gestor de Incidencias** para centralizar el registro, clasificación y trazabilidad de problemas técnicos y operativos del workspace del agente.

### Problemas a Resolver
- No existe registro centralizado de incidencias
- No hay clasificación por canal, tipo o severidad
- No hay trazabilidad de correcciones aplicadas
- No hay healthcheck de integraciones externas
- Skills sin registro ni control de calidad

---

## Stack Tecnológico del Proyecto

| Componente | Tecnología | Propósito |
|---|---|---|
| Plataforma agente | OpenClaw v2026.9.7 | Orquestador del agente conversacional |
| Canal comunicación | Telegram Bot API | Interfaz con el usuario |
| API educativa | BreatheCode REST API | Datos académicos |
| Integración Google | Zapier MCP | Drive / Calendar |
| Almacén secreto | OpenClaw Secrets Store | Tokens cifrados |
| Control versiones | Git + GitHub | Trazabilidad de cambios |

---

## Estado Actual de Skills

| Skill | Estado | Última prueba |
|---|---|---|
| `gestionar-incidencias` | ✅ Creada en este proyecto | 17 oct 2026 |
| Otras skills | ❌ No implementadas en este repositorio | — |

---

## Catálogo de Incidencias

| ID | Fecha | Tipo | Severidad | Estado |
|---|---|---|---|---|
| INC-001 | 17 oct 2026 | skill_obsoleta_sin_filtro | 🔴 Alta | Resuelta |

---

## Convenciones del Proyecto

- **Rama de trabajo:** `feature/incident-manager`
- **Commits:** Prefijos convencionales (`feat:`, `fix:`, `docs:`, `chore:`)
- **Incidencias:** Registro en `docs/incidencias/` con formato `YYYY-MM-DD--<tipo>.md`
- **Skills:** Frontmatter YAML con `name`, `description`, `emoji`, `status`
- **Healthcheck:** Paso 0 obligatorio en skills con dependencias externas

---

*Última actualización: 17 de octubre de 2026 — Paso 3*