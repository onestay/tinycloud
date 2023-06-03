from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_user
from ..models.users import User, UserSchema

router = APIRouter()


@router.get("/user/me", response_model=UserSchema)
async def create_user(user: Annotated[User, Depends(get_user)]):
    return user


@router.get("/user/{id}", response_model=UserSchema)
async def get_user_by_id():
    pass
