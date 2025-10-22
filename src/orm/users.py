
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from datetime import datetime
from db import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email_address: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    requests: Mapped[list["UserRequest"]] = relationship("UserRequest", back_populates="user")

class AdminUser(Base):
    __tablename__ = "admin_users"

    admin_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)


class UserRequest(Base):
    __tablename__ = "user_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), index=True)
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    character_count: Mapped[int] = mapped_column(default=2, nullable=False)
    story: Mapped["Story"] = relationship("Story", back_populates="request", uselist=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="requests")



class BlockList(Base):
    __tablename__ = "blocklist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)