from typing import Annotated

from fastapi import APIRouter, Depends

from features._shared.types import Provider
from features.accounts.services import AccountCreator, AccountGetter
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
