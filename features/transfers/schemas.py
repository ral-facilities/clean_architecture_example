# features/transfers/schemas.py
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateTransferRequest(BaseModel):
    """
    HTTP request schema for creating a transfer.
    """
    from_account_id: str
    to_account_id: str
    amount_pence: int = Field(ge=1)


class TransferResponse(BaseModel):
    """
    HTTP response schema for returning a transfer result.
    """
    id: str
    from_account_id: str
    to_account_id: str
    amount_pence: int
    created_at: datetime
    from_balance_pence: int
    to_balance_pence: int
