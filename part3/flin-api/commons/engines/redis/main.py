from datetime import datetime
from typing import Callable, Optional
from redis import from_url
from django.conf import settings

redis_client = from_url(settings.CACHE_LOCATION)


def cache_result(
    key: Optional[str] = None,
    key_func: Optional[Callable] = None,
    expire_at: Optional[Callable] = None,
):
    """
    A decorator to cache function results.

    Args:
        key: A static cache key. If provided, it will be used directly.
        key_func: A function that generates a dynamic cache key based on function arguments.
        expire_at: The expiration time for the cache. If provided, the cache will expire at this time.

    Returns:
        The cached result if available, otherwise computes and caches the function result.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            cache_key = key if key else key_func(*args, **kwargs) if key_func else None
            if not cache_key:
                raise ValueError("Either 'key' or 'key_func' must be provided.")

            cache_value = redis_client.get(cache_key)
            if cache_value is not None:
                return cache_value

            result = func(*args, **kwargs)

            redis_client.set(cache_key, result)
            if expire_at:
                redis_client.expireat(cache_key, expire_at())

            return result

        return wrapper

    return decorator
