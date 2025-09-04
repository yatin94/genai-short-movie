
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email_address: Mapped[str] = mapped_column(String, index=True, nullable=False)
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    character_count: Mapped[int] = mapped_column(default=2, nullable=False)
    story: Mapped["Story"] = relationship("Story", back_populates="user", uselist=False)





class BlockList(Base):
    __tablename__ = "blocklist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)