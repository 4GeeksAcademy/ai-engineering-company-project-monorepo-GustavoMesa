"""
Brasaland API — Aplicación principal FastAPI.
Incluye el router de inventario y verificación de base de datos.
"""
import os
import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2

from src.inventory.router import router as inventory_router

app = FastAPI(
    title="Brasaland Services",
    description="API del ecosistema digital y de inventario de Brasaland.",
    version="1.0.0",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://brasaland_user:brasaland_pass@db:5432/brasaland",
)
BOOT_TIME = time.time()


def check_db() -> bool:
    """Check PostgreSQL connection and return True if healthy."""
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)
        conn.close()
        return True
    except Exception:
        return False


# Incluir router de inventario
app.include_router(inventory_router)


@app.get("/status", tags=["health"])
def status():
    """Health-check endpoint. Returns API status and database connectivity."""
    db_connected = check_db()
    return {
        "status": "ok",
        "database": "connected" if db_connected else "disconnected",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - BOOT_TIME, 2),
    }


@app.get("/health", tags=["health"])
def health_check():
    """Quick health check for load balancers / orchestration."""
    db_connected = check_db()
    if not db_connected:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )
    return {"status": "healthy", "database": "connected"}