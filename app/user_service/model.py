import datetime

from sqlalchemy import Integer, String, Enum, TIMESTAMP
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[Enum] = mapped_column(Enum("student", "teacher", name="user_roles"))

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
