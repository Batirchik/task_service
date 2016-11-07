import redis


class RedisCache(object):
    """
        Adapter for accessing to redis cache
    """
    connection = redis.Redis()

    @classmethod
    def get_data(cls, obj):
        return cls.connection.get(obj)

    @classmethod
    def set_data(cls, obj, value, ttl):
        cls.connection.setex(obj, value, ttl)

    @classmethod
    def del_data(cls, obj):
        cls.connection.delete(obj)

c = RedisCache()
