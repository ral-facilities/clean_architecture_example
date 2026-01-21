"""
END-TO-END FLOW (transfers/post) with "In returns TransferResponse" and
"Out.present returns TransferResponse".

Primary ports (In/Out) are use-case boundaries.
Secondary ports (Repo, IdGenerator, Clock) are driven by the use case.
"""
from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

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
