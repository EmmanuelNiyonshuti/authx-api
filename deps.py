from fastapi import Depends
from typing import Annotated
from sqlmodel import Session
from .core.database import engine

def get_session():
    """ generator-based dependency to yield a fresh DB session """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
