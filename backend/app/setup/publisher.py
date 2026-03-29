import os
import aio_pika
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
import json

from app.setup.ws import WSConnectionManager
from app.utils import create_payload

load_dotenv()
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'RABBITMQ_URL')

# publisher 
async def publish_vote(
    poll_id: int, 
    option_id: int,
    delta: int = 1,
):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("poll_updates", aio_pika.ExchangeType.FANOUT)

    message = {
        "type": "vote_increment",
        "poll_id": poll_id,
        "option_id": option_id,
        "delta": delta,
        "hour": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H"),
    }

    await exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key="",
    )
    await connection.close()

async def on_message(wsmanager: WSConnectionManager, data):
    poll_id = data['poll_id']
    # create_payload()

    # await wsmanager.broadcast(
    #     poll_id=poll_id,
    #     voter_payload= ,
    #     creator_payload= ,
    # )    

# consumer
async def start_consumer(wsmanager: WSConnectionManager, queue_name):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)

    exchange = await channel.declare_exchange("poll_updates", aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process(requeue=True):
                data = json.loads(message.body)
                # broadcast to connected WS clients (non-blocking)
                asyncio.create_task(on_message(wsmanager, data))