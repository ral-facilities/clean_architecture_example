"""
Ring: Composition Root

Responsibility:
Defines dependency wiring for the Transfers feature.
This module constructs concrete implementations of repositories, presenters, and
use case interactors and exposes them as injectable dependencies.

Design intent:
This is pure object graph composition.
It connects:
- Infrastructure implementations (TransferRepo),
- Interface adapters (TransferCreatorPresenter),
- Application interactors (TransferCreator),
- Shared runtime context (session, logger),
into a fully assembled use case.

No business logic or application policy lives here.
Only construction and wiring of already-defined components.

This module contains:
- get_transfer_repo: builds the concrete TransferRepo using the current DB session.
- get_transfer_creator: builds the TransferCreator interactor with all its dependencies.

Dependency constraints:
- May depend on all inner layers (infra, features, core).
- Must not be imported by any inner layer.
- Must not contain business rules or use case logic.

Stability:
- Highly volatile.
- Changes whenever wiring, construction strategy, or infrastructure changes.

Usage:
- Used by delivery layers (routers) through FastAPI dependency injection.
- Acts as the assembly point for the Transfers feature object graph.
- Ensures that interactors are always created with fully satisfied dependencies.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from infra.db.transfers.repo import TransferRepo
from features.transfers.presenters import TransferCreatorPresenter
from features.transfers.use_cases import TransferCreator
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
