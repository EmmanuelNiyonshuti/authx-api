from fastapi import APIRouter, Depends, Body
from sqlmodel import Session
from ..dependencies import SessionDep
from ..services.auth_services import AuthService
from ..schemas.user import UserCreate, UserRead, UserUpdate

auth_router = APIRouter(
    tags=["Authentication"],
    prefix="/auth",
)

@auth_router.post("/register", response_model=UserRead)
async def register(
    user_data: UserCreate,
    session: SessionDep
    ):
    return AuthService.register_user(session, user_data)

@auth_router.post("/login")
async def login():
    pass
@auth_router.post("/logout")
async def logout():
    pass

