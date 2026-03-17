import asyncio
from contextlib import asynccontextmanager

import os 
from dotenv import load_dotenv

from fastapi import FastAPI

from sqlalchemy.orm import Session
import redis.asyncio as redis
from redis.asyncio import Redis

from app.db.session import SessionLocal
from app.db.model.poll import PollModel

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'REDIS_URL')

# Caching
redis_client: Redis = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)

DB_SYNC_INTERVAL = 30

async def sync_votes_db():

    print("Vote sync worker started")

    while True:

        db: Session = SessionLocal()

        try:
            cursor = 0

            while True:
                cursor, keys = await redis_client.scan(
                    cursor, match="poll:*:votes", count=100
                )

                for key in keys:

                    poll_id = int(key.split(":")[1])

                    votes = await redis_client.hgetall(key)     # type: ignore
                    if not votes:
                        continue

                    votes = {int(k): int(v) for k, v in votes.items()}

                    poll = db.query(PollModel).filter(
                        PollModel.id == poll_id
                    ).first()

                    if not poll:
                        continue

                    for opt in poll.options:
                        new_votes = votes.get(opt.id, 0)

                        if opt.votes != new_votes:
                            opt.votes = new_votes

                if cursor == 0:
                    break

            db.commit()

        except Exception as e:
            print("DB Sync error:", e)

        finally:
            db.close()

        print("Running database sync cycle")
        await asyncio.sleep(DB_SYNC_INTERVAL)