from django_redis import get_redis_connection

def delete_cache_by_prefix(prefix):
    redis_conn = get_redis_connection('default')
    keys = redis_conn.keys(f"{prefix}*")
    if keys:
        redis_conn.delete(*keys)

def delete_cache_by_key(key):
    redis_conn = get_redis_connection('default')
    redis_conn.delete(key)