
from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from infra.db.accounts.repo import AccountRepo
from features.accounts.presenters import AccountCreatorPresenter, AccountGetterPresenter
from features.accounts.services import AccountCreator, AccountGetter
from root.di._shared import ContextDep


def get_account_repo(ctx: ContextDep) -> AccountRepo:
    return AccountRepo(session=ctx.session)

AccountRepoDep = Annotated[AccountRepo, Depends(get_account_repo)]


def get_account_creator(
    repo: AccountRepoDep,
    ctx: ContextDep,
) -> AccountCreator:
    return AccountCreator(
        repo=repo,
        presenter=AccountCreatorPresenter(),
        logger=ctx.logger,
    )


def get_account_getter(
    repo: AccountRepoDep,
    ctx: ContextDep,
) -> AccountGetter:
    return AccountGetter(
        repo=repo,
        presenter=AccountGetterPresenter(),
        logger=ctx.logger,
    )
