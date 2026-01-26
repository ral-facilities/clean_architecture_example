"""
Ring: Application (Use Case / Interactors)

Responsibility:
Implements the account-related use cases of the system.
These interactors coordinate domain objects, repositories, presenters, and logging
to realise application behaviour such as fetching and creating accounts.

They define:
- How the domain is used to fulfil a request.
- The orchestration of domain logic, persistence, and presentation.
- The translation of domain errors into application-level errors.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly.
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Less stable than the domain, more stable than infrastructure.
- Changes when application behaviour changes, not when technical details change.

Usage:
- Invoked by delivery mechanisms (e.g. HTTP controllers, CLI, jobs).
- Calls domain entities and services to perform business work.
- Delegates data access to repositories and formatting to presenters.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.entities.account import Account
from core.utils.id import new_id
from core.values.errors import InvalidAmountError as DomainInvalidAmountError
from core.values.objects import Money
from core.values.types import AccountId
from features.accounts.errors import AccountNotFoundError, AccountValidationError
from features.accounts.ports import AccountCreatorPort, AccountGetterPort, AccountRepoPort

if TYPE_CHECKING:
    from features.accounts.schemas import AccountResponse


class AccountGetter(AccountGetterPort.In):
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

    def execute(self, *, account_id: str) -> AccountResponse:
        self._logger.info("account_get_started account_id=%s", account_id)

        account = self._load_account_or_raise(account_id=account_id)

        self._log_succeeded(account)

        return self._presenter.present(account)

    def _load_account_or_raise(self, *, account_id: str) -> Account:
        account = self._repo.get(AccountId(account_id))
        if account is None:
            self._logger.info("account_get_not_found account_id=%s", account_id)
            raise AccountNotFoundError(f"Account not found: {account_id}")

        return account

    def _log_succeeded(self, account: Account) -> None:
        self._logger.info(
            "account_get_succeeded account_id=%s balance_pence=%s",
            str(account.id),
            account.balance.pence,
        )


class AccountCreator(AccountCreatorPort.In):
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

    def execute(self, *, initial_balance_pence: int | None) -> AccountResponse:
        initial = initial_balance_pence if (initial_balance_pence is not None) else 0
        self._logger.info("account_create_started initial_balance_pence=%s", initial_balance_pence)

        account = self._create_domain_account_or_raise(initial_balance_pence=initial)

        self._repo.save(account)

        self._log_succeeded(account)

        return self._presenter.present(account)

    def _create_domain_account_or_raise(self, *, initial_balance_pence: int) -> Account:
        try:
            return Account(
                id=AccountId(new_id()),
                balance=Money(initial_balance_pence),
            )
        except DomainInvalidAmountError as exc:
            self._logger.info(
                "account_create_failed_validation initial_balance_pence=%s error=%s",
                initial_balance_pence,
                str(exc),
            )
            raise AccountValidationError(str(exc)) from exc

    def _log_succeeded(self, account: Account) -> None:
        self._logger.info(
            "account_create_succeeded account_id=%s balance_pence=%s",
            str(account.id),
            account.balance.pence,
        )
