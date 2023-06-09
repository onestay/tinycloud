from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.session import UserSession, UserSessionSchema

from ..dependencies import get_db
from ..models.users import User, UserInSchema

router = APIRouter()

pwd_context = CryptContext(schemes=["argon2"])


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)


@router.post("/login/", response_model=UserSessionSchema)
def login(
    session: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = User.get_by_email(session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = UserSession.create(session, user.user_id).token

    return UserSessionSchema(access_token=token)


@router.post("/register/", response_model=UserSessionSchema)
def register(session: Annotated[Session, Depends(get_db)], user_in: UserInSchema):
    hashed_password = hash_password(user_in.password)
    user_in.password = hashed_password
    user = User.create(session, user_in)

    token = UserSession.create(session, user.user_id).token
    return UserSessionSchema(access_token=token)
