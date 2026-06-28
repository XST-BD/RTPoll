import logging, time

from datetime import datetime, date, timezone
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, selectinload

from app.db.model.poll import PollHistoryEntry, PollModel
from app.deps import SessionLocal

logging.basicConfig(level=logging.INFO)
HISTORY_SYNC_INTERVAL = 3600 

def sync_poll_history():

    db : Session = SessionLocal()
    try:
        polls = (
            db.query(PollModel)
            .options(selectinload(PollModel.options))
            .all()
        )

        for poll in polls: 
            today = date.today()
            total_votes = sum(option.votes for option in poll.options)
            stmt = insert(PollHistoryEntry).values(
                poll_id=poll.id,
                snapshot_date=today,
                total_votes=total_votes,
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=["poll_id", "snapshot_date"])

            db.execute(stmt)
            
        db.commit()
        logging.info("History sync completed")

    except Exception as e:
        db.rollback()
        logging.exception("History sync error")

    finally:
        db.close()
    

def vote_history_worker():
    logging.info("Vote history sync worker started")

    while True: 
        try: 
            sync_poll_history()
        except Exception:
            logging.exception("Vote history sync failed")
        time.sleep(HISTORY_SYNC_INTERVAL)


if __name__ == "__main__":
    vote_history_worker()