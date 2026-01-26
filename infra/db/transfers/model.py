"""
Ring: Infrastructure (Database / ORM Models)

Responsibility:
Defines the persistence model for transfers.
This module maps the domain concept of a Transfer into a relational database
representation using an ORM.

Design intent:
This is a pure infrastructure concern.
It exists only to describe how transfer data is stored and retrieved.
It must not contain business rules or domain behaviour.
It adapts the database to the domain, never the other way around.

This module contains:
- TransferModel: the ORM mapping for the transfers table.

Dependency constraints:
- Must not import from the application layer (features/*).
- May depend on the Domain layer only for conceptual alignment, never for behaviour.
- May depend on infrastructure tooling (SQLAlchemy, DB session, etc.).

Stability:
- Highly volatile.
- Changes when the database schema or persistence technology changes.

Usage:
- Used by infrastructure repositories to persist and load transfer data.
- Never imported by domain or application code.
- Acts as the lowest-level adapter between the database and the system.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.session import ORMBase


class TransferModel(ORMBase):
    """
    ORM model for transfers.
    """

    __tablename__ = "transfers"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    from_account_id: Mapped[str] = mapped_column(String, nullable=False)
    to_account_id: Mapped[str] = mapped_column(String, nullable=False)

    amount_pence: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
