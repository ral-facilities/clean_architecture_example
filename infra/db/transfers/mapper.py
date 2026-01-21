# infra/db/transfers/mapper.py
from __future__ import annotations

from core.entities.transfer import Transfer
from core.values.objects import Money
from core.values.types import AccountId, TransferId

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
