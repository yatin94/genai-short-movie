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


class StoryScenes(Base):
    __tablename__ = "story_scenes"
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"))
    scene_numer: Mapped[int] = mapped_column(nullable=False)
    scene_heading: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    story: Mapped["Story"] = relationship("Story", back_populates="segments")
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dialouge: Mapped[List["Dialouge"]] = relationship("Dialouge", back_populates="story_scene")


class Dialouge(Base):
    __tablename__ = "dialogues"
    scene_id: Mapped[int] = mapped_column(ForeignKey("story_scenes.id"))
    character: Mapped[str] = mapped_column(String(50), nullable=False)
    line: Mapped[str] = mapped_column(Text, nullable=False)
    story_scene: Mapped["StoryScenes"] = relationship("StoryScenes", back_populates="dialogues")
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

