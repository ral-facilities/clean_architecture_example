# features/transfers/services.py
from __future__ import annotations

import logging

from core.entities.transfer import Transfer
from core.services.transfer import apply_transfer
from core.utils.id import new_id
from core.utils.time import utc_now
from core.values.errors import (
    InsufficientFundsError as DomainInsufficientFundsError,
    InvalidAmountError as DomainInvalidAmountError,
    SameAccountTransferError as DomainSameAccountTransferError,
)
from core.values.objects import Money
from core.values.types import AccountId, TransferId
from features.accounts.ports import AccountRepoPort
from features.transfers.errors import (
    TransferAccountNotFoundError,
    TransferInsufficientFundsError,
    TransferValidationError,
)
from features.transfers.ports import TransferCreatorPort, TransferRepoPort


class TransferCreator(TransferCreatorPort.In):
    """
    Use case service for creating a transfer.

    Implements TransferCreatorPort.In and coordinates:
    - repository access (two accounts + transfer)
    - domain validation (via Transfer/Money invariants and domain services)
    - persistence (saving updated accounts + transfer fact)
    - presentation via TransferCreatorPort.Out
    """

    def __init__(
        self,
        *,
        account_repo: AccountRepoPort,
        transfer_repo: TransferRepoPort,
        presenter: TransferCreatorPort.Out,
        logger: logging.Logger,
    ) -> None:
        self._account_repo = account_repo
        self._transfer_repo = transfer_repo
        self._presenter = presenter
        self._logger = logger

    def execute(
        self,
        *,
        from_account_id: str,
        to_account_id: str,
        amount_pence: int,
    ) -> "TransferResponse":
        self._logger.info(
            "transfer_create_started from_account_id=%s to_account_id=%s amount_pence=%s",
            from_account_id,
            to_account_id,
            amount_pence,
        )

        # Load accounts.
        from_account = self._account_repo.get(AccountId(from_account_id))
        if from_account is None:
            self._logger.info(
                "transfer_create_failed_missing_account account_id=%s role=from",
                from_account_id,
            )
            raise TransferAccountNotFoundError(f"Account not found: {from_account_id}")

        to_account = self._account_repo.get(AccountId(to_account_id))
        if to_account is None:
            self._logger.info(
                "transfer_create_failed_missing_account account_id=%s role=to",
                to_account_id,
            )
            raise TransferAccountNotFoundError(f"Account not found: {to_account_id}")

        # Create the Transfer entity (validates IDs and amount).
        try:
            transfer = Transfer(
                id=TransferId(new_id()),
                from_account_id=from_account.id,
                to_account_id=to_account.id,
                amount=Money(amount_pence),
                created_at=utc_now(),
            )
        except (DomainInvalidAmountError, DomainSameAccountTransferError) as exc:
            self._logger.info(
                "transfer_create_failed_validation from_account_id=%s to_account_id=%s amount_pence=%s error=%s",
                from_account_id,
                to_account_id,
                amount_pence,
                str(exc),
            )
            # Translate domain validation errors into application-level errors.
            raise TransferValidationError(str(exc)) from exc

        # Apply the transfer to the accounts (domain service).
        try:
            applied = apply_transfer(
                from_account=from_account,
                to_account=to_account,
                transfer=transfer,
            )
        except DomainInsufficientFundsError as exc:
            self._logger.info(
                "transfer_create_failed_insufficient_funds from_account_id=%s amount_pence=%s error=%s",
                from_account_id,
                amount_pence,
                str(exc),
            )
            raise TransferInsufficientFundsError(str(exc)) from exc

        # Persist updated account states.
        self._account_repo.save(applied.updated_from_account)
        self._account_repo.save(applied.updated_to_account)

        # Persist the transfer fact.
        self._transfer_repo.save(applied.transfer)

        self._logger.info(
            "transfer_create_succeeded transfer_id=%s from_account_id=%s to_account_id=%s amount_pence=%s from_balance_pence=%s to_balance_pence=%s",
            str(applied.transfer.id),
            str(applied.transfer.from_account_id),
            str(applied.transfer.to_account_id),
            applied.transfer.amount.pence,
            applied.updated_from_account.balance.pence,
            applied.updated_to_account.balance.pence,
        )

        # Delegate formatting to the presenter.
        return self._presenter.present(applied)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import only for typing; avoids runtime coupling / import cycles.
    from features.transfers.schemas import TransferResponse
