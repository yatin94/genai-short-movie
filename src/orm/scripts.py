from sqlalchemy.orm import Session
from models.stories import StoryScenes, Dialouge
from schemas.scripts import CreateScript

class ScriptOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_script(self, script_id: int) -> StoryScenes:
        """
        Get script and its dialogues by ID.
        """
        scripts = self.db_session.query(StoryScenes).filter(StoryScenes.id == script_id).first()
        return scripts

    def create_script(self, script: CreateScript) -> None:
        print("Creating script in DB:", script)
        with Session() as session:
            script = StoryScenes(
                story_id=script.story_id,
                scene_number=script.scene_number,
                scene_heading=script.scene_heading,
                action=script.action
            )
            session.add(script)
            session.flush()

            for dialogue in script.dialogues:
                dialogue_entry = Dialouge(
                    character=dialogue.character,
                    line=dialogue.line,
                    scene_id=script.id
                )
                session.add(dialogue_entry)
                print("Created dialogue:", dialogue_entry)
            
            session.commit()
        

