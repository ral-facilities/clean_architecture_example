"""
Ring: Domain (Shared Kernel / Value Objects)

Responsibility:
Defines domain value objects: objects that are defined purely by their value and not
by identity, lifecycle, or persistence. They represent facts, measurements, or results
within the domain.

Design intent:
- Value objects have no identity and no independent existence over time.
- Equality is defined only by their contained values.
- They differ from entities, which are tracked by identity and represent things that
  persist and evolve in the system.

This module contains:
- Money: a measurement of monetary value in minor units.
- AppliedTransfer: the result of a domain operation, not a persistent business object.

Dependency constraints:
- Must only depend on other domain modules and the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).

Stability:
- Highly stable.
- Changes here redefine the meaning of fundamental domain values.

Usage:
- Used by domain entities and domain services to express business facts and results.
- Used by outer layers as immutable domain data without redefining their semantics.
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
