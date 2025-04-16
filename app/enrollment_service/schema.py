from pydantic import BaseModel
import datetime


class EnrollmentCreate(BaseModel):
    course_id: int


class EnrollmentRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
