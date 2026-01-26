"""
Ring: Infrastructure (Database / Session & Connection Management)

Responsibility:
Defines the database engine, ORM base, and session lifecycle management.
This module owns how the application connects to the database and how transactions
are opened, committed, rolled back, and closed.

Design intent:
This is pure infrastructure code.
It centralises all SQLAlchemy configuration and session handling so that:
- Domain code never sees ORM concepts.
- Application code never manages transactions.
- Delivery code only requests a session, without knowing how it is built.

This module contains:
- ORMBase: the declarative base class for all ORM models.
- Engine configuration for the database.
- Session factory (SessionLocal).
- Table creation bootstrap function.
- Session provider with transaction scoping.

Dependency constraints:
- Must not import from the Domain layer (core/).
- Must not import from the Application layer (features/*).
- May depend only on infrastructure libraries and tooling (SQLAlchemy, DB drivers).
- Must not contain business rules or application policy.

Stability:
- Highly volatile.
- Changes when database technology, connection strategy, or transaction model changes.

Usage:
- Called at startup to initialise database tables.
- Used by infrastructure repositories to obtain transactional sessions.
- Used by delivery frameworks (e.g. FastAPI) to inject a session per request.
- Acts as the single source of truth for database connectivity and transaction scope.
"""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

class ORMBase(DeclarativeBase):
    """
    SQLAlchemy ORM base for all mapped models.
    """

# In-memory SQLite
DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # critical for in-memory DB persistence
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def create_all_db_tables() -> None:
    """
    Create all database tables.
    Must be called once at startup.
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
