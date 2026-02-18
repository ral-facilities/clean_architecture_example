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
- AccountGetterPort: primary In/Out ports for fetching an account.
- AccountCreatorPort: primary In/Out ports for creating an account.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature's own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Highly stable.
- Ports are the contracts that outer layers adapt to; they should change rarely.

Usage:
- Implemented by interactors (In) and presenters (Out) within the feature.
- Implemented by infrastructure adapters for persistence ports.
- Imported by delivery and infrastructure to wire concrete implementations.
"""

from __future__ import annotations

from typing import Protocol

from core.entities.account import Account
from features._shared.ports import IOPorts
from features.accounts.use_cases.models import CreateAccountInput, GetAccountInput


class AccountGetterPort(IOPorts):
    """
    Use case: fetch an existing account.
    """

    class In(Protocol):
        """
        Input boundary for fetching an account.
        The interactor implements this.
        """

        def execute(
            self,
            *,
            account_input: GetAccountInput,
            presenter: AccountGetterPort.Out,
        ) -> None:
            raise NotImplementedError

    class Out(Protocol):
        """
        Output boundary for presenting an account.
        The presenter implements this.
        """

        def present(self, account: Account) -> None:
            raise NotImplementedError


class AccountCreatorPort(IOPorts):
    """
    Use case: create a new account.
    """

    class In(Protocol):
        """
        Input boundary for creating an account.
        The interactor implements this.
        """

        def execute(
            self,
            *,
            account_input: CreateAccountInput,
            presenter: AccountCreatorPort.Out,
        ) -> None:
            raise NotImplementedError

    class Out(Protocol):
        """
        Output boundary for presenting a newly created account.
        The presenter implements this.
        """

        def present(self, account: Account) -> None:
            raise NotImplementedError
