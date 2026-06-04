import os
from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
import redis.client
from redis.connection import BlockingConnectionPool

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.model.poll import PollModel

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL', 'REDIS_URL')

logger = get_task_logger(__name__)

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

DB_SYNC_INTERVAL = 30

# Create a global pool (all tasks in this worker share it)
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL, decode_responses=True
)

def get_redis_client():
    """Return a Redis client from the global pool."""
    return redis.Redis(connection_pool=redis_pool)

@celery_app.task(name='sync_votes_db')
def sync_votes_db():

    logger.info("Vote sync worker started")
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
        logger.error("DB sync error", exc_info=True)
    finally:
        db.close()

    logger.info("Running database sync cycle")


celery_app.conf.beat_schedule = {
    'sync-votes-every-minute': {
        'task': 'sync_votes_db',
        'schedule': DB_SYNC_INTERVAL,
    },
}