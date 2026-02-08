import redis
from urllib.parse import urlparse
from app.core.config import settings

redis_url = settings.REDIS_URL

if redis_url:
    parsed = urlparse(redis_url)
    redis_client = redis.Redis(
        host=parsed.hostname,
        port=parsed.port,
        password=parsed.password,
        decode_responses=True
    )
else:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )

try:
    redis_client.ping()
    print("✅ Redis connected")
except Exception as e:
    print("❌ Redis connection failed:", e)
