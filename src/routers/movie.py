from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from schemas.movie import MovieRequest, MovieResponse
from uuid import uuid4
from agents.story_teller.llm_init import StoryTellerAgent


router = APIRouter()


database = []


@router.post("/movie", response_model=MovieResponse)
async def create_movie(request: MovieRequest):
    # Simulate movie creation logic
    movie_summary = {"movie_topic": request.topic, "characters": request.characters, "id": str(uuid4())}
    
    database.append(movie_summary)
    return MovieResponse(message="Movie request created successfully for topic: " + request.topic)



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




