import jwt
import random


from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

key = random.randbytes(32)

security = HTTPBearer()  # This parses the Authorization: Bearer <token> header


def encode_jwt(admin_id: int) -> str:
    payload = {"admin_id": admin_id}
    token = jwt.encode(payload, key, algorithm="HS256")
    return token


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, key, algorithm='HS256')



def decode_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        return payload  # You can return user info from the token (like user_id or role)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
