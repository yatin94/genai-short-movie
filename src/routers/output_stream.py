from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()


connections = []


@router.websocket("/ws")
async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(10)  # Adjust the frequency as needed
            await websocket.send_text(f"Message received: {fresh_data[-1] if fresh_data else 'No data yet'}")
    except WebSocketDisconnect:
        print("Client disconnected")