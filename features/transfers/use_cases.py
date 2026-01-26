"""
Ring: Application (Use Case / Interactors)

Responsibility:
Implements the transfer creation use case.
This interactor coordinates loading required accounts, constructing a transfer
fact, applying the transfer via domain services, persisting resulting state, and
presenting the result.

Design intent:
The interactor owns orchestration and application policy:
- It coordinates multiple repositories and domain operations.
- It translates domain errors into transfer-specific application errors.
- It delegates formatting to a presenter and persistence to repositories.

This module contains:
- TransferCreator: the interactor implementing TransferCreatorPort.In.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Less stable than the domain, more stable than infrastructure.
- Changes when transfer behaviour changes, not when implementation details change.

Usage:
- Invoked by delivery mechanisms (e.g. HTTP controllers).
- Loads data via repository ports, applies domain rules, persists results, and
  delegates output formatting to the presenter.
"""

from __future__ import annotations

import logging

from core.entities.account import Account
from core.entities.transfer import Transfer
from core.services.transfer import apply_transfer
from core.utils.id import new_id
from core.utils.time import utc_now
from core.values.custom_types import AccountId, TransferId
from core.values.errors import InsufficientFundsError as DomainInsufficientFundsError
from core.values.errors import InvalidAmountError as DomainInvalidAmountError
from core.values.errors import (
    SameAccountTransferError as DomainSameAccountTransferError,
)
from core.values.objects import AppliedTransfer, Money
from features.accounts.ports import AccountRepoPort
from features.transfers.errors import (
    TransferAccountNotFoundError,
    TransferInsufficientFundsError,
    TransferValidationError,
)
from features.transfers.ports import TransferCreatorPort, TransferRepoPort
from features.transfers.schemas import TransferResponse


class TransferCreator(TransferCreatorPort.In):
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
    ) -> TransferResponse:
        self._logger.info(
            "transfer_create_started from_account_id=%s to_account_id=%s amount_pence=%s",
            from_account_id,
            to_account_id,
            amount_pence,
        )

        from_account, to_account = self._load_accounts(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
        )

        new_transfer = self._create_transfer(
            from_account=from_account,
            to_account=to_account,
            amount_pence=amount_pence,
        )

        applied_transfer = self._apply_transfer(
            from_account=from_account,
            to_account=to_account,
            transfer=new_transfer,
        )

        self._persist(applied_transfer)

        self._log_succeeded(applied_transfer)

        return self._presenter.present(applied_transfer)

    def _load_accounts(
        self,
        *,
        from_account_id: str,
        to_account_id: str,
    ) -> tuple[Account, Account]:
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

        return from_account, to_account

    def _create_transfer(
        self,
        *,
        from_account: Account,
        to_account: Account,
        amount_pence: int,
    ) -> Transfer:
        try:
            return Transfer(
                id=TransferId(new_id()),
                from_account_id=from_account.id,
                to_account_id=to_account.id,
                amount=Money(amount_pence),
                created_at=utc_now(),
            )
        except (DomainInvalidAmountError, DomainSameAccountTransferError) as exc:
            self._logger.info(
                "transfer_create_failed_validation from_account_id=%s to_account_id=%s amount_pence=%s error=%s",
                str(from_account.id),
                str(to_account.id),
                amount_pence,
                str(exc),
            )
            raise TransferValidationError(str(exc)) from exc

    def _apply_transfer(
        self,
        *,
        from_account: Account,
        to_account: Account,
        transfer: Transfer,
    ) -> AppliedTransfer:
        try:
            return apply_transfer(
                from_account=from_account,
                to_account=to_account,
                transfer=transfer,
            )
        except DomainInsufficientFundsError as exc:
            self._logger.info(
                "transfer_create_failed_insufficient_funds from_account_id=%s amount_pence=%s error=%s",
                str(from_account.id),
                transfer.amount.pence,
                str(exc),
            )
            raise TransferInsufficientFundsError(str(exc)) from exc

    def _persist(self, applied: AppliedTransfer) -> None:
        self._account_repo.save(applied.updated_from_account)
        self._account_repo.save(applied.updated_to_account)
        self._transfer_repo.save(applied.transfer)

    def _log_succeeded(self, applied: AppliedTransfer) -> None:
        self._logger.info(
            "transfer_create_succeeded transfer_id=%s from_account_id=%s to_account_id=%s amount_pence=%s from_balance_pence=%s to_balance_pence=%s",
            str(applied.transfer.id),
            str(applied.transfer.from_account_id),
            str(applied.transfer.to_account_id),
            applied.transfer.amount.pence,
            applied.updated_from_account.balance.pence,
            applied.updated_to_account.balance.pence,
        )
