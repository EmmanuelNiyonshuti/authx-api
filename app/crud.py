from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from sqlmodel import Session, select
import uuid

from app.models.user import User, UserCreate, UserRead
from app.core.security import get_password_hash, verify_password
from app.api.deps import CurrentUser


def register_user(session: Session, user_data: UserCreate) -> UserRead:
    user_exists = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    pwd_hash = get_password_hash(user_data.password)
    user_data_obj = user_data.model_dump(exclude={"password"})
    new_user = User(**user_data_obj, password=pwd_hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserRead.model_validate(jsonable_encoder(new_user), from_attributes=True)


def authenticate_user(session: Session, form_data):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def delete_user(
    session: Session, current_user: CurrentUser, user_id: str
) -> None:
    user = session.exec(select(User).where(User.id == uuid.UUID(user_id))).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} does not exists",
        )
    user_obj = jsonable_encoder(user)
    current_user = jsonable_encoder(current_user)
    if not (current_user["is_superuser"] or user_id == user_obj["id"]):
        raise HTTPException(
            status_code=403,
            detail="Forbidden, you don't have permissions to perform this action.",
        )
    session.delete(user)
    session.commit()
