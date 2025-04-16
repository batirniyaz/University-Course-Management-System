from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.enrollment_service.enrollment_client import validate_course, get_user_id
from app.enrollment_service.model import Enrollment
from app.enrollment_service.schema import EnrollmentRead, EnrollmentCreate


async def create_enrollment(db: AsyncSession, course_id: int, student_id: int) -> EnrollmentRead:
    """
    Create a new enrollment.
    """
    await validate_course(course_id)
    db_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    return EnrollmentRead.model_validate(db_enrollment)


async def get_enrollment(db: AsyncSession, enrollment_id: int) -> EnrollmentRead:
    """
    Get an enrollment by its ID.
    """
    db_enrollment = await db.execute(select(Enrollment).filter_by(id=enrollment_id))
    db_enrollment = db_enrollment.scalars().first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return EnrollmentRead.model_validate(db_enrollment)


async def get_enrollments_by_student(db: AsyncSession, student_id: int) -> list[EnrollmentRead]:
    """
    Get a list of enrollments with pagination by student.
    """
    db_enrollments = await db.execute(select(Enrollment).filter_by(student_id=student_id))
    db_enrollments = db_enrollments.scalars().all()

    course_ids = set()
    for db_enrollment in db_enrollments:
        course_ids.add(db_enrollment.course_id)

    courses = []
    for course_id in course_ids:
        course = await validate_course(course_id)
        courses.append(course)

    # return [EnrollmentRead.model_validate(enrollment) for enrollment in db_enrollments]
    return courses

async def get_enrollments_by_course(db: AsyncSession, course_id: int) -> list[EnrollmentRead]:
    """
    Get a list of enrollments with pagination by course.
    """
    db_enrollments = await db.execute(select(Enrollment).filter_by(course_id=course_id))
    db_enrollments = db_enrollments.scalars().all()

    student_ids = set()
    for db_enrollment in db_enrollments:
        student_ids.add(db_enrollment.student_id)

    print(f"{student_ids=}")

    students = []
    for student_id in student_ids:
        student = await get_user_id(student_id)
        students.append(student)

    print(f"{students=}")

    # return [EnrollmentRead.model_validate(db_enrollment) for db_enrollment in db_enrollments]
    return students
