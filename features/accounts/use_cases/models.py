# features/accounts/use_cases/models.py
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateAccountInput(BaseModel):
    """
    A use-case input model for creating an account.
    """

    initial_balance_pence: int | None = Field(default=None, ge=0)


class GetAccountInput(BaseModel):
    """
    A use-case input model for fetching an account.
    """

    account_id: str
