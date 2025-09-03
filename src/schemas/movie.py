from pydantic import BaseModel


class MovieRequest(BaseModel):
    topic: str
    characters: int = 2

class MovieResponse(BaseModel):
    message: str

