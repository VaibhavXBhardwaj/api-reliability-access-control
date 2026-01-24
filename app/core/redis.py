import redis
from app.core.config import settings

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
