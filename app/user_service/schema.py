from enum import Enum
from typing import Optional
from pydantic import BaseModel
import datetime


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole


class UserRead(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
