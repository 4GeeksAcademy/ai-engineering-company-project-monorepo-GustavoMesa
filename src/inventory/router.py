"""
Inventory Manager — FastAPI router with endpoints for stock management.
Stock is always calculated from movements, never stored directly.

SECURITY: Implements strict serialization separation between Request and Response models
to prevent data leakage of sensitive fields like unit_price and cost information.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from . import service, models

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])

# ============================================================================
# REQUEST MODELS (Input validation)
# ============================================================================

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


# ============================================================================
# RESPONSE MODELS (Output validation — SECURITY: Excludes sensitive fields)
# ============================================================================

class MovementResponse(BaseModel):
    """Public response for movement creation.
    EXCLUDES: unit_price, reference, notes (internal/sensitive data)"""
    id: str
    product_id: str
    location_id: str
    movement_type: str
    quantity: float
    created_at: str
    
    class Config:
        from_attributes = True


class MovementHistoryPublic(BaseModel):
    """Public response for movement history.
    EXCLUDES: unit_price, reference, notes (internal/sensitive data)"""
    id: str
    product_id: str
    location_id: str
    movement_type: str
    quantity: float
    created_at: str
    
    class Config:
        from_attributes = True


class StockInfoPublic(BaseModel):
    """Public response for stock query."""
    product_id: str
    location_id: str
    current_stock: float
    alert: bool
    
    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    """Public response for product creation.
    EXCLUDES: stock_minimo, created_at (internal fields)"""
    id: str
    name: str
    sku: str
    category: str
    unit: str
    
    class Config:
        from_attributes = True


class ProductPublic(BaseModel):
    """Public response for product listing.
    EXCLUDES: stock_minimo, created_at (internal fields)"""
    id: str
    name: str
    sku: str
    category: str
    unit: str
    
    class Config:
        from_attributes = True


class LocationResponse(BaseModel):
    """Public response for location creation."""
    id: str
    name: str
    country: str
    city: str
    
    class Config:
        from_attributes = True


class LocationPublic(BaseModel):
    """Public response for location listing."""
    id: str
    name: str
    country: str
    city: str
    
    class Config:
        from_attributes = True


@router.on_event("startup")
def startup():
    models.init_db()
    models.seed_data()


# ============================================================================
# ENDPOINTS (Secured with response_model)
# ============================================================================

@router.post("/movements", response_model=MovementResponse)
def create_movement(m: MovementCreate):
    """Register a new inventory movement. Stock is calculated from movements.
    
    SECURITY: Returns only non-sensitive fields (excludes unit_price, reference, notes).
    """
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


@router.get("/stock", response_model=StockInfoPublic)
def get_stock(product_id: str, location_id: str):
    """Get calculated stock for a product at a location.
    
    SECURITY: Response schema is explicitly validated by Pydantic.
    """
    info = service.get_stock_info(product_id, location_id)
    return info


@router.get("/movements", response_model=List[MovementHistoryPublic])
def get_movements(product_id: str, location_id: str):
    """Get movement history for a product at a location.
    
    SECURITY: Returns only non-sensitive fields (excludes unit_price, reference, notes).
    """
    return service.get_historial(product_id, location_id)


@router.post("/products", response_model=ProductResponse)
def create_product(p: ProductCreate):
    """Create a new product.
    
    SECURITY: Response is validated by ProductResponse model.
    """
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
    return {
        "id": pid,
        "name": p.name,
        "sku": p.sku,
        "category": p.category,
        "unit": p.unit,
    }


@router.get("/products", response_model=List[ProductPublic])
def list_products(category: Optional[str] = None):
    """List all products.
    
    SECURITY: Returns only public fields (excludes stock_minimo, created_at).
    """
    conn = models.get_connection()
    if category is None:
        rows = conn.execute("SELECT id, name, sku, category, unit FROM products").fetchall()
    else:
        normalized_category = category.strip().upper()
        if normalized_category not in models.PRODUCT_CATEGORIES:
            conn.close()
            raise HTTPException(status_code=422, detail="Categoría no válida")
        rows = conn.execute(
            "SELECT id, name, sku, category, unit FROM products WHERE category = ?",
            (normalized_category,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/locations", response_model=LocationResponse)
def create_location(l: LocationCreate):
    """Create a new location.
    
    SECURITY: Response is validated by LocationResponse model.
    """
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
    return {"id": lid, "name": l.name, "country": l.country, "city": l.city}


@router.get("/locations", response_model=List[LocationPublic])
def list_locations():
    """List all locations.
    
    SECURITY: Response is validated by LocationPublic model.
    """
    conn = models.get_connection()
    rows = conn.execute("SELECT id, name, country, city FROM locations").fetchall()
    conn.close()
    return [dict(r) for r in rows]