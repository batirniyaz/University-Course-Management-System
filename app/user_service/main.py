from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_db_and_tables
from app.user_service.routes import router


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    await create_db_and_tables()

    yield


app = FastAPI(
    title="User Service",
    version="0.1",
    summary="...",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "This is the root endpoint of the User Service"}


app.include_router(router, prefix="/auth", tags=["Auth"])


