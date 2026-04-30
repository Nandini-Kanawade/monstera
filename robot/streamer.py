# send data to laptop over wifi
import asyncio
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "0.0.0.0"                          # listen on all interfaces
PORT = int(os.getenv("PI_PORT", 8765))

_clients = set()


async def _handler(websocket):
    """Handles a new laptop connection."""
    _clients.add(websocket)
    print(f"[streamer] Laptop connected: {websocket.remote_address}")
    try:
        await websocket.wait_closed()
    finally:
        _clients.discard(websocket)
        print(f"[streamer] Laptop disconnected")


async def broadcast(state: dict):
    """Send current map state to all connected laptops."""
    if not _clients:
        return
    message = json.dumps(state)
    await asyncio.gather(
        *[client.send(message) for client in _clients],
        return_exceptions=True,
    )


async def start_server():
    """Start the WebSocket server. Call once at startup."""
    print(f"[streamer] Listening on ws://{HOST}:{PORT}")
    async with websockets.serve(_handler, HOST, PORT):
        await asyncio.Future()  # run forever
