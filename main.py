from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from .core.database import db_health_check
from .core.logging import setup_logging
from .routers.auth_routes import auth_router
from .routers.user_routes import user_router

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
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"msg": "Up and Running"}


# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     session: SessionDep
#     ) -> Token:
#     user = AuthService.authenticate_user(session, form_data)
#     access_token = create_access_token(data={"user_id": user.id})
#     return Token(access_token=access_token, token_type="bearer")
