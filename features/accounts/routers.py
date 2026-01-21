# features/accounts/routers.py
from __future__ import annotations

from fastapi import APIRouter

from features.accounts.ports import AccountCreatorPort, AccountGetterPort
from features.accounts.schemas import AccountResponse, CreateAccountRequest, GetAccountRequest


def build_account_routers(
    *,
    account_creator: AccountCreatorPort.In,
    account_getter: AccountGetterPort.In,
) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post("", response_model=AccountResponse)
    def create_account_endpoint(req: CreateAccountRequest) -> AccountResponse:
        return account_creator.execute(initial_balance_pence=req.initial_balance_pence)

    @router.get("/{account_id}", response_model=AccountResponse)
    def get_account_endpoint(req: GetAccountRequest) -> AccountResponse:
        return account_getter.execute(account_id=req.account_id)

    return router
