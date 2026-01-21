from __future__ import annotations

from dataclasses import dataclass

from core.values.objects import Money
from core.values.types import AccountId


@dataclass(slots=True)
class Account:
    """
    Pure state entity.

    Invariants:
    - balance is never negative (enforced by Money)
    """

    id: AccountId
    balance: Money
