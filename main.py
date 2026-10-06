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
from helperfuncs import *

load_dotenv()

servername = os.getenv("servername")
motd = f"><> Good morning! Welcome to {servername}! <><"

logger.success(f"Loading {servername}")

authpairs = []
authed_clients = set()
connected_clients = set()

async def chat_handler(websocket):
    connected_clients.add(websocket)
    await websocket.send(json.dumps({"motd":motd}))
    try:
        async for message in websocket:
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps(makejsonerror("Invalid JSON")))
                continue
            try:
                cmd = message["cmd"]

                if cmd == "auth":
                    token = message["token"]
                    validation = validate(token)
                    username = validation["username"]
                    userid = validation["userid"]
                    userobj = {"user": userid, "auth": websocket}
                    chatauth(userid, username, websocket)
                    authed_clients.add(websocket)

                    await websocket.send(json.dumps(makejsonsuccess("Successfully authed.")))

                    data = {"cmd": "connect", "id": userid, "username": username}
                    broadcast(connected_clients, json.dumps(data))
                    logger.success(f"Welcome {username}")

                elif websocket in authed_clients:
                    user = next((user for user, username, ws in authpairs if ws == websocket), None)

                    if cmd == "new_message":
                        content = message["body"]
                        if len(content) >= 5:
                            channel = message["channel"]
                            msgid = f"msg{uuid.uuid4}"
                            data = {"cmd": "new_message", "username": username, "userid": user, "channel": channel, "timestamp": time.time(), "id": msgid, "body": content}
                            savetofile(channel, json.dumps(data))
                            logger.success(f"{username} - {content}")
                            broadcast(authed_clients, json.dumps(data))
                        else:
                            await websocket.send(json.dumps(makejsonerror("Message too short. Must be 5 chars at least.")))

                    if cmd == "delete_message":
                        messageid = message["msgid"]
                        channel = message["channel"]
                        message = find_message(channel, messageid)
                        validation = validate(token)
                        if messageid and validation and message["userid"] == validation["userid"]:
                            try:
                                delete_message(channel, messageid)
                                data = {"cmd": "delete_message", "username": username, "userid": user, "channel": channel, "id": msgid}
                                await broadcast(data)
                            except Exception as e:
                                await websocket.send(e)
                        else:
                            await websocket.send(json.dumps(makejsonerror("No msgid provided.")))

                    if cmd == "gethistory":
                        length = message["length"]
                        channel = message["channel"]

                        await websocket.send(json.dumps(retrievelines(channel, length)))

                else:
                    await websocket.send(json.dumps(makejsonerror("Invalid auth")))

            except Exception as e:
                ex = str(e)
                await websocket.send(json.dumps(makejsonerror(ex)))
                logger.error(ex)
    finally:
        connected_clients.remove(websocket)
        user, username = next(((user, username) for user, username, ws in authpairs if ws == websocket),(None, None))
        authpairs[:] = [(user, username, ws) for user, username, ws in authpairs if ws != websocket]
        logger.error(f"{username} disconnected")
        data = {"cmd": "disconnect", "id": user, "username": username}
        broadcast(connected_clients, json.dumps(data))

async def main():
    portuse = 5615

    async with serve(chat_handler, "localhost", portuse):
        logger.info(f"Running on port {portuse}")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())