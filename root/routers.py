from __future__ import annotations

from fastapi import Depends, FastAPI

from features.accounts.routers import build_account_routers
from features.transfers.routers import build_transfer_routers
from root.di.accounts import get_account_creator, get_account_getter
from root.di.transfers import get_transfer_creator


def register_routers(app: FastAPI) -> None:
    app.include_router(
        build_account_routers(
            account_creator=get_account_creator,
            account_getter=get_account_getter,
        )
    )

    app.include_router(
        build_transfer_routers(
            transfer_creator=get_transfer_creator,
        )
    )
