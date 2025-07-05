from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str | None = None
    email: str
    password: str

class UserRead(BaseModel):
    id: str
    name: str | None = None
    email: str

class LoginCredentials(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str | None
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
