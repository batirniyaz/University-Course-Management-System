from fastapi import APIRouter

from app.course_service.course_client import TeacherDep, UserDep
from app.course_service.schema import CourseCreate
from app.db import SessionDep
from app.course_service.crud import create_course, get_course, get_courses, get_courses_by_teacher

router = APIRouter()


@router.post("/")
async def create_course_endpoint(
        course: CourseCreate,
        db: SessionDep,
        current_user: TeacherDep,
):
    """
    Create a new course.
    """
    print(current_user)
    return await create_course(db, course, current_user['user_id'])


@router.get("/{course_id}")
async def get_course_endpoint(
        course_id: int,
        db: SessionDep,
        current_user: UserDep,
):
    """
    Get a course by its ID.
    """
    return await get_course(db, course_id)


@router.get("/")
async def get_courses_endpoint(
        db: SessionDep,
        current_user: UserDep,
        page: int = 1,
        limit: int = 10
):
    """
    Get a list of courses with pagination.
    """
    return await get_courses(db, page, limit)


@router.get("/teacher/")
async def get_courses_by_teacher_endpoint(
        db: SessionDep,
        current_user: TeacherDep,
):
    """
    Get all courses by a specific teacher.
    """
    return await get_courses_by_teacher(db, current_user['user_id'])
