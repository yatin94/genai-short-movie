from sqlalchemy.orm import Session
from orm.stories import StoryScenes, Dialogue
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

    def create_script(self, script_data: CreateScript) -> StoryScenes:
        print("Creating script in DB:", script_data)
        try:
            story_scene = StoryScenes(
                story_id=script_data.story_id,
                scene_number=script_data.scene_number,
            )
            self.db_session.add(story_scene)
            self.db_session.flush()

            for dialogue in script_data.dialogues:
                dialogue_entry = Dialogue(
                    character=dialogue.character,
                    line=dialogue.line,
                    scene_id=story_scene.id
                )
                self.db_session.add(dialogue_entry)
                print("Created dialogue:", dialogue_entry)
            
            self.db_session.commit()
            return story_scene
        except Exception as e:
            self.db_session.rollback()
            print("Error creating script:", e)
            raise


