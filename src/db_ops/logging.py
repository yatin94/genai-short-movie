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


class UserStateOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session


    def create_request_state(self, comment: str, user_id: str, status: str) -> RequestState:
        request_state = RequestState(
            user_id = user_id,
            comment = comment,
            status = status
        )
        self.db_session.add(request_state)
        self.db_session.commit()
        self.db_session.refresh(request_state)
        return request_state
    
    def get_request_state(self, user_id: str) -> RequestState | None:
        return (
            self.db_session.query(RequestState)
            .filter(RequestState.user_id == user_id)
            .order_by(RequestState.created_at.desc())
            .first()
        )
    
    def get_all_request_states(self, user_id: str, exclude_ids = []) -> list[RequestState]:
        return (
            self.db_session.query(RequestState)
            .filter(RequestState.user_id == user_id)
            .filter(RequestState.id.notin_(exclude_ids))
            .order_by(RequestState.id.asc())
            .all()
        )