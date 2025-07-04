from fastapi import HTTPException
from sqlmodel import Session, select
from ..schemas.user import UserCreate, UserRead, LoginCredentials, UserUpdate
from ..models.user import User
from ..utils.security import get_password_hash, verify_password

class AuthService:
    @staticmethod
    def register_user(session: Session, user_data: UserCreate) -> UserRead:
        user_exists = session.exec(
            select(User).where(User.email == user_data.email)
        ).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="User already exists")
        pwd_hash = get_password_hash(user_data.password)
        new_user = User(
                        **user_data.dict(exclude={"password"}),
                        password=pwd_hash
                        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        new_user_dict = UserRead.model_dump(new_user)
        return UserRead.model_validate(new_user_dict)

    @staticmethod
    def login_user(session: Session, login_details: LoginCredentials):
        user_exists = session.exec(
            select(User).where(User.email == login_details.email)
        ).first()
        if not user_exists or not verify_password(login_details.password, user_exists.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
    # generate jwt bearer token with expiration time and send it back