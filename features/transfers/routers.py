# features/transfers/routers.py
from typing import Annotated

from fastapi import APIRouter, Depends

from features._shared.types import Provider
from features.transfers.services import TransferCreator
from features.transfers.schemas import CreateTransferRequest, TransferResponse


def build_transfer_routers(
    *,
    transfer_creator: Provider[TransferCreator],
) -> APIRouter:
    router = APIRouter(prefix="/transfers", tags=["transfers"])

    @router.post("", response_model=TransferResponse)
    def create_transfer_endpoint(
        req: CreateTransferRequest,
        creator: Annotated[TransferCreator, Depends(transfer_creator)],
    ) -> TransferResponse:
        return creator.execute(
            from_account_id=req.from_account_id,
            to_account_id=req.to_account_id,
            amount_pence=req.amount_pence,
        )

    return router
