# Hallazgos y Propuestas de Reglas — Brasaland / Dashboard Financiero

**Fecha:** 17 de octubre de 2026
**Repositorio:** `ai-engineering-company-project-monorepo-GustavoMesa`

---

## Hallazgos Detectados

| # | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| 1 | **CONTEXT.md sin reemplazar** — El briefing de Brasaland no se ha copiado al archivo `CONTEXT.md`. Sigue siendo un placeholder. | `CONTEXT.md` contiene instrucciones de plantilla, no datos de la empresa. | 🔴 Alto — Sin contexto de empresa, ningún agente o skill puede operar con datos reales. |
| 2 | **Monorepo con estructura por capas** — El repositorio está organizado en capas claras (uis, services, data, agents, skills, workflows, infra, etc.) pero sin código de implementación real. | Solo existen templates y READMEs. `agents/_template/agent.py` está vacío. `services/` no tiene `main.py`. `uis/` no tiene carpetas `website/` ni `backoffice/`. | 🟡 Medio — La estructura está lista pero no hay código funcional. |
| 3 | **Docker Compose con 2 servicios** — `uis` (Node.js) y `backend` (FastAPI) están configurados pero el backend no tiene `main.py` y los UIs no tienen carpetas de proyecto. | `docker-compose.yml` referencia servicios que no pueden arrancar porque falta código fuente. | 🟡 Medio — La orquestación está definida pero no es ejecutable. |
| 4 | **Bilingüe consistente** — Toda documentación existe en español e inglés, lo cual es una buena práctica para equipos multilingües. | README.es.md y README.md en cada carpeta. | ✅ Bueno — Mantener esta convención. |
| 5 | **Sin tests ni CI/CD** — No hay archivos de test, GitHub Actions ni pipelines de integración continua. | No existe `tests/`, `.github/workflows/`, ni referencias a testing. | 🟡 Medio — Sin tests, no hay garantía de calidad. |
| 6 | **Sin base de datos definida** — No hay schema SQL, migraciones, ORM configurado ni servicio de base de datos en docker-compose. | Aunque el backend tiene FastAPI + Pydantic, no hay conexión a DB configurada. | 🔴 Alto — Una aplicación financiera sin base de datos no es funcional. |
| 7 | **Dependencias de Python sin fijar** — `requirements.txt` usa versiones exactas pero falta `sqlalchemy`, `alembic`, `httpx` y otras dependencias típicas de un backend financiero. | Solo tiene fastapi, uvicorn, pydantic y python-dotenv. | 🟡 Medio — Las dependencias actuales son mínimas, crecerán con el desarrollo. |
| 8 | **La skill `code-review` está vacía** — Existe `skills/code-review/.gitkeep` pero no hay `SKILL.md` ni código. | El directorio skills tiene template y code-review, pero code-review no tiene implementación. | 🔵 Bajo — Template preparado pero skill sin contenido. |

---

## Propuestas de Reglas para el Repositorio

### Regla 1: CONTEXT_REQUIRED
**Directiva:** El archivo `CONTEXT.md` debe contener el briefing completo de la empresa asignada (Brasaland) antes de cualquier implementación. Ningún agente, skill ni servicio debe referenciar datos de la empresa sin antes verificar que `CONTEXT.md` tiene el contenido real.

### Regla 2: CODE_BEFORE_INFRA
**Directiva:** No agregar configuraciones de infraestructura (Docker, despliegue, CI/CD) sin tener primero el código funcional correspondiente. El `docker-compose.yml` solo debe referenciar servicios que tengan código ejecutable.

### Regla 3: MONOREPO_LAYERS
**Directiva:** Cada directorio raíz tiene una responsabilidad única y no debe contener código de otra capa. `uis/` solo tiene frontends, `services/` solo backends, `agents/` solo agentes IA, etc.

### Regla 4: BILINGUAL_DOCS
**Directiva:** Toda documentación debe existir en español e inglés (`.md` + `.es.md`). Mantener la convención existente.

### Regla 5: DATABASE_FIRST
**Directiva:** Para aplicaciones financieras, definir el schema de base de datos y las migraciones antes de implementar endpoints de API. No crear rutas FastAPI sin tener el modelo de datos correspondiente.

### Regla 6: SKILL_WITH_SKILLMD
**Directiva:** Toda skill nueva en `skills/` debe tener su propio `SKILL.md` con frontmatter YAML (`name`, `description`, `emoji`) y procedimiento numerado. No dejar skills sin contenido.

### Regla 7: COMMIT_CONVENTION
**Directiva:** Los mensajes de commit deben usar prefijos convencionales (`feat:`, `fix:`, `docs:`, `chore:`, `test:`) seguidos de una descripción en español o inglés.

---

*Documento generado como parte de la FASE 2 — Definición de Hallazgos y Propuestas de Reglas.*