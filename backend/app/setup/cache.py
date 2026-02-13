import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy.orm import Session
import redis.asyncio as redis

from app.db.session import session_local
from app.db.model.poll import PollModel

# Caching
redis_client = redis.from_url(
    'redis://rtpoll-redis:6379',
    decode_responses=True,
)

SYNC_INTERVAL = 30

async def sync_votes_db():

    while True: 

        db: Session = session_local

        try: 
            keys = await redis_client.keys('poll:*:votes')

            for key in keys:
                # key = poll:<poll_id>:votes
                poll_id = int(key.split(":")[1])
                votes = await redis_client.hgetall(key)

                if not votes: 
                    continue

                poll = db.query(PollModel).filter(
                    PollModel.id == poll_id
                ).first()

                if not poll:
                    continue

                # Convert to list[int] based on options
                new_votes = []

                for opt in poll.options:
                    new_votes.append(
                        int(votes.get(str(opt), 0))
                    )

                poll.votes = new_votes

            db.commit()

        except Exception as e: 
            print("Sync error: ", e)
        finally: 
            db.close()

        await asyncio.sleep(SYNC_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    task = asyncio.create_task(sync_votes_db())

    yield

    # Shutdown
    task.cancel()