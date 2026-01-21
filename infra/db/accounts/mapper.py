from __future__ import annotations

from core.entities.account import Account
from core.values.objects import Money
from core.values.types import AccountId

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
