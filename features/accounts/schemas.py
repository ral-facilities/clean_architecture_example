from __future__ import annotations

from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    """
    HTTP request schema for creating an account.
    """
    initial_balance_pence: int | None = Field(default=None, ge=0)


class AccountResponse(BaseModel):
    """
    HTTP response schema for returning an account.
    """
    id: str
    balance_pence: int
