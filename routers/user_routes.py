from fastapi import APIRouter, Depends

from ..schemas.user import UserRead
from ..deps import CurrentUser

user_router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@user_router.get("/me")
async def read_profile(
    current_user: CurrentUser
    ):
    return current_user
