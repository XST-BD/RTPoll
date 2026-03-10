import aio_pika
import asyncio

from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app.db.model.poll import PollHistoryEntry, PollModel
from app.deps import get_db
from app.setup.cache import redis_client
from app.deps import SessionLocal

HISTORY_RECORD_INTERVAL = 3600

async def sync_poll_history():
    
    print("History sync worker started")
    await asyncio.sleep(60)  # allow vote sync to populate DB

    while True:
        db : Session = SessionLocal()
        try:
            polls = (
                db.query(PollModel)
                .options(selectinload(PollModel.options))
                .all()
            )

            for poll in polls:
                total_votes = sum(option.votes for option in poll.options)

                prev_total = (
                    db.query(func.sum(PollHistoryEntry.value))
                    .filter(PollHistoryEntry.poll_id==poll.id)
                    .scalar()
                ) or 0

                delta = max(0, total_votes - prev_total)

                poll_history = PollHistoryEntry(
                    poll_id=poll.id,
                    timestamp = datetime.now(timezone.utc),
                    value=delta,
                )

                db.add(poll_history)
            
            db.commit()

        except Exception as e:
            print("History sync error:", e)
            db.rollback()

        finally:
            db.close()

        print("Running history sync cycle")

        await asyncio.sleep(HISTORY_RECORD_INTERVAL)
    