from __future__ import annotations

import secrets
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.types import TIMESTAMP

from app.models.base import Base
from app.models.users import User


class StorageBackend(Enum):
    Local = 1


class File(Base):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    owner: Mapped[User] = relationship(back_populates="files")
    backend: Mapped[StorageBackend]
    size: Mapped[int]
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    modified: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    is_dir: Mapped[bool]
    is_uploaded: Mapped[bool] = mapped_column(default=False)

    @classmethod
    def create(cls, session: Session, file_in: FileInSchema, user: User) -> File:
        token = secrets.token_hex(32)
        file = File(
            token=token,
            name=file_in.name,
            owner_id=user.user_id,
            size=file_in.size,
            is_dir=file_in.is_dir,
            backend=StorageBackend.Local,
        )

        session.add(file)
        session.commit()
        session.refresh(file)
        print(file)
        return file


class FileBaseSchema(BaseModel):
    pass


class FileInSchema(FileBaseSchema):
    name: str
    size: int
    is_dir: bool


class FileSchema(FileBaseSchema):
    file_id: int
    token: str
    name: str
    backend: StorageBackend
    size: int
    created: datetime
    modified: datetime
    is_dir: bool

    class Config:
        orm_mode = True
