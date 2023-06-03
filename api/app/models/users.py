from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from app.fs import make_user_dir

from .base import Base

if TYPE_CHECKING:
    from .files import File
    from .session import UserSession


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    password: Mapped[str]
    profile_picture: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    sessions: Mapped[list[UserSession]] = relationship(back_populates="user")
    files: Mapped[list[File]] = relationship(back_populates="owner")
    base_dir: Mapped[UserLocalStorageBaseDir | None] = relationship(
        back_populates="user"
    )

    @classmethod
    def create(
        cls,
        session: Session,
        user_in: UserInSchema,
        create_local_storage: bool = True,
    ):
        db_user = User(
            email=user_in.email, name=user_in.name, password=user_in.password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        if create_local_storage:
            UserLocalStorageBaseDir.create(session, db_user)

        return db_user

    @classmethod
    def get_by_id(cls, session: Session, user_id: int) -> User | None:
        stmt = select(cls).where(cls.user_id == user_id)

        return session.scalar(stmt)

    @classmethod
    def get_by_email(cls, session: Session, email: str) -> User | None:
        stmt = select(cls).where(cls.email == email)

        return session.scalar(stmt)


class UserLocalStorageBaseDir(Base):
    __tablename__ = "user_storage_base_dirs"
    local_storage_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped[User] = relationship(back_populates="base_dir")
    path: Mapped[str] = mapped_column(index=True)

    @classmethod
    def create(cls, session: Session, user: User):
        path = make_user_dir(user.user_id)
        base_dir_db = UserLocalStorageBaseDir(user_id=user.user_id, path=str(path))
        session.add(base_dir_db)
        session.commit()


class UserBaseSchema(BaseModel):
    name: str


class UserInSchema(UserBaseSchema):
    email: str
    password: str


class UserSchema(UserBaseSchema):
    user_id: int
    email: str
    name: str
    profile_picture: str | None
    is_active: bool

    class Config:
        orm_mode = True
