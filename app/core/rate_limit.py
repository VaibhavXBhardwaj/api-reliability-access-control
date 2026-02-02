import time
from fastapi import Request, HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# 🔥 Global in-memory store (used for testing)
RATE_STORE: dict[str, list[float]] = {}


def rate_limit(key: str, limit: int, window_seconds: int):
    def limiter(request: Request):
        identifier = request.client.host
        now = time.time()

        bucket = RATE_STORE.get(identifier, [])

        # Remove expired timestamps
        bucket = [ts for ts in bucket if now - ts < window_seconds]

        if len(bucket) >= limit:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        bucket.append(now)
        RATE_STORE[identifier] = bucket

    return limiter
