from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel

# from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from .base import Base
from .users import User

DEFAULT_TOKEN_LENGTH = timedelta(hours=2)
TOKEN_BYTES = 32


class UserSession(Base):
    __tablename__ = "sessions"

    user_id = mapped_column(ForeignKey("users.user_id"))
    token: Mapped[str] = mapped_column(primary_key=True)
    expires: Mapped[datetime] = mapped_column()
    user: Mapped[User] = relationship(back_populates="sessions")

    @classmethod
    def create(
        cls, session: Session, user_id: int, expires: datetime | None = None
    ) -> UserSession:
        if expires is None:
            expires = datetime.now(tz=timezone.utc) + DEFAULT_TOKEN_LENGTH
        token = secrets.token_urlsafe(TOKEN_BYTES)
        db_session = UserSession(user_id=user_id, token=token, expires=expires)

        session.add(db_session)
        session.commit()

        return db_session

    @classmethod
    def get_session(cls, session: Session, token: str) -> UserSession | None:
        stmt = select(cls).where(cls.token == token)

        user_session = session.scalar(stmt)
        if user_session is not None and not user_session.expires < datetime.now(
            tz=timezone.utc
        ):
            return user_session

        return None

    @classmethod
    def get_user_by_session(cls, session: Session, token: str) -> User | None:
        user_session = cls.get_session(session, token)
        return user_session.user if user_session is not None else None


class UserSessionSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True
