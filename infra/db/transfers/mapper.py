"""
Ring: Infrastructure (Database / ORM Adapters)

Responsibility:
Defines mapping functions between ORM persistence models and domain entities for
Transfers. This module adapts raw database rows into domain Transfer entities and
converts domain Transfer entities back into ORM models.

Design intent:
This is a classic data mapper.
It isolates all impedance between SQLAlchemy models and domain entities so that
the domain remains completely free of ORM concerns and persistence structure.

This module contains:
- to_entity: conversion from TransferModel (ORM) to Transfer (domain entity).
- to_model: conversion from Transfer (domain entity) to TransferModel (ORM).

Dependency constraints:
- Must not import from the application layer (features/*).
- May depend on the Domain layer (core/).
- May depend on infrastructure models and tooling (SQLAlchemy).

Stability:
- Volatile.
- Changes when either the domain entity shape or the database schema changes.

Usage:
- Used by infrastructure repositories when saving transfer facts to the database.
- Never imported by domain or application code.
- Acts as the translation boundary between persistence and business meaning.
"""

from __future__ import annotations

from core.entities.transfer import Transfer
from core.values.custom_types import AccountId, TransferId
from core.values.objects import Money
from infra.db.transfers.model import TransferModel


def to_entity(model: TransferModel) -> Transfer:
    """
    Convert a TransferModel ORM row into a domain Transfer entity.
    """
    return Transfer(
        id=TransferId(model.id),
        from_account_id=AccountId(model.from_account_id),
        to_account_id=AccountId(model.to_account_id),
        amount=Money(model.amount_pence),
        created_at=model.created_at,
    )


def to_model(entity: Transfer) -> TransferModel:
    """
    Convert a domain Transfer entity into a TransferModel ORM row.
    """
    return TransferModel(
        id=str(entity.id),
        from_account_id=str(entity.from_account_id),
        to_account_id=str(entity.to_account_id),
        amount_pence=entity.amount.pence,
        created_at=entity.created_at,
    )
