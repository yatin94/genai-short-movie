from sqlalchemy.orm import Session
from orm.stories import Story


class StoryOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_story(self, user_id: str) -> Story:
        return self.db_session.query(Story).filter(Story.user_id == user_id).first()

    def create_story(self, story: Story) -> Story:
        print("Creating story in DB:", story)
        self.db_session.add(story)
        self.db_session.commit()
        self.db_session.refresh(story)
        return story