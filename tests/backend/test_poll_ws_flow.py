from httpx_ws import aconnect_ws
import pytest


# @pytest.mark.asyncio
# @pytest.mark.run(order=9)
# async def test_poll_ws_flow(shared_data):

#     async with aconnect_ws(
#         url=f'ws://127.0.0.1/api/v0/ws/{shared_data['poll_id']}?t={shared_data['token']}&fp={shared_data['fingerprint']}'
#     ) as ws:

#     ws.send_json({'type':'info',})