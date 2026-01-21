# features/accounts/ports.py
"""
END-TO-END FLOW (accounts/get) with "In returns AccountResponse" and
"Out.present returns AccountResponse".

Primary ports (In/Out) are use-case boundaries.
Secondary ports (Repo, IdGenerator) are driven by the use case.
"""
from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

from core.entities.account import Account
from core.values.types import AccountId

from features._shared.ports import IOPorts


class AccountGetterPort(IOPorts):
    """
    Use case: fetch an existing account.
    """

    class In(Protocol):
        """
        Input boundary for fetching an account.
        The interactor implements this.
        """

        def execute(self, *, account_id: str) -> "AccountResponse":
            raise NotImplementedError

    class Out(Protocol):
        """
        Output boundary for presenting an account.
        The presenter implements this.
        """

        def present(self, account: Account) -> "AccountResponse":
            raise NotImplementedError


class AccountCreatorPort(IOPorts):
    """
    Use case: create a new account.
    """

    class In(Protocol):
        """
        Input boundary for creating an account.
        """
        def execute(self, *, initial_balance_pence: int | None) -> "AccountResponse":
            raise NotImplementedError

    class Out(Protocol):
        """
        Output boundary for presenting a newly created account.
        """
        def present(self, account: Account) -> "AccountResponse":
            raise NotImplementedError


class AccountRepoPort(Protocol):
    """
    Persistence port for accounts.
    Implemented by infrastructure adapters.
    """

    def get(self, account_id: AccountId) -> Account | None:
        raise NotImplementedError

    def save(self, account: Account) -> None:
        raise NotImplementedError


if TYPE_CHECKING:
    # Import only for typing; avoids runtime coupling / import cycles.
    from features.accounts.schemas import AccountResponse
