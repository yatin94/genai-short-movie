from typing import List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email_address: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    topic: Mapped[str] = mapped_column(Text, nullable=False)

    stories: Mapped[List["Story"]] = relationship("Story", back_populates="user")

