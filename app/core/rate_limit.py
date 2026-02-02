import time
from fastapi import Request, HTTPException, status
from redis import Redis

# Redis client (already connected elsewhere if needed)
redis = Redis(host="localhost", port=6379, decode_responses=True)


def rate_limit(key_prefix: str, limit: int, window: int):
    """
    Rate limit dependency factory

    key_prefix: logical name (signup, login, etc.)
    limit: number of requests
    window: time window in seconds
    """

    async def limiter(request: Request): 
        # identify caller
        if hasattr(request.state, "user") and request.state.user:
            identifier = f"user:{request.state.user.id}"
        else:
            identifier = f"ip:{request.client.host}"

        redis_key = f"rate:{key_prefix}:{identifier}"

        now = int(time.time())

        pipe = redis.pipeline()
        pipe.zadd(redis_key, {now: now})
        pipe.zremrangebyscore(redis_key, 0, now - window)
        pipe.zcard(redis_key)
        pipe.expire(redis_key, window)
        _, _, count, _ = pipe.execute()

        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )

    return limiter
