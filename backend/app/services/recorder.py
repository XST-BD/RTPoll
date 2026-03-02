import aio_pika
import asyncio

from datetime import datetime
import json
from sqlalchemy.orm import Session

from app.db.model.poll import PollHistoryEntry
from app.deps import get_db
from app.setup.cache import redis_client
from app.deps import SessionLocal

RABBITMQ_URL="amqp://rtpoll-rmq:5672"

def get_minute_key(poll_id: int, ts: datetime):
    ts_min = ts.replace(second=0, microsecond=0)
    return f'poll_id:{poll_id}:{ts_min.isoformat()}'


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        poll_id = data['poll_id']
        num_votes = data['num_votes']
        ts = datetime.fromisoformat(data['timestamp'])
        key = get_minute_key(poll_id, ts)

        await redis_client.incrby(key, num_votes)


async def flush_db_votes():
    while True: 
        await asyncio.sleep(60)
        db = SessionLocal()
        now = datetime.now().replace(second=0, microsecond=0)

        try: 
            async for key in redis_client.scan_iter("vote_aggregate:*"):
                _, poll_id_str, min_str = key.split(':')
                poll_id = int(poll_id_str)
                min_ts: datetime = (min_str)

                if min_ts <= now:
                        total_votes = int(await redis_client.get(key))
                        entry = PollHistoryEntry(
                            poll_id=poll_id,
                            timestamp=min_ts,
                            value=total_votes
                        )
                        db.add(entry)
                        try:
                            db.commit()
                        except Exception as e:
                            db.rollback()
                            print(f"DB insert error for {poll_id} at {min_ts}: {e}")

                        # delete key from Redis after flush
                        await redis_client.delete(key)

        except Exception as e: 
            print('Redis flush error: ', e)


async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue('vote_events', durable=True)
    await queue.consume(process_message)  # type: ignore

    # start periodic flush task
    asyncio.create_task(flush_db_votes())

    # keep worker running
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
