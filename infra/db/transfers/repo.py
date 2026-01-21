# infra/db/transfers/repo.py
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
