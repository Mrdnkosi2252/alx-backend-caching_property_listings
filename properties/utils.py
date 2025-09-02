from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    queryset = cache.get('all_properties')
    if queryset is None:
        queryset = list(Property.objects.all())
        cache.set('all_properties', queryset, 3600)  # Cache for 1 hour
    return queryset

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    ratio = hits / total if total > 0 else 0
    
    metrics = {
        'hits': hits,
        'misses': misses,
        'hit_ratio': ratio
    }
    
    logger.info(f"Cache Metrics: {metrics}")
    return metrics