from fastapi import APIRouter, Request, Depends, WebSocketDisconnect, WebSocket
from schemas.movie import MovieRequest, MovieResponse
from uuid import uuid4
from db_ops.users import UserOperations, User
from db import get_db
from sqlalchemy.orm import Session
import asyncio
from fastapi import BackgroundTasks
from functions.bg_tasks import call_parent_agent_factory
from db_ops.logging import BgTaskOperations

router = APIRouter()

DUPLICATE_EMAIL_ALLOWED = True


@router.post("/movie", response_model=MovieResponse)
async def create_movie(movie_req: MovieRequest, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    # Simulate movie creation logic
    ip_address = request.client.host
    user_operations = UserOperations(db)
    if user_operations.check_ban(ip_address):
        return MovieResponse(message="Your IP has been banned from making requests.")

    if not DUPLICATE_EMAIL_ALLOWED and user_operations.check_email_exists(movie_req.email):
        return MovieResponse(message="Email address is already in use.")

    user = User(
        user_id = str(uuid4()),
        email_address = movie_req.email,
        topic = movie_req.topic,
        ip = ip_address
    )
    user_operations.create_user(user)
    background_tasks.add_task(
        func=call_parent_agent_factory, 
        topic=movie_req.topic, 
        user_id=user.user_id, 
        characters_count=movie_req.characters,
        db=db
    )
    BgTaskOperations(db).create_bg_task(movie_req.topic, user.user_id)
    print("Background task for story generation has been initiated.")
    return MovieResponse(message="Movie request created successfully for topic: " + movie_req.topic, user_id=user.user_id)



@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    user_operations = UserOperations(db)
    topic = user_operations.get_user(user_id).topic

    try:
        while True:
            # topic = user_operations.get_user(user_id).topic
            await websocket.send_json({"message": "Movie request created successfully for topic: " + topic})
            await asyncio.sleep(10)

    except WebSocketDisconnect:
        print("Client disconnected")

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(user_id: str, websocket: WebSocket):
#     await websocket.accept()
#     try:
#         teller_obj = StoryTellerAgent(
#             topic=request.topic, user_id="test_user", characters_count=request.characters
#         )
#         await teller_obj.run()
#         while True:
            
#             topic = data.get("topic")
#             characters = data.get("characters", 2)
#             movie_summary = {"movie_topic": topic, "characters": characters, "id": str(uuid4())}
#             database.append(movie_summary)
#             await websocket.send_json({"message": "Movie request created successfully for topic: " + topic})
#     except WebSocketDisconnect:
#         print("Client disconnected")




