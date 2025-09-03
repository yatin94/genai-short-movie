from fastapi import FastAPI
import random
import asyncio
from contextlib import asynccontextmanager
from db import Base, engine
from routers import movie_router
from models import users, stories

async def generate_data():
    while True:
        fresh_data.append(random.randint(1, 100))
        # Keep only last 100 items to avoid memory bloat
        if len(fresh_data) > 5:
            fresh_data.pop(0)
        # Broadcast latest value to all connected clients
        await asyncio.sleep(5)  # Generate every 1 second


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Hereeeeeeseee")
    Base.metadata.create_all(bind=engine)
    yield
    # stop all async tasks here if needed
    asyncio.get_event_loop().stop()




app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Hereeeeeeeee")

fresh_data = []

app.include_router(movie_router)



@app.get("/")
async def read_root():
    asyncio.create_task(generate_data())
    return {"message": "Hello, FastAPI with Poetry!"}

