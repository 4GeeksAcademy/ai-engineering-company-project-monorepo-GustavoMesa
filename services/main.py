"""
Brasaland API — Aplicación principal FastAPI.
MVP Contenedorizado: endpoint /status con verificación de base de datos.
"""
import os
import time

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(
    title="Brasaland API",
    version="0.1.0",
    description="API del ecosistema digital de Brasaland",
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


@app.get("/status")
def status():
    """Health-check endpoint. Returns API status and database connectivity."""
    db_connected = check_db()
    return {
        "status": "ok",
        "database": "connected" if db_connected else "disconnected",
        "version": "0.1.0",
        "uptime_seconds": round(time.time() - BOOT_TIME, 2),
    }


@app.get("/health")
def health():
    """Quick health check for load balancers / orchestration."""
    db_connected = check_db()
    if not db_connected:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )
    return {"status": "healthy", "database": "connected"}