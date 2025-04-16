from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.user_service.schema import Token, UserCreate
from app.user_service.util import authenticate_user, create_access_token, UserDep, oauth2_scheme, blacklist_token, \
    read_me, create_user, get_user, decode_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db import SessionDep

router = APIRouter()


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: SessionDep,
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, 'role': user.role, 'id': user.id}, expires_delta=access_token_expires
    )
    decoded = decode_token(access_token)
    print(decoded)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(
        current_user: UserDep,
        token: Annotated[str, Depends(oauth2_scheme)],
):
    blacklist_token(token)
    return {"message": "Logged out successfully"}


@router.get("/me/", response_model={})
async def read_user_me(
        current_user: UserDep,
        token: Annotated[str, Depends(oauth2_scheme)]
):
    return await read_me(current_user, token)


@router.post("/register")
async def create_user_endpoint(user: UserCreate, db: SessionDep):
    return await create_user(db, user)


@router.get('/user/{user_id}')
async def get_user_endpoint(user_id: int, db: SessionDep, current_user: UserDep):
    return await get_user(db, user_id)

