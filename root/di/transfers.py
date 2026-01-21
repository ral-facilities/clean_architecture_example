# root/di/transfers.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from infra.db.transfers.repo import TransferRepo
from features.transfers.presenters import TransferCreatorPresenter
from features.transfers.services import TransferCreator
from root.di._shared import ContextDep
from root.di.accounts import AccountRepoDep


def get_transfer_repo(ctx: ContextDep) -> TransferRepo:
    return TransferRepo(session=ctx.session)

TransferRepoDep = Annotated[TransferRepo, Depends(get_transfer_repo)]


def get_transfer_creator(
    account_repo: AccountRepoDep,
    transfer_repo: TransferRepoDep,
    ctx: ContextDep,
) -> TransferCreator:
    return TransferCreator(
        account_repo=account_repo,
        transfer_repo=transfer_repo,
        presenter=TransferCreatorPresenter(),
        logger=ctx.logger,
    )
