from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config


def make_db_url() -> str:
    return f"postgresql+psycopg://{config.DB_USER}:{config.DB_PASS}@{config.DB_ADDR}/{config.DB_NAME}"


engine = create_engine(make_db_url(), pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
