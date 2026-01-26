"""
Ring: Infrastructure (Persistence / Repositories)

Responsibility:
Implements the Account repository using SQLAlchemy.
This module provides a concrete persistence adapter for the AccountRepoPort defined
by the application layer.

Design intent:
This is an infrastructure implementation of an application-facing port.
It adapts the database and ORM to the needs of the application, never the reverse.
All SQLAlchemy and session mechanics are contained here so that application and
domain layers remain persistence-agnostic.

This module contains:
- AccountRepo: a SQLAlchemy-backed implementation of AccountRepoPort.

Dependency constraints:
- Must not be imported application use case code directly (pass down through DI instead).
- Must depend on application ports (features/accounts/ports) to implement them.
- May depend on the Domain layer (core/) for entities and value types.
- May depend on infrastructure tooling (SQLAlchemy, sessions, ORM models).

Stability:
- Highly volatile.
- Changes when persistence technology, schema, or ORM usage changes.

Usage:
- Instantiated and wired in the infrastructure or root layer.
- Used by application interactors through the AccountRepoPort interface.
- Serves as the concrete bridge between relational storage and domain entities.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entities.account import Account
from core.values.custom_types import AccountId
from features.accounts.ports import AccountRepoPort
from infra.db.accounts.mapper import to_entity, to_model
from infra.db.accounts.model import AccountModel


class AccountRepo(AccountRepoPort):
    """
    SQLAlchemy-backed AccountRepo.

    This implementation is intentionally simple:
    - `get` and `save` operate within a provided Session.
    - Transaction scoping is managed by infra/db/session.session_scope().
    """

    def __init__(self, *, session: Session) -> None:
        self._session = session

    def get(self, account_id: AccountId) -> Account | None:
        stmt = select(AccountModel).where(AccountModel.id == str(account_id))
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else to_entity(model)

    def save(self, account: Account) -> None:
        """
        Upsert semantics for the demo.

        If the row exists, update the balance.
        If it does not, insert it.
        """
        existing = self._session.get(AccountModel, str(account.id))
        if existing is None:
            self._session.add(to_model(account))
            return

        existing.balance_pence = account.balance.pence
