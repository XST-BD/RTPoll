import os 
from dotenv import load_dotenv

import redis.asyncio as redis
from redis.asyncio import Redis

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'REDIS_URL')

# Caching
redis_client: Redis = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)
