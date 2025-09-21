from pydantic import BaseModel


class ScriptDialouges(BaseModel):
    character: str
    line: str


class CreateScript(BaseModel):
    story_id: int
    scene_number: int
    scene_heading: str
    action: str
    dialogues: list[ScriptDialouges] = []

