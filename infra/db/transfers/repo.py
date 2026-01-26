"""
Ring: Infrastructure (Persistence / Repositories)

Responsibility:
Implements the Transfer repository using SQLAlchemy.
This module provides a concrete persistence adapter for the TransferRepoPort defined
by the application layer.

Design intent:
This is an infrastructure implementation of an application-facing port.
It adapts the database and ORM to the needs of the application, never the reverse.
All SQLAlchemy and session mechanics are contained here so that application and
domain layers remain persistence-agnostic.

This module contains:
- TransferRepo: a SQLAlchemy-backed implementation of TransferRepoPort.

Dependency constraints:
- Must not be imported by application use case code directly (wired through DI).
- Must depend on application ports (features/transfers/ports) to implement them.
- May depend on the Domain layer (core/) for entities and value types.
- May depend on infrastructure tooling (SQLAlchemy, sessions, ORM models).

Stability:
- Highly volatile.
- Changes when persistence technology, schema, or ORM usage changes.

Usage:
- Instantiated and wired in the infrastructure or root layer.
- Used by application interactors through the TransferRepoPort interface.
- Serves as the concrete bridge between relational storage and domain transfer facts.
"""
from __future__ import annotations

from sqlalchemy.orm import Session
from core.entities.transfer import Transfer
from features.transfers.ports import TransferRepoPort
from infra.db.transfers.mapper import to_model


class TransferRepo(TransferRepoPort):
    """
    SQLAlchemy-backed TransferRepo.

    Persistence adapter for Transfer facts.
    """

    def __init__(self, *, session: Session) -> None:
        self._session = session

    def save(self, transfer: Transfer) -> None:
        self._session.add(to_model(transfer))
