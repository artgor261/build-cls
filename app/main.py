from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.objects import router as objects_router
from app.api.recognize import router as recognize_router
from app.core.database import engine
from app.core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Build Classifier", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(objects_router)
app.include_router(recognize_router)
