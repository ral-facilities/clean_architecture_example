from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from core.values.errors import InvalidAmountError, SameAccountTransferError
from core.values.objects import Money
from core.values.types import AccountId, TransferId


@dataclass(frozen=True, slots=True)
class Transfer:
    """
    Pure fact entity.

    Invariants:
    - source and destination accounts differ
    - amount is positive
    """

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
