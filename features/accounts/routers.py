"""
Ring: Delivery (Controllers, Frameworks & Drivers / HTTP)

Responsibility:
Defines the HTTP routing layer for the Accounts feature.
This module binds FastAPI endpoints to application use cases and adapts HTTP
requests and responses to and from the application layer.

Design intent:
This file is pure delivery mechanism. It contains no business logic and no
application policy. Its only role is to translate protocol-level concepts
(HTTP routes, request bodies, dependency injection) into calls to use cases.

This module contains:
- FastAPI route definitions for account creation and retrieval.
- Dependency wiring between HTTP endpoints and application interactors.

Dependency constraints:
- Must not import from any other feature!
- Must not contain domain or application business rules.
- Must not perform persistence or infrastructure work directly.
- May depend on the Application layer (use cases, ports, schemas).
- May depend on shared application contracts in features/_shared.
- May depend on framework code (FastAPI, dependency injection).

Stability:
- Highly volatile.
- Changes when the API surface, routing, or framework configuration changes.

Usage:
- Loaded by the application root to register HTTP endpoints.
- Acts as the outermost adapter between the web framework and the use case layer.
- Never called directly by domain or application code.
"""
 
from typing import Annotated

from fastapi import APIRouter, Depends

from features._shared.types import Provider
from features.accounts.use_cases import AccountCreator, AccountGetter
from features.accounts.schemas import AccountResponse, CreateAccountRequest

def build_account_routers(
    *,
    account_creator: Provider[AccountCreator],
    account_getter: Provider[AccountGetter],
) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post("", response_model=AccountResponse)
    def create_account_endpoint(
        req: CreateAccountRequest,
        creator: Annotated[AccountCreator, Depends(account_creator)],
    ) -> AccountResponse:
        return creator.execute(initial_balance_pence=req.initial_balance_pence)

    @router.get("/{account_id}", response_model=AccountResponse)
    def get_account_endpoint(
        account_id: str,
        getter: Annotated[AccountGetter, Depends(account_getter)],
    ) -> AccountResponse:
        return getter.execute(account_id=account_id)

    return router
