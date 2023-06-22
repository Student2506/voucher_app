"""External file to handle redis connection."""

import redis

from settings.config import settings


def redis_init() -> redis.Redis:
    """Connect to Redis.

    Returns:
        redis.Redis - instance
    """
    return redis.from_url(settings.redis_url, decode_responses=True)
