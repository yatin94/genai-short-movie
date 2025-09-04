from sqlalchemy.orm import Session
from models.stories import Story


class StoryOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_story(self, story_id: int) -> Story:
        return self.db_session.query(Story).filter(Story.id == story_id).first()

    def create_story(self, story: Story) -> Story:
        self.db_session.add(story)
        self.db_session.commit()
        self.db_session.refresh(story)
        return story