import datetime

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped
from app.db import Base

class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    teacher_id: Mapped[int] = mapped_column(Integer, index=True)  # fetched from User Service

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
