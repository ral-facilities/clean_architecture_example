"""
Ring: Domain (Enterprise Business Rules)

Responsibility:
Defines the Transfer domain entity as an immutable business fact.
A Transfer represents value movement between two distinct accounts at a point in time.

Dependency constraints:
- Must only depend on core modules and standard library types.
- Must never import from features/, infra/, or root/.
- Must not reference persistence, HTTP, or serialization concerns.

Stability:
- Stable business policy. Changes here change what a Transfer *means*.

Usage:
- Created by application use cases when a transfer is authorised/recorded.
- Persisted by infrastructure as domain data (infrastructure adapts to this shape).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from core.values.errors import InvalidAmountError, SameAccountTransferError
from core.values.objects import Money
from core.values.types import AccountId, TransferId


@dataclass(frozen=True, slots=True)
class Transfer:
    id: TransferId
    from_account_id: AccountId
    to_account_id: AccountId
    amount: Money
    created_at: datetime

    def __post_init__(self) -> None:
        if self.from_account_id == self.to_account_id:
            raise SameAccountTransferError("Source and destination accounts must differ")

        if not self.amount.is_positive():
            raise InvalidAmountError("Transfer amount must be positive")
