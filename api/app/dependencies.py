import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models.session import UserSession
from app.models.users import User

from .database import SessionLocal

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db)],
) -> User:
    user = UserSession.get_user_by_session(session, token)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
