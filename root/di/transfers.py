# root/di/transfers.py
from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy.orm import Session

from features.transfers.presenters import TransferCreatorPresenter
from features.transfers.ports import TransferCreatorPort
from features.transfers.services import TransferCreator

from infra.db.accounts.repo import AccountRepo
from infra.db.transfers.repo import TransferRepo


@dataclass(frozen=True, slots=True)
class TransfersDeps:
    """
    Wired dependencies for the transfers feature.
    """

    transfer_creator: TransferCreatorPort.In


def build_transfers_deps(*, session: Session, logger: logging.Logger) -> TransfersDeps:
    """
    Build the transfers dependency graph for a given request-scoped Session.
    """
    account_repo = AccountRepo(session=session)
    transfer_repo = TransferRepo(session=session)

    presenter = TransferCreatorPresenter()

    transfer_creator = TransferCreator(
        account_repo=account_repo,
        transfer_repo=transfer_repo,
        presenter=presenter,
        logger=logger,
    )

    return TransfersDeps(transfer_creator=transfer_creator)
