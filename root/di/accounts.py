# root/di/accounts.py
from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy.orm import Session

from features.accounts.presenters import AccountCreatorPresenter, AccountGetterPresenter
from features.accounts.ports import AccountCreatorPort, AccountGetterPort
from features.accounts.services import AccountCreator, AccountGetter

from infra.db.accounts.repo import AccountRepo


@dataclass(frozen=True, slots=True)
class AccountsDeps:
    """
    Wired dependencies for the accounts feature.
    """

    account_creator: AccountCreatorPort.In
    account_getter: AccountGetterPort.In


def build_accounts_deps(*, session: Session, logger: logging.Logger) -> AccountsDeps:
    """
    Build the accounts dependency graph for a given request-scoped Session.
    """
    repo = AccountRepo(session=session)

    getter_presenter = AccountGetterPresenter()
    creator_presenter = AccountCreatorPresenter()

    account_getter = AccountGetter(repo=repo, presenter=getter_presenter, logger=logger)
    account_creator = AccountCreator(
        repo=repo,
        presenter=creator_presenter,
        logger=logger,
    )

    return AccountsDeps(
        account_creator=account_creator,
        account_getter=account_getter,
    )
