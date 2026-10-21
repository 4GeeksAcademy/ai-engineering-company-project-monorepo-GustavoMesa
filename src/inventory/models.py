"""
Inventory Manager — Modelos de dominio.
Brasaland: Gestión de inventario con stock calculado desde movimientos.
"""
import sqlite3
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class MovementType(str, Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    MERMA = "MERMA"


PRODUCT_CATEGORIES = ("CARNE", "BEBIDA", "LACTEO", "VEGETAL", "OTRO")


DB_PATH = "data/inventory.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize database schema."""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sku TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL DEFAULT 'OTRO',
            stock_minimo REAL NOT NULL DEFAULT 0,
            unit TEXT NOT NULL DEFAULT 'unidades',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS locations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inventory_movements (
            id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            location_id TEXT NOT NULL,
            movement_type TEXT NOT NULL CHECK(movement_type IN ('ENTRADA', 'SALIDA', 'MERMA')),
            quantity REAL NOT NULL CHECK(quantity > 0),
            unit_price REAL,
            reference TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (location_id) REFERENCES locations(id)
        );

        CREATE INDEX IF NOT EXISTS idx_movements_product_location
            ON inventory_movements(product_id, location_id);

        CREATE INDEX IF NOT EXISTS idx_movements_created
            ON inventory_movements(created_at DESC);
    """)
    product_columns = {
        row["name"] for row in conn.execute("PRAGMA table_info(products)").fetchall()
    }
    if "category" not in product_columns:
        conn.execute(
            "ALTER TABLE products ADD COLUMN category TEXT NOT NULL DEFAULT 'OTRO'"
        )
    conn.commit()
    conn.close()


def seed_data():
    """Insert initial seed data for Brasaland."""
    conn = get_connection()

    # Check if data already exists
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count > 0:
        conn.close()
        return

    now = datetime.now(timezone.utc).isoformat()

    # Products
    products = [
        ("p1", "Carne de res (entraña)", "CAR-001", "CARNE", 50, "kg", now),
        ("p2", "Pechuga de pollo", "POL-001", "CARNE", 30, "kg", now),
        ("p3", "Arepa paisa", "ARE-001", "OTRO", 100, "unidades", now),
        ("p4", "Salsa BBQ Brasaland", "BBQ-001", "OTRO", 20, "L", now),
        ("p5", "Papas criollas", "PAP-001", "VEGETAL", 80, "kg", now),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO products
            (id, name, sku, category, stock_minimo, unit, created_at)
        VALUES (?,?,?,?,?,?,?)
        """,
        products,
    )

    # Locations (2 of 14 Brasaland restaurants)
    locations = [
        ("loc-med-01", "Sede Principal Medellín", "Colombia", "Medellín"),
        ("loc-mia-01", "Brasaland Miami - Little Havana", "USA", "Miami"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO locations VALUES (?,?,?,?)",
        locations,
    )

    # Initial movements (entradas = stock inicial)
    movements = [
        (str(uuid.uuid4()), "p1", "loc-med-01", "ENTRADA", 200, 12.50, "FAC-001", "Compra semal", now),
        (str(uuid.uuid4()), "p2", "loc-med-01", "ENTRADA", 100, 8.30, "FAC-001", "Compra semal", now),
        (str(uuid.uuid4()), "p3", "loc-med-01", "ENTRADA", 500, 0.85, "FAC-002", "Pedido arepas", now),
        (str(uuid.uuid4()), "p4", "loc-med-01", "ENTRADA", 40, 5.00, "FAC-003", "Salsa BBQ", now),
        (str(uuid.uuid4()), "p5", "loc-med-01", "ENTRADA", 150, 1.20, "FAC-001", "Papas criollas", now),
        # Miami
        (str(uuid.uuid4()), "p1", "loc-mia-01", "ENTRADA", 150, 14.00, "INV-MIA-001", "Initial stock Miami", now),
        (str(uuid.uuid4()), "p3", "loc-mia-01", "ENTRADA", 300, 1.10, "INV-MIA-001", "Arepas for Miami", now),
        (str(uuid.uuid4()), "p4", "loc-mia-01", "ENTRADA", 25, 6.50, "INV-MIA-001", "BBQ sauce Miami", now),
        # Some consumption (salidas)
        (str(uuid.uuid4()), "p1", "loc-med-01", "SALIDA", 30, None, "VEN-001", "Ventas dia 1", now),
        (str(uuid.uuid4()), "p3", "loc-med-01", "SALIDA", 80, None, "VEN-001", "Ventas dia 1", now),
    ]
    conn.executemany(
        "INSERT INTO inventory_movements VALUES (?,?,?,?,?,?,?,?,?)",
        movements,
    )

    conn.commit()
    conn.close()