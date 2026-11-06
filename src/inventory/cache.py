"""
Backend Caching Strategy for Brasaland Inventory API
Implements in-memory caching with TTL (Time-To-Live) for frequent queries.
"""
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps
import logging

logger = logging.getLogger("brasaland.cache")


class CacheEntry:
    """Representa una entrada en caché con TTL."""

    def __init__(self, value: Any, ttl_seconds: int = 300):
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds

    def is_expired(self) -> bool:
        """Verifica si el caché ha expirado."""
        return time.time() - self.created_at > self.ttl_seconds

    @property
    def age_ms(self) -> float:
        """Retorna la edad del caché en milisegundos."""
        return (time.time() - self.created_at) * 1000


class SimpleCache:
    """
    Caché en memoria simple con expiración basada en TTL.
    Válido para aplicaciones de una sola instancia.
    """

    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del caché si existe y no ha expirado."""
        if key not in self._cache:
            logger.debug(f"Cache MISS for key: {key}")
            return None

        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            logger.debug(f"Cache EXPIRED for key: {key}")
            return None

        logger.debug(f"Cache HIT for key: {key} (age: {entry.age_ms:.2f}ms)")
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Establecer valor en caché con TTL."""
        self._cache[key] = CacheEntry(value, ttl_seconds)
        logger.debug(f"Cache SET for key: {key} (TTL: {ttl_seconds}s)")

    def delete(self, key: str) -> None:
        """Eliminar entrada del caché."""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache DELETED for key: {key}")

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidar todas las claves que coincidan con un patrón.
        Útil para invalidar múltiples entradas relacionadas.
        """
        keys_to_delete = [k for k in self._cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self._cache[key]
        logger.debug(f"Cache INVALIDATED {len(keys_to_delete)} entries matching pattern: {pattern}")
        return len(keys_to_delete)

    def clear(self) -> None:
        """Limpiar todo el caché."""
        self._cache.clear()
        logger.debug("Cache CLEARED")

    def stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del caché."""
        return {
            "total_entries": len(self._cache),
            "keys": list(self._cache.keys()),
        }


# Instancia global del caché
_cache = SimpleCache()


def cache_result(ttl_seconds: int = 300, key_prefix: str = ""):
    """
    Decorator para cachear resultados de funciones.
    
    Uso:
        @cache_result(ttl_seconds=300, key_prefix="products")
        def get_products(category: str):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Construir clave única
            cache_key = f"{key_prefix}:{func.__name__}:{args}:{sorted(kwargs.items())}"

            # Intentar obtener del caché
            cached_value = _cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper

    return decorator


def get_cache() -> SimpleCache:
    """Obtener instancia del caché global."""
    return _cache


def invalidate_cache_for_product(product_id: str) -> int:
    """
    Invalidar caché para un producto específico.
    Útil cuando se actualiza un producto.
    """
    return _cache.invalidate_pattern(f"product:{product_id}")


def invalidate_cache_for_location(location_id: str) -> int:
    """
    Invalidar caché para una ubicación específica.
    Útil cuando se actualiza una ubicación.
    """
    return _cache.invalidate_pattern(f"location:{location_id}")


def invalidate_cache_for_stock(product_id: str, location_id: str) -> int:
    """
    Invalidar caché de stock para un producto en una ubicación.
    Útil cuando se registra un movimiento.
    """
    return _cache.invalidate_pattern(f"stock:{product_id}:{location_id}")
