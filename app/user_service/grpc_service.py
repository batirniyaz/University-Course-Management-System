from sqlalchemy.future import select
import grpc
import asyncio

import app.user_service.user_pb2 as user_pb2
from app.user_service.user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server


class UserService(UserServiceServicer):
    async def GetUserById(self, request, context):
        from app.user_service.model import User
        from app.db import get_async_session

        async for db in get_async_session():
            user = await db.execute(select(User).filter_by(id=request.id))
            user = user.scalars().first()
            if not user:
                context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
            return user_pb2.GetUserByIdResponse(
                id=user.id,
                username=user.username,
                role=user.role
            )

    async def ValidateToken(self, request, context):
        from app.user_service.util import decode_token

        try:
            payload = decode_token(request.token)
            username = payload.get("sub")
            user_id = payload.get("id")
            role = payload.get("role")
            print(payload)

            return user_pb2.ValidateTokenResponse(
                is_valid=True,
                user_id=user_id,
                role=role
            )

        except Exception as e:
            print(f"Token validation failed: {str(e)}")
            return user_pb2.ValidateTokenResponse(
                is_valid=False,
                user_id=0,
                role=""
            )


async def serve():
    server = grpc.aio.server()
    add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    print("Starting gRPC server...")
    asyncio.run(serve())
    print("Done.")