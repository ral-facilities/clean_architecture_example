from __future__ import annotations
from pydantic import BaseModel, Field
from core.values.objects import AppliedTransfer


class CreateTransferInput(BaseModel):
    """
    A use-case input model for creating a transfer.
    """

    from_account_id: str
    to_account_id: str
    amount_pence: int = Field(ge=1)


CreateTransferOutput = AppliedTransfer
