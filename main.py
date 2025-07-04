from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from .core.database import db_health_check
from .core.logging import setup_logging
from .routers.auth import auth_router

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    if not db_health_check():
        raise Exception("Failed connecting to the database - cannot start application")
    logger.info("Application startup complete")
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Authx-api",
    description="User Authentication and Management API",
    lifespan=lifespan
)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"msg": "Up and Running"}
