"""
Brasaland API — Aplicación principal FastAPI.
Incluye el router de inventario, middleware de rendimiento y caching.
"""
import os
import time
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2

from src.inventory.router import router as inventory_router
from src.inventory.middleware import PerformanceMiddleware, CacheMetricsMiddleware

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

BOOT_TIME = time.time()
DATABASE_URL = os.getenv("DATABASE_URL", "")

app = FastAPI(
    title="Brasaland Services",
    description="API del ecosistema digital y de inventario de Brasaland.",
    version="1.0.0",
)

# Agregar middlewares de rendimiento
app.add_middleware(PerformanceMiddleware)
app.add_middleware(CacheMetricsMiddleware)

app.include_router(inventory_router)


def check_db() -> bool:
    """Check PostgreSQL connection and return True if healthy."""
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)
        conn.close()
        return True
    except Exception:
        return False


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
