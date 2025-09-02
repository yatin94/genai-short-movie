from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import asyncio

app = FastAPI()

fresh_data = []

async def generate_data():
    while True:
        fresh_data.append(random.randint(1, 100))
        # Keep only last 100 items to avoid memory bloat
        if len(fresh_data) > 100:
            fresh_data.pop(0)
        # Broadcast latest value to all connected clients
        await asyncio.sleep(5)  # Generate every 1 second




@app.get("/")
async def read_root():
    asyncio.create_task(generate_data())
    return {"message": "Hello, FastAPI with Poetry!"}


async def get_movie_request():
    # Simulate a delay for fetching movie data
    await asyncio.sleep(2)
    return {"movie": "Inception", "director": "Christopher Nolan"}


@app.websocket("/ws")
async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(10)  # Adjust the frequency as needed
            await websocket.send_text(f"Message received: {fresh_data[-1] if fresh_data else 'No data yet'}")
    except WebSocketDisconnect:
        print("Client disconnected")
