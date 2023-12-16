"""External file to handle redis connection."""

import redis.asyncio as redis

from settings.config import settings

# def redis_init() -> redis.Redis:
#     """Connect to Redis.

#     Returns:
#         redis.Redis - instance
#     """
#     return redis.from_url(str(settings.redis_url), decode_responses=True)


async def redis_context(app) -> None:
    engine = redis.from_url(str(settings.redis_url), decode_responses=True)
    app['redis'] = engine
    yield
    await app['redis'].aclose()
