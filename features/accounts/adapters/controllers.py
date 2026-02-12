# features/accounts/adapters/controllers.py
"""
Ring: Delivery (Controllers, Frameworks & Drivers / HTTP)

Responsibility:
Defines the HTTP routing layer for the Accounts feature.
This module binds FastAPI endpoints to the account use cases and adapts HTTP
requests to application input parameters and application output to HTTP responses.

Design intent:
This file is delivery mechanism only. It contains no business logic and does not
perform persistence. It translates protocol-level concepts (routes, request bodies,
dependency injection) into calls to application use cases.

This module contains:
- FastAPI route definitions for creating and fetching accounts.
- Dependency wiring between HTTP endpoints and the account interactors.

Dependency constraints:
- Must not import from any other feature!
- Must not contain domain or application business rules.
- Must not perform persistence or infrastructure work directly.
- May depend on the Application layer (use cases, ports, schemas).
- May depend on shared application contracts in features/_shared.
- May depend on framework code (FastAPI, dependency injection).

Stability:
- Highly volatile.
- Changes when routing, API surface, or framework configuration changes.

Usage:
- Loaded by the application root to register HTTP endpoints.
- Acts as the outermost adapter between FastAPI and the accounts use case.
- Never imported by domain or application policy code.
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from features.accounts.adapters.presenters import (
    AccountCreatorPresenter,
    AccountGetterPresenter,
)
from features._shared.custom_types import Provider
from features.accounts.adapters.schemas import AccountResponse, CreateAccountRequest
from features.accounts.use_cases.models import CreateAccountInput, GetAccountInput
from features.accounts.use_cases.ports import AccountCreatorPort, AccountGetterPort


def build_account_routers(
    *,
    account_creator: Provider[AccountCreatorPort.In],
    account_creator_presenter: Provider[AccountCreatorPresenter],
    account_getter: Provider[AccountGetterPort.In],
    account_getter_presenter: Provider[AccountGetterPresenter],
) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post("", response_model=AccountResponse)
    def create_account_endpoint(
        request: CreateAccountRequest,
        creator: Annotated[AccountCreatorPort.In, Depends(account_creator)],
        presenter: Annotated[AccountCreatorPresenter, Depends(account_creator_presenter)],
    ) -> AccountResponse:
        creator.execute(
            account_input=CreateAccountInput(
                initial_balance_pence=request.initial_balance_pence,
            ),
            presenter=presenter,
        )
        return presenter.response

    @router.get("/{account_id}", response_model=AccountResponse)
    def get_account_endpoint(
        account_id: str,
        getter: Annotated[AccountGetterPort.In, Depends(account_getter)],
        presenter: Annotated[AccountGetterPresenter, Depends(account_getter_presenter)],
    ) -> AccountResponse:
        getter.execute(
            account_input=GetAccountInput(account_id=account_id),
            presenter=presenter,
        )
        return presenter.response

    return router
