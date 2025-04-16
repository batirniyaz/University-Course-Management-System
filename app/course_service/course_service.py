from sqlalchemy.future import select
import grpc
import asyncio

import app.course_service.course_pb2 as course_pb2
from app.course_service.course_pb2_grpc import CourseServiceServicer, add_CourseServiceServicer_to_server


class CourseService(CourseServiceServicer):
    async def GetCourseById(self, request, context):
        from app.course_service.model import Course
        from app.db import get_async_session

        async for db in get_async_session():
            course = await db.execute(select(Course).filter_by(id=request.id))
            course = course.scalars().first()
            if not course:
                return course_pb2.GetCourseByIdResponse(
                    id=0,
                    title="",
                    description="",
                )
            return course_pb2.GetCourseByIdResponse(
                id=course.id,
                title=course.title,
                description=course.description,
            )


async def serve():
    server = grpc.aio.server()
    add_CourseServiceServicer_to_server(CourseService(), server)
    server.add_insecure_port("[::]:50052")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    print("Starting gRPC server...")
    asyncio.run(serve())
    print("Done.")