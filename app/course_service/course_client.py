from typing import Annotated

import grpc
import app.user_service.user_pb2 as user_pb2
from app.user_service.user_pb2_grpc import UserServiceStub
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/login")

async def validate_token(token: str):
    try:
        async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
            stub = UserServiceStub(channel)
            try:
                response = await stub.ValidateToken(user_pb2.ValidateTokenRequest(token=token))
                print(token)
                print(f"Response: is_valid={response.is_valid}, user_id={response.user_id}, role={response.role}")
                if not response.is_valid:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid authentication token",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                return {"user_id": response.user_id, "role": response.role}
            except grpc.RpcError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Authentication service error: {str(e)}"
                )
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cannot connect to authentication service: {str(e)}"
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await validate_token(token)

UserDep = Annotated[dict, Depends(get_current_user)]

async def get_teacher(current_user: UserDep):
    if current_user["role"] != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can perform this action"
        )
    return current_user

TeacherDep = Annotated[dict, Depends(get_teacher)]
