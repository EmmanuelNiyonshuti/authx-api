from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import EmailStr
import uuid


# shared properties
class Base(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UserCreate(SQLModel):
    username: str = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class UserRead(Base, SQLModel):
    username: str = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class LoginCredentials(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(SQLModel):
    username: str = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)


class Token(SQLModel):
    access_token: str
    token_type: str


# db model
class User(Base, table=True):
    username: str = Field(default=None, max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    is_active: bool = True
    is_superuser: bool = False
