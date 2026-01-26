"""
Ring: Composition Root

Responsibility:
Defines dependency wiring for the Accounts feature.
This module constructs concrete implementations of repositories, presenters, and
use case interactors and exposes them as injectable dependencies.

Design intent:
This is pure object graph composition.
It connects:
- Infrastructure implementations (AccountRepo),
- Interface adapters (AccountCreatorPresenter, AccountGetterPresenter),
- Application interactors (AccountCreator, AccountGetter),
- Shared runtime context (session, logger),
into fully assembled use cases.

No business logic or application policy lives here.
Only construction and wiring of already-defined components.

This module contains:
- get_account_repo: builds the concrete AccountRepo using the current DB session.
- get_account_creator: builds the AccountCreator interactor with all its dependencies.
- get_account_getter: builds the AccountGetter interactor with all its dependencies.

Dependency constraints:
- May depend on all inner layers (infra, features, core).
- Must not be imported by any inner layer.
- Must not contain business rules or use case logic.

Stability:
- Highly volatile.
- Changes whenever wiring, construction strategy, or infrastructure changes.

Usage:
- Used by delivery layers (routers) through FastAPI dependency injection.
- Acts as the assembly point for the Accounts feature object graph.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from features.accounts.presenters import AccountCreatorPresenter, AccountGetterPresenter
from features.accounts.use_cases import AccountCreator, AccountGetter
from infra.db.accounts.repo import AccountRepo
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
