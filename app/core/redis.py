import os
import redis
from urllib.parse import urlparse

redis_url = os.getenv("REDIS_URL")

if redis_url:
    # Render / external URL format
    parsed = urlparse(redis_url)
    redis_client = redis.Redis(
        host=parsed.hostname,
        port=parsed.port,
        password=parsed.password,
        decode_responses=True
    )
else:
    # Local / Railway internal network
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

try:
    redis_client.ping()
    print("✅ Redis connected")
except Exception as e:
    print("❌ Redis connection failed:", e)
