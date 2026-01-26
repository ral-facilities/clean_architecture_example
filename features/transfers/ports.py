"""
Ring: Application (Use Case Boundaries / Ports)

Responsibility:
Defines the port interfaces for the Transfers feature.
These ports form the stable contracts that isolate transfer use case logic from
outer details such as persistence and presentation formatting.

Design intent:
- Primary ports (In/Out) define the use case boundary: what the application offers
  and what output it emits.
- Secondary ports (repositories) define what the use case needs from external
  systems, without importing those systems.
- Dependencies point inwards: interactors implement In, presenters implement Out,
  infrastructure implements repository ports.

This module contains:
- TransferCreatorPort: primary In/Out ports for creating a transfer.
- TransferRepoPort: secondary persistence port for saving transfer facts.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Highly stable.
- Ports are the contracts that outer layers adapt to; they should change rarely.

Usage:
- Implemented by transfer interactors (In) and presenters (Out).
- Implemented by infrastructure adapters for persistence ports.
- Imported by delivery and infrastructure to wire concrete implementations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from core.values.objects import AppliedTransfer
from features._shared.ports import IOPorts


class TransferCreatorPort(IOPorts):
    """
    Use case: create and apply a transfer between two existing accounts.
    """

    class In(Protocol):
        """
        Input boundary for creating a transfer.
        The service implements this.
        """

        def execute(
            self,
            *,
            from_account_id: str,
            to_account_id: str,
            amount_pence: int,
        ) -> "TransferResponse":
            raise NotImplementedError

    class Out(Protocol):
        """
        Output boundary for presenting a transfer result.
        The presenter implements this.
        """

        def present(self, applied: AppliedTransfer) -> "TransferResponse":
            raise NotImplementedError


class TransferRepoPort(Protocol):
    """
    Persistence port for transfers (facts).
    Implemented by infrastructure adapters.
    """

    def save(self, transfer: "Transfer") -> None:
        raise NotImplementedError


if TYPE_CHECKING:
    # Import only for typing; avoids runtime coupling / import cycles.
    from core.entities.transfer import Transfer
    from features.transfers.schemas import TransferResponse
