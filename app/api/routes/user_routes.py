from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.crud import delete_user
from app.api.deps import SessionDep

user_router = APIRouter(tags=["Users"], prefix="/users")

@user_router.get("/me")
async def read_profile(current_user: CurrentUser):
    return current_user

@user_router.delete("/{user_id}")
async def delete_account(
    session: SessionDep,
    current_user: CurrentUser,
    user_id: str,
    ):
    await delete_user(session, current_user, user_id)
    return { "msg": "success"}
