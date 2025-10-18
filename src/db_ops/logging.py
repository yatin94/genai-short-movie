from sqlalchemy.orm import Session
from orm.logging import AllBackgroundTask, RequestState


class BgTaskOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session


    def create_bg_task(self, topic: str, user_id: str) -> AllBackgroundTask:
        bg_task = AllBackgroundTask(
            user_id = user_id,
            topic = topic
        )
        self.db_session.add(bg_task)
        self.db_session.commit()
        self.db_session.refresh(bg_task)
        return bg_task
