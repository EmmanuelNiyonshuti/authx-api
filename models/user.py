from sqlmodel import Field, SQLModel
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory= lambda: str(uuid.uuid4()), primary_key=True)
    name: str | None = Field(default=None)
    email: str
    password: str

