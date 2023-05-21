from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_user
from app.models.files import File, FileInSchema, FileSchema
from app.models.users import User

router = APIRouter(prefix="/files")


@router.post("/create", response_model=FileSchema)
def file_create(
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
    file_in: FileInSchema,
):
    file = File.create(session, file_in, user)
    print(f"The file has the id: {file.id}")

    return file


@router.post("/upload/full")
def file_upload_full(file: UploadFile):
    pass
