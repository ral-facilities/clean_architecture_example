from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel
from features.transfers.use_cases.models import CreateTransferInput

CreateTransferRequest = CreateTransferInput

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
