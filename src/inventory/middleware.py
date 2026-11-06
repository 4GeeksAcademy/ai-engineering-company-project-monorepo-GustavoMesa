"""
Performance Middleware for Brasaland API
Measures response times and logs performance metrics.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("brasaland.performance")


class PerformanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware que mide el tiempo de respuesta de cada endpoint.
    Registra métricas en milisegundos para análisis de rendimiento.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Capturar tiempo de inicio con precisión
        start_time = time.perf_counter()

        # Procesar la solicitud
        response = await call_next(request)

        # Calcular tiempo total en milisegundos
        process_time_ms = (time.perf_counter() - start_time) * 1000

        # Agregar header con tiempo de procesamiento
        response.headers["X-Process-Time-Ms"] = str(round(process_time_ms, 2))

        # Log de performance
        log_level = "info" if process_time_ms < 100 else "warning" if process_time_ms < 500 else "error"
        getattr(logger, log_level)(
            f"Endpoint: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time_ms:.2f}ms"
        )

        return response


class CacheMetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware para rastrear efectividad del caché.
    Registra hits y misses para análisis de optimización.
    """

    def __init__(self, app):
        super().__init__(app)
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
        }

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Registrar stats en headers (para debugging)
        if hasattr(request.app.state, "cache_hit"):
            response.headers["X-Cache"] = "HIT"
            self.cache_stats["hits"] += 1
        else:
            response.headers["X-Cache"] = "MISS"
            self.cache_stats["misses"] += 1

        return response
