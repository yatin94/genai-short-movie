from fastapi import FastAPI, WebSocket
import random
import asyncio
from db import Base, engine, SessionLocal
from routers import movie_router, admin_router
from orm.users import User, BlockList
from orm.stories import Story
from orm.logging import RequestState, AllBackgroundTask
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from db import get_db

from prometheus_fastapi_instrumentator import Instrumentator



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

fresh_data = []

app.include_router(movie_router)
app.include_router(admin_router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    data = db.query(Story).all()
    print(f"data: {data}")
    return {"message": data}
