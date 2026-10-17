# Entrada Inicial de Inventario — Brasaland

**Fecha:** 17 de octubre de 2026
**Propósito:** Datos semilla para pruebas del Gestor de Inventario.

## Productos Registrados

| SKU | Producto | Unidad | Stock Mínimo |
|---|---|---|---|
| CAR-001 | Carne de res (entraña) | kg | 50 |
| POL-001 | Pechuga de pollo | kg | 30 |
| ARE-001 | Arepa paisa | unidades | 100 |
| BBQ-001 | Salsa BBQ Brasaland | L | 20 |
| PAP-001 | Papas criollas | kg | 80 |

## Locales Registrados

| ID | Nombre | País | Ciudad |
|---|---|---|---|
| loc-med-01 | Sede Principal Medellín | Colombia | Medellín |
| loc-mia-01 | Brasaland Miami - Little Havana | USA | Miami |

## Movimientos Iniciales

### Medellín — Entradas (stock inicial)
| Producto | Cantidad | Precio Unitario | Referencia |
|---|---|---|---|
| Carne de res | 200 kg | $12.50 | FAC-001 |
| Pechuga de pollo | 100 kg | $8.30 | FAC-001 |
| Arepa paisa | 500 und | $0.85 | FAC-002 |
| Salsa BBQ | 40 L | $5.00 | FAC-003 |
| Papas criollas | 150 kg | $1.20 | FAC-001 |

### Medellín — Salidas (consumo)
| Producto | Cantidad | Referencia |
|---|---|---|
| Carne de res | 30 kg | VEN-001 |
| Arepa paisa | 80 und | VEN-001 |

### Miami — Entradas (stock inicial)
| Producto | Cantidad | Precio Unitario | Referencia |
|---|---|---|---|
| Carne de res | 150 kg | $14.00 | INV-MIA-001 |
| Arepa paisa | 300 und | $1.10 | INV-MIA-001 |
| Salsa BBQ | 25 L | $6.50 | INV-MIA-001 |

## Stocks Calculados (después de movimientos iniciales)

| Local | Producto | Stock | Alerta |
|---|---|---|---|
| Medellín | Carne de res | 170 kg | ✅ Normal |
| Medellín | Pechuga de pollo | 100 kg | ✅ Normal |
| Medellín | Arepa paisa | 420 und | ✅ Normal |
| Medellín | Salsa BBQ | 40 L | ✅ Normal |
| Medellín | Papas criollas | 150 kg | ✅ Normal |
| Miami | Carne de res | 150 kg | ✅ Normal |
| Miami | Arepa paisa | 300 und | ✅ Normal |
| Miami | Salsa BBQ | 25 L | ✅ Normal |