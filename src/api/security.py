from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import time
import redis

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cor.erarta.ai"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Rate limiting
redis_client = redis.Redis(host='localhost', port=6379, db=0)
RATE_LIMIT = 100  # запросов
RATE_LIMIT_PERIOD = 3600  # в час

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current = redis_client.incr(f"rate_limit:{client_ip}")
    
    if current == 1:
        redis_client.expire(f"rate_limit:{client_ip}", RATE_LIMIT_PERIOD)
    
    if current > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    response = await call_next(request)
    return response

app.middleware("http")(rate_limit_middleware) 