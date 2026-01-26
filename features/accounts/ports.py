"""
Ring: Application (Use Case Boundaries / Ports)

Responsibility:
Defines the port interfaces for the Accounts feature.
These ports form the stable contracts that isolate use case interactors from outer
details such as persistence and presentation formatting.

Design intent:
- Primary ports (In/Out) define the use case boundary: what the application offers
  and what output it emits.
- Secondary ports (e.g. repositories) define what the use case needs from external
  systems, without importing those systems.
- Dependencies point inwards: interactors implement In, presenters implement Out,
  infrastructure implements repository ports.

This module contains:
- Primary ports for account retrieval and creation (In/Out).
- A secondary persistence port for account storage (repository).

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own errors and ports.
- May depend on shared application contracts in features/_shared.

Stability:
- Highly stable.
- Ports are the contracts that outer layers adapt to; they should change rarely.

Usage:
- Implemented by interactors (In) and presenters (Out) within the feature.
- Implemented by infrastructure adapters for persistence ports.
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
