"""
Ring: Delivery (Interface Adapters / HTTP Boundary)

Responsibility:
Defines the HTTP-facing schemas for the Transfers feature.
These models describe the external API contract for creating a transfer and for
returning the result.

Design intent:
These schemas represent the external contract of the system.
They provide protocol-level validation and a stable shape for request/response
payloads, without embedding business rules or persistence concerns.

This module contains:
- CreateTransferRequest: request DTO for creating a transfer.
- TransferResponse: response DTO describing the transfer and resulting balances.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Less stable than the application and domain layers.
- Changes when the public API contract changes.

Usage:
- Used by HTTP controllers to validate incoming transfer requests.
- Used to serialise transfer results returned to clients.
- Produced by presenters and returned by use cases.
"""
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
