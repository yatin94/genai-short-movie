from sqlalchemy.orm import Session
from orm.stories import StoryScenes, Dialogue
from schemas.scripts import CreateScript
from typing import List



class SceneOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_scene(self, story_id: int) -> List[StoryScenes]:
        """
        Get script and its dialogues by ID.
        """
        scripts = self.db_session.query(StoryScenes).filter(StoryScenes.story_id == story_id).all()
        return scripts
    
    def get_scene_with_dialogues(self, story_id: int):
        """
        Get script along with its dialogues by scene ID.
        """
        all_diaglogues = []
        scenes = self.db_session.query(StoryScenes).filter(StoryScenes.story_id == story_id).all()
        if scenes:
            for scene in scenes:
                scene_data = [f'Scene : {scene.scene_number}']
                dialogues = self.db_session.query(Dialogue).filter(Dialogue.scene_id == scene.id).all()
                if dialogues:
                    for dialogue in dialogues:
                        scene_data.append(f"\n{dialogue.character}: {dialogue.line}")
                all_diaglogues.append("\n".join(scene_data))

        
        return all_diaglogues

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


