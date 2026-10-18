# SKILLS.md — Flujo de Trabajo Autónomo del Agente

## Propósito
Formalizar el flujo de trabajo que el agente sigue al recibir una tarea en el contexto de Brasaland, garantizando consistencia, trazabilidad y alineación con la rúbrica de evaluación.

---

## Flujo de Trabajo Estándar

### 1. INICIO — Recepción de Tarea
- Analizar la solicitud y extraer: rama a usar, archivos a crear/modificar, criterios de aceptación, entregables esperados.
- Verificar repositorio correcto (`ai-engineering-company-project-monorepo-GustavoMesa`).
- Verificar rama activa; si no existe, crearla con nombre `feature/<nombre>`.

### 2. EJECUCIÓN — Por Fases/Entregables
- Dividir la tarea en fases lógicas (Spec, Plan, Implement, Verify).
- Cada fase recibe un commit independiente con mensaje convencional.
- Seguir las reglas del proyecto:
  - `AGENTS.md` para directivas imperativas.
  - `.agent/rules/agent-rules.md` para reglas específicas.
  - `memory-bank/` para contexto del proyecto.

### 3. VERIFICACIÓN — Validación de Criterios
- Antes de cerrar cada fase, verificar que los criterios de aceptación EARS se cumplen.
- Documentar resultados en `verification_report.md` cuando corresponda.
- Si hay fallos, corregir antes de continuar.

### 4. CIERRE — Push y Merge
- Pushear la rama feature.
- Hacer merge a `main`.
- Sincronizar con GitHub (`git push origin main`).

---

## Árbol de Decisión para el Agente

```
¿La tarea tiene criterios EARS?
├── Sí → Crear spec.md primero, luego implementar
│        ¿El módulo afecta inventario?
│        ├── Sí → Aplicar regla STOCK_DERIVED
│        └── No → Seguir spec estándar
└── No → Ejecutar en un único commit

¿Hay rama feature?
├── Sí → Trabajar en ella
└── No → git checkout -b feature/<nombre>

¿Todos los criterios verificados?
├── Sí → Push + merge a main
└── No → Iterar hasta cumplir
```

---

## Convenciones de Commit

| Prefijo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad (código) |
| `docs:` | Documentación (specs, plan, tasks, memory-bank) |
| `test:` | Verificación, reportes de test |
| `fix:` | Corrección de errores |
| `chore:` | Mantenimiento, configuración |

Formato: `<prefijo>(<ámbito>): <descripción en español>`

---

## Recordatorios Críticos

- **Stock es derivado**: nunca escribir stock directamente como campo CRUD.
- **Movimientos inmutables**: una vez registrados, no se modifican ni eliminan.
- **EARS primero**: toda implementación empieza con especificación.
- **Un commit por fase**: mantener trazabilidad granular por entregable.
- **No hacer push directo a main**: siempre via rama feature + merge.