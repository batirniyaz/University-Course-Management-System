from fastapi import APIRouter

from app.enrollment_service.schema import EnrollmentCreate
from app.db import SessionDep
from app.enrollment_service.enrollment_client import StudentDep
from app.enrollment_service.crud import create_enrollment, get_enrollment, get_enrollments_by_student, get_enrollments_by_course

router = APIRouter()


@router.post("/")
async def create_enrollment_endpoint(
        enrollment: EnrollmentCreate,
        db: SessionDep,
        current_user: StudentDep,
):
    """
    Create a new enrollment.
    """
    return await create_enrollment(db, enrollment.course_id, current_user['user_id'])


@router.get("/{enrollment_id}")
async def get_enrollment_endpoint(
        enrollment_id: int,
        db: SessionDep,
        current_user: StudentDep,
):
    """
    Get an enrollment by its ID.
    """
    return await get_enrollment(db, enrollment_id)


@router.get("/student/")
async def get_enrollments_by_student_endpoint(
        db: SessionDep,
        current_user: StudentDep,
):
    """
    Get a list of enrollments with pagination by student.
    """
    return await get_enrollments_by_student(db, current_user['user_id'])


@router.get("/course/")
async def get_enrollments_by_course_endpoint(
        db: SessionDep,
        current_user: StudentDep,
        course_id: int
):
    """
    Get a list of enrollments with pagination by course.
    """
    return await get_enrollments_by_course(db, course_id)

