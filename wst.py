import logging

from alpaca_trade_api.stream import Stream

from keys import paper_apikey, paper_secretkey
ALPACA_API_KEY = paper_apikey
ALPACA_SECRET_KEY = paper_secretkey


import asyncio
import websockets
import json

async def connect_to_websocket():
    uri = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"
    
    async with websockets.connect(uri) as websocket:
        auth_data = {
            "action": "auth",
            "key": ALPACA_API_KEY,
            "secret": ALPACA_SECRET_KEY
        }
        await websocket.send(json.dumps(auth_data))

        subscribe_data = {
            "action": "subscribe",
            # "trades": ["BTC/USD"],
            # "quotes": ["LTC/USD", "ETH/USD"],
            "bars": ["BTC/USD"]
        }
        await websocket.send(json.dumps(subscribe_data))

        async for message in websocket:
            print(message)

asyncio.run(connect_to_websocket())