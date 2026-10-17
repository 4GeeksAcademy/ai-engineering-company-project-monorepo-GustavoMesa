# Reglas de Comportamiento — Proyecto Brasaland

## 1. CONTEXT_REQUIRED
**Directiva:** El archivo `CONTEXT.md` debe contener el briefing completo de la empresa asignada (Brasaland) antes de cualquier implementación. Ningún agente, skill ni servicio debe operar sin verificar que `CONTEXT.md` tiene datos reales.

## 2. CODE_BEFORE_INFRA
**Directiva:** No agregar configuraciones de infraestructura (Docker, despliegue, CI/CD) sin tener primero el código funcional correspondiente. El `docker-compose.yml` solo debe referenciar servicios ejecutables.

## 3. MONOREPO_LAYERS
**Directiva:** Cada directorio raíz tiene una responsabilidad única. `uis/` solo frontends, `services/` solo backends, `agents/` solo agentes IA, `data/` solo datos.

## 4. DATABASE_FIRST
**Directiva:** Definir schema de base de datos y migraciones antes de implementar endpoints de API. No crear rutas FastAPI sin tener el modelo de datos correspondiente.

## 5. SKILL_WITH_SKILLMD
**Directiva:** Toda skill nueva en `skills/` debe tener su `SKILL.md` con frontmatter YAML (`name`, `description`, `emoji`) y procedimiento numerado.

## 6. BILINGUAL_DOCS
**Directiva:** Mantener documentación en español e inglés (`.md` + `.es.md`) como estándar del repositorio.

## 7. COMMIT_CONVENTION
**Directiva:** Usar prefijos convencionales (`feat:`, `fix:`, `docs:`, `chore:`, `test:`) en commits.