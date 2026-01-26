"""
Ring: Infrastructure (Database / ORM Models)

Responsibility:
Defines the persistence model for accounts.
This module maps the domain concept of an Account into a relational database
representation using an ORM.

Design intent:
This is a pure infrastructure concern.
It exists only to describe how account data is stored and retrieved.
It must not contain business rules or domain behaviour.
It adapts the database to the domain, never the other way around.

This module contains:
- AccountModel: the ORM mapping for the accounts table.

Dependency constraints:
- Must not import from the application layer (features/*).
- May depend on the Domain layer only for conceptual alignment, never for behaviour.
- May depend on infrastructure tooling (SQLAlchemy, DB session, etc.).

Stability:
- Highly volatile.
- Changes when the database schema or persistence technology changes.

Usage:
- Used by infrastructure repositories to persist and load account data.
- Never imported by domain or application code.
- Acts as the lowest-level adapter between the database and the system.
"""
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.session import ORMBase


class AccountModel(ORMBase):
    """
    ORM model for accounts.
    """

    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    balance_pence: Mapped[int] = mapped_column(Integer, nullable=False)
