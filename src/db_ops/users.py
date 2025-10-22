from sqlalchemy.orm import Session
from orm.users import UserRequest, User, BlockList, AdminUser
from uuid import uuid4



class UserOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_user(self, email: str) -> User | None:
        user_obj: User = self.db_session.query(User).filter(User.email_address == email).first()
        if user_obj:
            return user_obj
        else:
            return None
    
    def get_user_by_id(self, user_id: str) -> User | None:
        user_obj: User = self.db_session.query(User).filter(User.user_id == user_id).first()
        if user_obj:
            return user_obj
        else:
            return None

    def get_all_users(self) -> list[User]:
        return self.db_session.query(User).all()

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def ban_user(self, ip: str) -> BlockList:
        banned_ip = BlockList(ip=ip)
        self.db_session.add(banned_ip)
        self.db_session.commit()
        self.db_session.refresh(banned_ip)
        return banned_ip

    def check_ban(self, ip: str) -> bool:
        banned_ip = self.db_session.query(BlockList).filter(BlockList.ip == ip).first()
        return banned_ip is not None

    def check_email_exists(self, email: str) -> bool:
        existing_user = self.db_session.query(User).filter(User.email_address == email).first()
        return existing_user is not None
    

class UserRequestOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_user_request(self, user_id: str, topic: str, ip: str, character_count: int) -> UserRequest:
        user_request = UserRequest(
            user_id=user_id,
            topic=topic,
            ip=ip,
            character_count=character_count,
            id=str(uuid4())
        )
        self.db_session.add(user_request)
        self.db_session.commit()
        self.db_session.refresh(user_request)
    
        return user_request

    def get_user_request_by_id(self, request_id: str, user_id: str) -> UserRequest | None:
        return self.db_session.query(UserRequest).filter(UserRequest.id == request_id, UserRequest.user_id == user_id).first()
