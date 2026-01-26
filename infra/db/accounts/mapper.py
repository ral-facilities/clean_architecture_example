"""
Ring: Infrastructure (Database / ORM Adapters)

Responsibility:
Defines mapping functions between ORM persistence models and domain entities.
This module adapts raw database representations into domain objects and converts
domain objects back into database-ready models.

Design intent:
This is a classic data mapper.
It keeps the domain completely free of ORM concerns while allowing infrastructure
to translate between storage format and business objects.
All structural impedance between SQLAlchemy models and domain entities is isolated here.

This module contains:
- to_entity: conversion from AccountModel (ORM) to Account (domain entity).
- to_model: conversion from Account (domain entity) to AccountModel (ORM).

Dependency constraints:
- Must not import from the application layer (features/*).
- May depend on the Domain layer (core/).
- May depend on infrastructure models and tooling (SQLAlchemy).

Stability:
- Volatile.
- Changes when either the domain entity shape or the database schema changes.

Usage:
- Used by infrastructure repositories when loading from or saving to the database.
- Never imported by domain or application code.
- Acts as the translation boundary between persistence and business meaning.
"""

from __future__ import annotations

from core.entities.account import Account
from core.values.custom_types import AccountId
from core.values.objects import Money
from infra.db.accounts.model import AccountModel


def to_entity(model: AccountModel) -> Account:
    """
    Convert an AccountModel ORM row into a domain Account entity.
    """
    return Account(
        id=AccountId(model.id),
        balance=Money(model.balance_pence),
    )


def to_model(entity: Account) -> AccountModel:
    """
    Convert a domain Account entity into an AccountModel ORM row.
    """
    return AccountModel(
        id=str(entity.id),
        balance_pence=entity.balance.pence,
    )
