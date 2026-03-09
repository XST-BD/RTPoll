import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy.orm import Session
import redis.asyncio as redis
from redis.asyncio import Redis

from app.db.session import SessionLocal
from app.db.model.poll import PollModel

# Caching
redis_client: Redis = redis.from_url(
    'redis://rtpoll-redis:6379',
    decode_responses=True,
)

SYNC_INTERVAL = 30

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

                    print("Redis votes:", votes)

                    for opt in poll.options:
                        new_votes = votes.get(opt.id, 0)

                        print("Updating", opt.id, "->", new_votes)

                        if opt.votes != new_votes:
                            opt.votes = new_votes

                if cursor == 0:
                    break

            db.commit()

        except Exception as e:
            print("Sync error:", e)

        finally:
            db.close()

        print("Running sync cycle")

        await asyncio.sleep(SYNC_INTERVAL)