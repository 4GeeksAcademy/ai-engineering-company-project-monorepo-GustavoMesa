"""
Inventory Manager — FastAPI router with endpoints for stock management.
Stock is always calculated from movements, never stored directly.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from . import service, models

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


class MovementCreate(BaseModel):
    product_id: str
    location_id: str
    movement_type: str = Field(..., pattern="^(ENTRADA|SALIDA|MERMA)$")
    quantity: float = Field(..., gt=0)
    unit_price: Optional[float] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str = Field(
        default="OTRO", pattern="^(CARNE|BEBIDA|LACTEO|VEGETAL|OTRO)$"
    )
    stock_minimo: float = 0
    unit: str = "unidades"


class LocationCreate(BaseModel):
    name: str
    country: str
    city: str


@router.on_event("startup")
def startup():
    models.init_db()
    models.seed_data()


@router.post("/movements")
def create_movement(m: MovementCreate):
    """Register a new inventory movement. Stock is calculated from movements."""
    try:
        result = service.registrar_movimiento(
            product_id=m.product_id,
            location_id=m.location_id,
            movement_type=m.movement_type,
            quantity=m.quantity,
            unit_price=m.unit_price,
            reference=m.reference,
            notes=m.notes,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/stock")
def get_stock(product_id: str, location_id: str):
    """Get calculated stock for a product at a location."""
    info = service.get_stock_info(product_id, location_id)
    return info


@router.get("/movements")
def get_movements(product_id: str, location_id: str):
    """Get movement history for a product at a location."""
    return service.get_historial(product_id, location_id)


@router.post("/products")
def create_product(p: ProductCreate):
    """Create a new product."""
    import uuid
    from datetime import datetime, timezone

    conn = models.get_connection()
    pid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute(
            "INSERT INTO products (id, name, sku, category, stock_minimo, unit, created_at) VALUES (?,?,?,?,?,?,?)",
            (pid, p.name, p.sku, p.category, p.stock_minimo, p.unit, now),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"id": pid, "name": p.name, "sku": p.sku}


@router.get("/products")
def list_products(category: Optional[str] = None):
    """List all products."""
    conn = models.get_connection()
    if category is None:
        rows = conn.execute("SELECT * FROM products").fetchall()
    else:
        normalized_category = category.strip().upper()
        if normalized_category not in models.PRODUCT_CATEGORIES:
            conn.close()
            raise HTTPException(status_code=422, detail="Categoría no válida")
        rows = conn.execute(
            "SELECT * FROM products WHERE category = ?", (normalized_category,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/locations")
def create_location(l: LocationCreate):
    """Create a new location."""
    import uuid

    conn = models.get_connection()
    lid = str(uuid.uuid4())
    try:
        conn.execute(
            "INSERT INTO locations VALUES (?,?,?,?)",
            (lid, l.name, l.country, l.city),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"id": lid, "name": l.name}


@router.get("/locations")
def list_locations():
    """List all locations."""
    conn = models.get_connection()
    rows = conn.execute("SELECT * FROM locations").fetchall()
    conn.close()
    return [dict(r) for r in rows]