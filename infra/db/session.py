# infra/db/session.py
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class ORMBase(DeclarativeBase):
    """
    SQLAlchemy ORM base for all mapped models.
    """


DATABASE_URL = "sqlite+pysqlite:///./demo.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def create_all_db_tables() -> None:
    """
    Create all database tables.
    """
    ORMBase.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency: provides a transactional session per request.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
