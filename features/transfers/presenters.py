"""
Ring: Interface Adapters (Presenters)

Responsibility:
Defines presenters for the Transfers feature.
Presenters adapt domain results into response DTOs suitable for external delivery.

Design intent:
Presenters isolate representation and formatting concerns from use cases.
Use cases produce domain results (e.g. AppliedTransfer); presenters decide how that
result is shaped for external consumption without leaking domain objects outward.

This module contains:
- TransferCreatorPresenter: mapping from AppliedTransfer to TransferResponse.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain domain or application business rules.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Moderately stable.
- Changes when response representations change, even if use case logic does not.

Usage:
- Called by the transfer use case interactor to produce output DTOs.
- Used by delivery layers as the final response shape.
- Acts as the boundary between use case policy and presentation format.
"""

from __future__ import annotations

from core.values.objects import AppliedTransfer
from features.transfers.ports import TransferCreatorPort
from features.transfers.schemas import TransferResponse


class TransferCreatorPresenter(TransferCreatorPort.Out):
    """
    Presenter for the transfer use case.

    Converts an AppliedTransfer (domain result) into a TransferResponse DTO.
    """

    def present(self, applied: AppliedTransfer) -> TransferResponse:
        return TransferResponse(
            id=str(applied.transfer.id),
            from_account_id=str(applied.transfer.from_account_id),
            to_account_id=str(applied.transfer.to_account_id),
            amount_pence=applied.transfer.amount.pence,
            created_at=applied.transfer.created_at,
            from_balance_pence=applied.updated_from_account.balance.pence,
            to_balance_pence=applied.updated_to_account.balance.pence,
        )
