import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import db_health_check
from app.core.logging import setup_logging
from app.api.main import api_router

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
    lifespan=lifespan,
    root_path="/api",
)
app.include_router(api_router)
