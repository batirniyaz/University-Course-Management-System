from datetime import timedelta, datetime
from typing import Annotated, Set
import pytz

from sqlalchemy.future import select

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.exc import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.user_service.model import User
from app.user_service.schema import TokenData, UserRead, UserCreate
from app.config import SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.db import SessionDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

token_blacklist: Set[str] = set()


def blacklist_token(token: str):
    token_blacklist.add(token)


def is_token_blacklisted(token: str) -> bool:
    return token in token_blacklist


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_user_by_username(db: AsyncSession, username: str):
    res = await db.execute(select(User).filter_by(username=username))
    user = res.scalars().first()
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    current_tz = pytz.timezone('Asia/Tashkent')
    if expires_delta:
        expire = datetime.now(current_tz) + expires_delta
    else:
        expire = datetime.now(current_tz) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Invalid token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: SessionDep,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if is_token_blacklisted(token):
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


UserDep = Annotated[UserRead, Depends(get_current_user)]


async def read_me(current_user, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    current_tz = pytz.timezone('Asia/Tashkent')
    new_expire = datetime.now(current_tz) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['exp'] = new_expire
    new_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {"user": current_user, "token": new_token}


async def create_user(db: AsyncSession, user: UserCreate):

    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    if user.role not in ('teacher', 'student'):
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed_password = get_password_hash(user.password)

    try:
        db_user = User(
            username=user.username,
            hashed_password=hashed_password,
            role=user.role
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserRead.model_validate(db_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")


async def get_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).filter_by(id=user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


async def get_users(db: AsyncSession):
    users = await db.execute(select(User))
    users = users.scalars().all()
    return [UserRead.model_validate(user) for user in users]
