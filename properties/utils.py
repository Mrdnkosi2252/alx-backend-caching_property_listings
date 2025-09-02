from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
       
        return cached_properties
    
    
    properties = Property.objects.all()
    
    
    cache.set('all_properties', properties, 3600)
    
    return properties

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