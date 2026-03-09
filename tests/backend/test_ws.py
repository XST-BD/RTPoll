import asyncio 
import json
import websockets

async def test_ws_vote_view():
    uri = "ws://127.0.0.1:8000/ws/vote/3"

    async with websockets.connect(uri) as websocket:
        
        async def send_message():
            msg = {"type": "get_vote"}
            await websocket.send(json.dumps(msg))
            await asyncio.sleep(1)

        async def read_message():
            while True: 
                response = await websocket.recv()
                try: 
                    data = json.loads(response)
                    print(data)
                except json.JSONDecodeError:
                    print(response)

        await asyncio.gather(send_message(), read_message())

async def test_ws_vote_sent():
    uri = "ws://127.0.0.1:8000/ws/vote/3"

    async with websockets.connect(uri) as websocket:
        
        async def send_message():
            msg = {"type": "send_vote", "option_id": 1}
            await websocket.send(json.dumps(msg))
    

        async def read_message():
            while True: 
                response = await websocket.recv()
                try: 
                    data = json.loads(response)
                    print(data)
                except json.JSONDecodeError:
                    print(response)

        await asyncio.gather(send_message(), read_message())


async def test_ws_poll_view(): 
    uri = "ws://127.0.0.1:8000/ws/poll/1"

    async with websockets.connect(uri) as websocket: 

        async def send_message():
            while True: 
                msg = {
                    "type": "poll_view",
                }
                await websocket.send(json.dumps(msg))

        async def read_message(): 
            while True: 
                response  = await websocket.recv() 
                try: 
                    data = json.loads(response)
                    print(data)
                except json.JSONDecodeError:
                    print(response)

        await asyncio.gather(send_message(), read_message())


asyncio.run(test_ws_vote_sent())     
        