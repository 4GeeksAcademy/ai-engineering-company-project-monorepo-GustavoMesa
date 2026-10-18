# Tech Context — Brasaland Digital

## Stack Tecnológico

| Componente | Tecnología | Propósito |
|---|---|---|
| Backend API | Python 3.11 + FastAPI 0.110 | API REST central |
| Frontend | Node.js 18 Alpine | Website + Backoffice |
| Base de datos | SQLite (dev), PostgreSQL (prod) | Datos operacionales |
| Orquestación | Docker Compose 3.8 | 2 servicios (uis + backend) |
| Gestor Python | uv | Instalación de dependencias |
| Control versiones | Git + GitHub | Código fuente |

## Arquitectura del Monorepo

```
├── CONTEXT.md          ← Briefing de Brasaland
├── docker-compose.yml  ← Orquestación local
├── services/           ← Backend FastAPI
├── uis/                ← Frontends (website + backoffice)
├── agents/             ← Agentes IA
├── skills/             ← Capacidades de agente
├── data/               ← Pipelines ETL
├── workflows/          ← Automatización n8n
├── mcps/               ← Servidores MCP
├── specs/              ← Especificaciones EARS
├── docs/               ← Documentación técnica
├── memory-bank/        ← Memoria del proyecto
├── src/                ← Código de implementación
└── .agent/             ← Reglas del agente
```

## Restricciones Técnicas

1. **Stock derivado**: El stock NO es un campo CRUD. Siempre se calcula como agregación de movimientos.
2. **Movimientos inmutables**: No se modifican ni eliminan. Correcciones vía movimiento compensatorio.
3. **Stock negativo prohibido**: Validar antes de cada salida/merma.
4. **API centralizada**: Todos los endpoints bajo `/api/v1/`.
5. **Datos bilingües**: La documentación existe en español e inglés.
6. **Sin secrets en código**: Usar variables de entorno o Secrets Store.