from fastapi import APIRouter, Request, Depends, WebSocketDisconnect, WebSocket
from schemas.movie import MovieRequest, MovieResponse
from uuid import uuid4
from db_ops.users import UserOperations, User
from db_ops.logging import UserStateOperations
from db import get_db
from sqlalchemy.orm import Session
import asyncio
from fastapi import BackgroundTasks
from functions.bg_tasks import call_parent_agent_factory
from db_ops.logging import BgTaskOperations
from src.db_ops.logging import UserStateOperations
from src.db_ops.stories import StoryOperations
from src.db_ops.scripts import SceneOperations
from src.bg_tasks import call_parent_agent_factory
from src.log_mechs import get_user_logger

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
    get_user_logger(user.user_id).info(f"User created with ID: {user.user_id}, Email: {user.email_address}, Topic: {user.topic}, IP: {user.ip}")
    call_parent_agent_factory.delay(topic=movie_req.topic, user_id=user.user_id, characters_count=movie_req.characters) # type: ignore

    # background_tasks.add_task(
    #     func=call_parent_agent_factory, 
    #     topic=movie_req.topic, 
    #     user_id=user.user_id, 
    #     characters_count=movie_req.characters,
    #     db=db
    # )
    BgTaskOperations(db).create_bg_task(movie_req.topic, user.user_id)
    UserStateOperations(db).create_request_state(comment="Background Task Submitted.", user_id=user.user_id, status="success")
    print("Background task for story generation has been initiated.")
    return MovieResponse(message="Movie request created successfully for topic: " + movie_req.topic, user_id=user.user_id)



@router.websocket("/logs/{user_id}")
async def get_logs(websocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    user_operations = UserOperations(db)
    last_message = ""
    user_obj = user_operations.get_user(user_id)
    
    if not user_obj:
        await asyncio.sleep(30)
        await websocket.send_json({"message": "Invalid user ID."})
        await websocket.close()
        return
    
    try:
        while True:
            if websocket.client_state.name != "CONNECTED":
                await websocket.close()
                break
            if not last_message:
                all_messages = UserStateOperations(db).get_all_request_states(user_id)
                for msg in reversed(all_messages):
                    await websocket.send_json({"message": msg.comment, "status": msg.status.value})
                    await asyncio.sleep(2)
                last_message = all_messages[-1].comment if all_messages else ""
                await asyncio.sleep(20)

            messages = UserStateOperations(db).get_request_state(user_id)
            if messages and messages.comment != last_message:
                last_message = messages.comment
                await websocket.send_json({"message": last_message, "status": messages.status.value})
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
            

    except WebSocketDisconnect:
        print("Client disconnected")




@router.websocket("/data/{user_id}")
async def get_real_time_data(websocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    user_operations = UserOperations(db)
    user_obj = user_operations.get_user(user_id)
    
    if not user_obj:
        await asyncio.sleep(30)
        await websocket.send_json({"message": "Invalid user ID."})
        await websocket.close()
        return
    
    story_sent = False
    story_id = 0
    scene_sent = False
    
    try:
        while True:
            if websocket.client_state.name != "CONNECTED":
                await websocket.close()
                break
            if not story_sent:
                story_obj = StoryOperations(db)
                story_object = story_obj.get_story(user_id)
                if story_object:
                    story_id = story_object.id
                    await websocket.send_json({"story": story_object.story_text})
                    story_sent = True
                await asyncio.sleep(1)
            elif not scene_sent:
                script_ops = SceneOperations(db)
                script_object: list = script_ops.get_scene_with_dialogues(story_id)
                if script_object:
                    for script in script_object:
                        await websocket.send_json({"script": script})
                    scene_sent = True
                await asyncio.sleep(1)
            

    except WebSocketDisconnect:
        print("Client disconnected")

