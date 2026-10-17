# 🏦 Brasaland — Banco de Memoria del Proyecto

## Contexto del Negocio

**Brasaland** es una cadena de restaurantes de cocina a la brasa fundada en 2008 en Medellín, Colombia. Opera **14 restaurantes propios** en dos países (Colombia y Florida, EE.UU.), emplea a **115 personas** y factura **~6 millones USD anuales**.

### Problemas Clave
- Pedidos de materia prima por WhatsApp sin datos de inventario
- Programa de fidelización con tarjetas físicas que los clientes pierden
- Sin visibilidad en tiempo real de las operaciones de cada local
- Equipo directivo sin capacidad de responder preguntas básicas sin llamar
- Dos mercados (Colombia y USA) con monedas, leyes y culturas distintas

### Organización
| Área | Líder | Función |
|---|---|---|
| Operaciones de Restaurante | Felipe Guerrero | Corazón del negocio, supervisa los 14 locales |
| Compras y Proveedores | Lucía Fernández | 20 proveedores, negociación en cada mercado |
| Marketing y Experiencia Digital | Camila Ospina | Web, redes, fidelización, campañas |
| Personas y Cultura | Ashley Turner | RRHH, contratos, horarios (115 personas) |
| Formación y Estándares de Calidad | Jake Morrison | Estandarización de recetas y procedimientos |
| Tecnología | Nicolás Park (CTO) | Stack mínimo: web estática, app obsoleta, hojas de cálculo |
| Dirección Ejecutiva | Mariana Restrepo (CEO) | Decisiones basadas en llamadas y PDFs semanales |

---

## Stack Tecnológico del Proyecto

| Componente | Tecnología | Propósito |
|---|---|---|
| Orquestación | Docker Compose 3.8 | 2 servicios: `uis` + `backend` en red bridge |
| Backend API | Python 3.11 + FastAPI 0.110 | API REST financiera |
| Servidor ASGI | Uvicorn 0.28 | Servidor web con hot-reload |
| Frontend Website | Node.js 18 Alpine | Sitio web público (puerto 3000) |
| Frontend Backoffice | Node.js 18 Alpine | Panel administrativo (puerto 3001) |
| Paquete compartido | npm `@repo/shared-types` 0.0.1 | Tipos TypeScript compartidos |
| Gestor Python | `uv` | Instalación de dependencias |

---

## Estado Actual del Repositorio

### ✅ Implementado
- ☑ Estructura completa del monorepo por capas (10 directorios)
- ☑ `docker-compose.yml` con 2 servicios (uis + backend)
- ☑ Dockerfiles para backend (Python) y frontend (Node.js)
- ☑ Documentación bilingüe (ES/EN) en cada carpeta
- ☑ Plantillas de agentes (`agents/_template/`) y skills (`skills/_template/`)
- ☑ Elección de empresa documentada (`company-choice.es.md`)
- ☑ Briefing de Brasaland disponible (`CONTEXT-Brasaland-Briefing.es.md`)

### ❌ Por Implementar
- ❌ `CONTEXT.md` sigue siendo placeholder — NO se ha copiado el briefing de Brasaland
- ❌ No hay `main.py` en `services/` — el backend FastAPI no arranca
- ❌ No hay `website/` ni `backoffice/` en `uis/` — los frontends no existen
- ❌ No hay base de datos definida (schema SQL, migraciones, ORM)
- ❌ No hay tests (`tests/`, CI/CD, GitHub Actions)
- ❌ No hay `.env` file configurado
- ❌ Skills `code-review` y `_template` están vacías sin SKILL.md

---

## Rechazo de Features / Suposiciones Inventadas

| Afirmación | Realidad | Evidencia |
|---|---|---|
| "El repositorio tiene un Dashboard Financiero implementado" | ❌ **Falso.** No hay ningún dashboard, gráfico,报表 ni visualización financiera en el código. La estructura de capas está preparada pero vacía. | `find . -name "*.html" -o -name "*.jsx" -o -name "*.tsx"` no devuelve archivos de UI reales |
| "El backend FastAPI está funcional" | ❌ **Falso.** No existe `main.py`, `routes/`, `models/` ni `schemas/` en `services/`. Solo hay Dockerfile y requirements.txt. | `ls services/` solo muestra archivos de configuración |
| "Hay base de datos conectada" | ❌ **Falso.** No hay `docker-compose` con servicio de BD, ni archivos SQL, ni migraciones, ni ORM configurado. | Buscar `postgres`, `mysql`, `sqlite` en `docker-compose.yml` y requirements.txt no da resultados |
| "La aplicación es funcional y se puede desplegar" | ❌ **Falso.** `docker-compose up` fallaría porque los servicios referencian código que no existe (`website/`, `backoffice/`, `main.py`). | `uis/start.sh` condiciona la ejecución a `if [ -d "website" ]` — la carpeta no existe |
| "Hay autenticación de usuarios" | ❌ **Falso.** No hay endpoints de auth, middleware, JWT, sesiones ni nada relacionado. | No hay archivos de login, auth ni usuarios en ninguna carpeta |
| "El proyecto tiene CI/CD implementado" | ❌ **Falso.** No hay GitHub Actions, `.gitlab-ci.yml` ni scripts de deploy. | Buscar `.github/` o archivos `*ci*` no da resultados |
| "Las skills de IA están operativas" | ❌ **Falso.** `skills/_template/SKILL.md` está vacío. `skills/code-review/` solo tiene un `.gitkeep`. | `cat skills/_template/SKILL.md` no devuelve contenido |
| "El agente de IA está implementado" | ❌ **Falso.** `agents/_template/agent.py` está vacío. Solo existe la estructura de directorio. | `cat agents/_template/agent.py` no devuelve contenido |

### Conclusión
Este repositorio es una **plantilla inicial** con la estructura de directorios y configuración de infraestructura, pero **no contiene código funcional**. Es el punto de partida sobre el cual se construirá el Dashboard Financiero de Brasaland. Todas las afirmaciones de funcionalidad operativa son falsas hasta que se implemente el código correspondiente.

---

## Convenciones del Proyecto

- **Monorepo por capas:** Cada directorio raíz tiene responsabilidad única
- **Documentación bilingüe:** ES + EN en cada carpeta
- **Docker first:** Todo servicio debe tener Dockerfile funcional antes de integrarse
- **Base de datos primero:** Schema y migraciones antes que endpoints
- **Commits con prefijo:** `feat:`, `fix:`, `docs:`, `chore:`, `test:`

---

*Última actualización: 17 de octubre de 2026 — Fase 4 completada*