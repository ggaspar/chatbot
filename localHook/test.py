
import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhook:5044/echo') as websocket:
        await websocket.send("[standard reply]")

asyncio.get_event_loop().run_until_complete(hello())
