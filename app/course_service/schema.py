from typing import Optional
from pydantic import BaseModel
import datetime


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None


class CourseRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    teacher_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
