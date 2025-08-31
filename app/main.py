from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.config import settings
from .database import engine
from .models import Base
from .routers import scores, students


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create DB tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

# Include routers
app.include_router(students.router)
app.include_router(scores.router)


@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    return {"status": "ok"}

