# root/router.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from features.accounts.routers import build_router as build_accounts_router
from features.transfers.routers import build_router as build_transfers_router
from infra.db.session import get_session
from root.di.accounts import build_accounts_deps
from root.di.container import Container
from root.di.transfers import build_transfers_deps


def register_routers(app: FastAPI, *, container: Container) -> None:
    """
    Register feature routers.

    Notes:
    - Feature router modules remain pure: they accept In ports.
    - Root wires In ports per request (Session) and passes them in.
    - Logger is process-wide and comes from Container.
    """
    app.include_router(_build_accounts_router(container))
    app.include_router(_build_transfers_router(container))


def _build_accounts_router(container: Container):
    """
    Build the accounts router with request-scoped wiring.
    """

    def _get_accounts_deps(session: Annotated[Session, Depends(get_session)]):
        return build_accounts_deps(session=session, logger=container.logger)

    def _get_account_creator(deps=Depends(_get_accounts_deps)):
        return deps.account_creator

    def _get_account_getter(deps=Depends(_get_accounts_deps)):
        return deps.account_getter

    router = build_accounts_router(
        account_creator=Depends(_get_account_creator),
        account_getter=Depends(_get_account_getter),
    )
    return router


def _build_transfers_router(container: Container):
    """
    Build the transfers router with request-scoped wiring.
    """

    def _get_transfers_deps(session: Annotated[Session, Depends(get_session)]):
        return build_transfers_deps(session=session, logger=container.logger)

    def _get_transfer_creator(deps=Depends(_get_transfers_deps)):
        return deps.transfer_creator

    router = build_transfers_router(
        transfer_creator=Depends(_get_transfer_creator),
    )
    return router
