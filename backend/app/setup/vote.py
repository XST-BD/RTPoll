import asyncio

from cache import redis_client

from app.db.session import session_local
from app.db.model.poll import PollModel


# DB write within fixed interval
async def sync_votes():

    while True:
        await asyncio.sleep(30)

        db = session_local

        try: 
            keys = await redis_client.keys('poll:*:votes')
            for key in keys:
                poll_id = int(key.split(":")[1])
                votes = await redis_client.hgetall(key) # type: ignore

                poll = db.query(PollModel).filter(PollModel.id == poll_id).first()

                if poll:
                    poll.votes = {k: int(v) for k, v in votes.items()} # type: ignore

            db.commit()

        except Exception as e: 
            print("Sync error:", e)
        finally: 
            db.close()

