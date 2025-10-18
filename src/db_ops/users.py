from sqlalchemy.orm import Session
from orm.users import User, BlockList


class UserOperations:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_user(self, user_id: str) -> User:
        return self.db_session.query(User).filter(User.user_id == user_id).first()

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