"""
Ring: Delivery (Interface Adapters / HTTP Boundary)

Responsibility:
Defines the HTTP-facing schemas for the Accounts feature.
These classes describe how data enters and leaves the system through the API.

Design intent:
These models represent the external contract of the application.
They separate protocol-level validation and formatting from domain and application logic.

This module contains:
- Request schemas for creating and fetching accounts.
- Response schemas for returning account data to clients.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/) only for type meaning.
- May depend on shared application contracts in features/_shared.

Stability:
- Less stable than the application and domain layers.
- Changes when the public API contract changes.

Usage:
- Used by HTTP controllers to validate incoming requests.
- Used to serialise responses returned to clients.
- Converted to and from application-level data structures by use cases.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    """
    HTTP request schema for creating an account.
    """

    initial_balance_pence: int | None = Field(default=None, ge=0)


class GetAccountRequest(BaseModel):
    """
    HTTP request schema for fetching an account.
    """

    account_id: str


class AccountResponse(BaseModel):
    """
    HTTP response schema for returning an account.
    """

    id: str
    balance_pence: int
