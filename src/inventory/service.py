"""
Inventory Manager — Service layer with stock calculation logic.
Stock is ALWAYS derived from movements, never stored directly.
"""
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional

from . import models


def calcular_stock(product_id: str, location_id: str) -> float:
    """Calculate current stock as SUM(entradas) - SUM(salidas) - SUM(mermas)."""
    conn = models.get_connection()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN movement_type = 'ENTRADA' THEN quantity ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN movement_type IN ('SALIDA', 'MERMA') THEN quantity ELSE 0 END), 0)
            AS current_stock
        FROM inventory_movements
        WHERE product_id = ? AND location_id = ?
        """,
        (product_id, location_id),
    ).fetchone()
    conn.close()
    return row[0]


def get_stock_info(product_id: str, location_id: str) -> dict:
    """Get stock info with alert flag."""
    conn = models.get_connection()
    stock = calcular_stock(product_id, location_id)
    min_stock = conn.execute(
        "SELECT stock_minimo FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    min_val = min_stock[0] if min_stock else 0
    return {
        "product_id": product_id,
        "location_id": location_id,
        "current_stock": stock,
        "alert": stock < min_val,
    }


def registrar_movimiento(
    product_id: str,
    location_id: str,
    movement_type: str,
    quantity: float,
    unit_price: Optional[float] = None,
    reference: Optional[str] = None,
    notes: Optional[str] = None,
) -> dict:
    """Register a movement. Validates stock before SALIDA or MERMA."""
    conn = models.get_connection()

    # Validate product and location exist
    product = conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product:
        conn.close()
        raise ValueError(f"Product {product_id} not found")

    location = conn.execute("SELECT id FROM locations WHERE id = ?", (location_id,)).fetchone()
    if not location:
        conn.close()
        raise ValueError(f"Location {location_id} not found")

    # Validate stock for SALIDA and MERMA
    if movement_type in ("SALIDA", "MERMA"):
        current = calcular_stock(product_id, location_id)
        if quantity > current:
            conn.close()
            raise ValueError(
                f"stock_insuficiente: {quantity} > {current} (available)"
            )

    # Insert movement
    movement_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO inventory_movements (id, product_id, location_id, movement_type, quantity, unit_price, reference, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (movement_id, product_id, location_id, movement_type, quantity, unit_price, reference, notes, now),
    )
    conn.commit()
    conn.close()

    return {
        "id": movement_id,
        "product_id": product_id,
        "location_id": location_id,
        "movement_type": movement_type,
        "quantity": quantity,
        "unit_price": unit_price,
        "reference": reference,
        "notes": notes,
        "created_at": now,
    }


def get_historial(product_id: str, location_id: str) -> list:
    """Get movement history ordered by created_at DESC."""
    conn = models.get_connection()
    rows = conn.execute(
        """
        SELECT id, product_id, location_id, movement_type, quantity, unit_price, reference, notes, created_at
        FROM inventory_movements
        WHERE product_id = ? AND location_id = ?
        ORDER BY created_at DESC
        """,
        (product_id, location_id),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]