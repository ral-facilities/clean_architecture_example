# features/transfers/routers.py
from __future__ import annotations

from fastapi import APIRouter

from features.transfers.ports import TransferCreatorPort
from features.transfers.schemas import CreateTransferRequest, TransferResponse


def build_transfer_routers(*, transfer_creator: TransferCreatorPort.In) -> APIRouter:
    router = APIRouter(prefix="/transfers", tags=["transfers"])

    @router.post("", response_model=TransferResponse)
    def create_transfer_endpoint(req: CreateTransferRequest) -> TransferResponse:
        return transfer_creator.execute(
            from_account_id=req.from_account_id,
            to_account_id=req.to_account_id,
            amount_pence=req.amount_pence,
        )

    return router
