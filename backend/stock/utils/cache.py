from django_redis import get_redis_connection

def delete_cache_by_match(regex):
    redis_conn = get_redis_connection('default')
    keys = redis_conn.keys(regex)
    if keys:
        redis_conn.delete(*keys)

def delete_cache_by_key(key):
    redis_conn = get_redis_connection('default')
    redis_conn.delete(key)