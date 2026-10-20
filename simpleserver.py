import asyncio
from websockets.asyncio.server import serve, broadcast
import json
import logger
import requests
import os
from dotenv import load_dotenv
import uuid
import time
from pathlib import Path
from collections import deque

def validate(token):
    url = 'https://cami.barfpile.dev/validate'
    payload = {'token': token}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return (response.json())["message"]
    else:
        return False
    pass

motd = "Welcome!"

async def chat_handler(websocket):
    await websocket.send(json.dumps({"motd":motd}))

async def main():
    portuse = 5615

    async with serve(chat_handler, "0.0.0.0", portuse):
        logger.info(f"Running on port {portuse}")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped cleanly.")