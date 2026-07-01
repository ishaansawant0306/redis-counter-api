import os

import redis
from fastapi import FastAPI

app = FastAPI()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)


@app.post("/hit/{key}")
async def hit(key: str):
    count = r.incr(f"counter:{key}")
    return {"key": key, "count": count}


@app.get("/count/{key}")
async def get_count(key: str):
    val = r.get(f"counter:{key}")
    return {"key": key, "count": int(val) if val is not None else 0}


@app.get("/healthz")
async def healthz():
    try:
        alive = r.ping()
    except Exception:
        alive = False
    return {"status": "ok", "redis": "up" if alive else "down"}
