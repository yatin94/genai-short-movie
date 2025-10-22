import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.db_ops.users import UserOperations, User, UserRequestOperations
from db import get_db
from sqlalchemy.orm import Session
from typing import List, TypedDict
from pathlib import Path
import httpx


class UserRequests(TypedDict):
    id: str
    ip: str
    topic: str
    created_at: str

class Users(TypedDict):
    user_id: str
    email_address: str
    requests: List[UserRequests]

class AdminDashboardResponse(TypedDict):
    users: List[Users]
    unique_ip_count: int
    total_requests: int
    total_users: int
    

router = APIRouter()

@router.get("/admin", response_class=JSONResponse)
async def admin_dashboard(db: Session = Depends(get_db)) -> JSONResponse:
    users: List[User] = UserOperations(db_session=db).get_all_users()
    admin_dashboard_response: AdminDashboardResponse = {
        "users": [
            {
                "user_id": user.user_id,
                "email_address": user.email_address,
                "requests": [
                    {
                        "id": request.id,
                        "ip": request.ip,
                        "topic": request.topic,
                        "created_at": request.created_at.isoformat()
                    } for request in user.requests
                ]

            } for user in users
        ],
        "unique_ip_count": sum(len(set(request.ip for request in user.requests)) for user in users),
        "total_requests": sum(len(user.requests) for user in users),
        "total_users": len(users)
    }
    return JSONResponse(content=admin_dashboard_response)


# {"bg_status":success, logs: ""}


async def get_bg_status_from_flower(request_id: str) -> str:
    flower_url = f"http://genai-short-movie-flower:5555/api/task/info/{request_id}"
    print(flower_url)
    async with httpx.AsyncClient() as client:
        resp = await client.get(flower_url)
        print(resp.status_code)
        if resp.status_code == 200:
            data = resp.json()
            print(data)
            # The status is in data['state']
            return data.get("state", "UNKNOWN")
        return "NOT_FOUND"

@router.get("/bgstatus/{user_id}/{request_id}", response_class=JSONResponse)
async def get_user_logs(user_id: str, request_id: str, db: Session = Depends(get_db)) -> JSONResponse:
    user_operations = UserOperations(db)
    user_request_operations = UserRequestOperations(db)
    user = user_operations.get_user_by_id(user_id)
    if not user:
        return JSONResponse(content={"message": "User not found."}, status_code=400)

    user_request = user_request_operations.get_user_request_by_id(request_id, user_id)
    if not user_request:
        return JSONResponse(content={"message": "Request not found for this user."}, status_code=400)
    
    logs_dir = Path("logs")
    user_log_file = logs_dir / f"{user_request.id}.json"
    log_lines = []
    if user_log_file.exists():
        with open(user_log_file, "r") as f:
            log_lines = [json.loads(line.strip()) for line in f if line.strip()]
    
    bg_status = await get_bg_status_from_flower(request_id)
        
    return JSONResponse(content={"bg_status": bg_status, "logs": log_lines})
