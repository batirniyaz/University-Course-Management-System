import datetime

from sqlalchemy import Integer, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Enrollment(Base):
    __tablename__ = "enrollment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)
