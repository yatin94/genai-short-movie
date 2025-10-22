
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email_address: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    requests: Mapped[list["UserRequest"]] = relationship("UserRequest", back_populates="user")

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