from typing import List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base



class Story(Base):
    __tablename__ = "stories"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    story_text: Mapped[str] = mapped_column(Text, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="story")
    id: Mapped[int] = mapped_column(primary_key=True, index=True)



