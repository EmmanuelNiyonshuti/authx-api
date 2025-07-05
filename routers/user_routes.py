from fastapi import APIRouter, Depends
from ..schemas.user import UserRead
from ..utils.security import get_current_user

user_router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@user_router.get("/me")
async def read_profile(
    current_user: UserRead = Depends(get_current_user)
    ):
    return current_user
