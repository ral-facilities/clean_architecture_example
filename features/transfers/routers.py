"""
Ring: Delivery (Controllers, Frameworks & Drivers / HTTP)

Responsibility:
Defines the HTTP routing layer for the Transfers feature.
This module binds FastAPI endpoints to the transfer use case and adapts HTTP
requests to application input parameters and application output to HTTP responses.

Design intent:
This file is delivery mechanism only. It contains no business logic and does not
perform persistence. It translates protocol-level concepts (routes, request bodies,
dependency injection) into calls to application use cases.

This module contains:
- FastAPI route definitions for creating transfers.
- Dependency wiring between HTTP endpoints and the TransferCreator interactor.

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
- Acts as the outermost adapter between FastAPI and the transfer use case.
- Never imported by domain or application policy code.
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from features._shared.types import Provider
from features.transfers.use_cases import TransferCreator
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
