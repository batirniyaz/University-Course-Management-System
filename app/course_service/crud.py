from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.course_service.model import Course
from app.course_service.schema import CourseCreate, CourseRead


async def create_course(db: AsyncSession, course: CourseCreate, teacher_id: int):

    new_course = Course(
        title=course.title,
        description=course.description,
        teacher_id=teacher_id
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return CourseRead.model_validate(new_course)


async def get_course(db: AsyncSession, course_id: int):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseRead.model_validate(course)


async def get_courses(db: AsyncSession, page: int = 1, limit: int = 10):
    courses = await db.execute(select(Course).offset((page - 1) * limit).limit(limit))
    courses = courses.scalars().all()
    return [CourseRead.model_validate(course) for course in courses]


async def get_courses_by_teacher(db: AsyncSession, teacher_id: int):
    courses = await db.execute(select(Course).filter_by(teacher_id=teacher_id))
    courses = courses.scalars().all()
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return [CourseRead.model_validate(course) for course in courses]