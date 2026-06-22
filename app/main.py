from fastapi import FastAPI

from app.database import Base
from app.database import engine
from app.auth import models
from app.auth.router import router as auth_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Backend Running"}


@app.get("/health")
async def health():
    async with engine.begin():
        pass

    return {"database": "connected"}
