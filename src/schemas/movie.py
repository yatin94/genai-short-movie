from pydantic import BaseModel


class MovieRequest(BaseModel):
    topic: str
    characters: int = 2
    email: str

class MovieResponse(BaseModel):
    message: str
    user_id: str | None = None

