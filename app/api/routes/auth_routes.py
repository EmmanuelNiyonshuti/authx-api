from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.services.auth_services import AuthService
from app.models.user import UserCreate, UserRead, Token
from app.core.security import create_access_token

auth_router = APIRouter(
    tags=["Authentication"],
    prefix="/auth",
)


@auth_router.post("/register", response_model=UserRead)
async def register(user_data: UserCreate, session: SessionDep):
    return AuthService.register_user(session, user_data)


@auth_router.post("/login/access_token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = AuthService.authenticate_user(session, form_data)
    access_token = create_access_token(data={"user_id": user.id})
    return Token(access_token=access_token, token_type="bearer")
