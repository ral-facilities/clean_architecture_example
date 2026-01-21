# features/accounts/services.py
from __future__ import annotations

import logging

from core.entities.account import Account
from core.utils.id import new_id
from core.values.errors import InvalidAmountError as DomainInvalidAmountError
from core.values.objects import Money
from core.values.types import AccountId
from features.accounts.errors import AccountNotFoundError, AccountValidationError
from features.accounts.ports import (
    AccountCreatorPort,
    AccountGetterPort,
    AccountRepoPort,
)


class AccountGetter(AccountGetterPort.In):
    """
    Use case interactor for fetching an account.

    Implements AccountGetter.In and coordinates:
    - repository access
    - error handling
    - presentation via AccountGetter.Out
    """

    def __init__(
        self,
        *,
        repo: AccountRepoPort,
        presenter: AccountGetterPort.Out,
        logger: logging.Logger,
    ) -> None:
        self._repo = repo
        self._presenter = presenter
        self._logger = logger

    def execute(self, *, account_id: str) -> "AccountResponse":
        self._logger.info("account_get_started account_id=%s", account_id)

        account = self._repo.get(AccountId(account_id))
        if account is None:
            self._logger.info("account_get_not_found account_id=%s", account_id)
            raise AccountNotFoundError(f"Account not found: {account_id}")

        self._logger.info(
            "account_get_succeeded account_id=%s balance_pence=%s",
            str(account.id),
            account.balance.pence,
        )

        # Delegate formatting to the presenter.
        return self._presenter.present(account)


class AccountCreator(AccountCreatorPort.In):
    """
    Use case interactor for creating an account.

    Implements AccountCreator.In and coordinates:
    - ID generation
    - domain validation
    - persistence
    - presentation via AccountCreator.Out
    """

    def __init__(
        self,
        *,
        repo: AccountRepoPort,
        presenter: AccountCreatorPort.Out,
        logger: logging.Logger,
    ) -> None:
        self._repo = repo
        self._presenter = presenter
        self._logger = logger

    def execute(self, *, initial_balance_pence: int | None) -> "AccountResponse":
        initial = initial_balance_pence if initial_balance_pence is not None else 0
        self._logger.info("account_create_started initial_balance_pence=%s", initial)

        try:
            account = Account(
                id=AccountId(new_id()),
                balance=Money(initial),
            )
        except DomainInvalidAmountError as exc:
            self._logger.info(
                "account_create_failed_validation initial_balance_pence=%s error=%s",
                initial,
                str(exc),
            )
            # Translate domain errors into application-level errors.
            raise AccountValidationError(str(exc)) from exc

        self._repo.save(account)

        self._logger.info(
            "account_create_succeeded account_id=%s balance_pence=%s",
            str(account.id),
            account.balance.pence,
        )

        # Delegate formatting to the presenter.
        return self._presenter.present(account)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import only for typing; avoids runtime coupling / import cycles.
    from features.accounts.schemas import AccountResponse
