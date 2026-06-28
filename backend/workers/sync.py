# vote sync worker

import os, time, logging
from dotenv import load_dotenv
import redis.client
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.model.poll import PollModel

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'REDIS_URL')
DB_SYNC_INTERVAL = 30

logging.basicConfig(level=logging.INFO)

# Create a global pool (all tasks in this worker share it)
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL, decode_responses=True
)

def get_redis_client():
    """Return a Redis client from the global pool."""
    return redis.Redis(connection_pool=redis_pool)

def sync_votes_db():

    redis_client = get_redis_client()

    db: Session = SessionLocal()

    try:
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor, match="poll:*:votes", count=100)   # type: ignore
            
            for key in keys:
                poll_id = str(key.split(":")[1])
                votes = redis_client.hgetall(key)  # type: ignore
                if not votes:
                    continue
                votes = {str(k): int(v) for k, v in votes.items()}  # type: ignore
                poll = db.query(PollModel).filter(PollModel.id == poll_id).first()
                if not poll:
                    continue
                for opt in poll.options:
                    new_votes = votes.get(opt.id, 0)
                    if opt.votes != new_votes:
                        opt.votes = new_votes
            
            if cursor == 0:  # finished scanning all keys
                break

        db.commit()
    except Exception as e:
        logging.error("DB sync error", exc_info=True)
    finally:
        db.close()

    logging.info("Running database sync cycle")


def vote_sync_worker():
    logging.info("Vote sync worker started")

    while True:
       try:
           sync_votes_db()
       except Exception:
           logging.exception("Vote sync failed")
       time.sleep(DB_SYNC_INTERVAL)


if __name__ == "__main__":
    vote_sync_worker()