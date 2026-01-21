# features/transfers/presenters.py
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
