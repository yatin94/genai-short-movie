
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base
from datetime import datetime


class RequestState(Base):
    __tablename__ = "request_state"
    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    comment: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AllBackgroundTask(Base):
    __tablename__ = "all_background_task"
    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String)
    response_url: Mapped[str] = mapped_column(String, nullable=True)
    response: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    