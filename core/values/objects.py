"""
Domain value objects.

These are objects that have:
- no identity
- no lifecycle
- no persistence of their own
- equality defined purely by their value

They differ from entities in that entities are tracked by identity
(AccountId, TransferId) and represent things that exist over time.

A value object represents a fact, a measurement, or a result.

For example:
- Money is not an entity because £10 is not a “thing” in the system.
  There is no MoneyId, no Money repository, no lifecycle.
  £10 is simply a value. Any £10 is interchangeable with any other £10.
- AppliedTransfer is not an entity because it does not represent a persistent
  business object. It represents the outcome of a domain operation.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from core.values.constants import MIN_TRANSFER_AMOUNT_PENCE
from core.values.errors import InvalidAmountError

if TYPE_CHECKING:
    from core.entities.account import Account
    from core.entities.transfer import Transfer


@dataclass(frozen=True, slots=True)
class Money:
    """
    Domain value object representing money in minor units (pence).
    """

    pence: int

    def __post_init__(self) -> None:
        if self.pence < 0:
            raise InvalidAmountError("Money cannot be negative")

    def is_positive(self) -> bool:
        return self.pence >= MIN_TRANSFER_AMOUNT_PENCE


@dataclass(frozen=True, slots=True)
class AppliedTransfer:
    """
    Domain value object representing the result of applying a transfer.
    """

    updated_from_account: "Account"
    updated_to_account: "Account"
    transfer: "Transfer"
