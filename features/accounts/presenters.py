"""
Ring: Interface Adapters (Presenters)

Responsibility:
Defines presenters that adapt domain entities into application-facing response
models. Presenters translate pure domain objects into DTOs that are safe and
convenient for delivery layers to expose.

Design intent:
Presenters isolate formatting and representation concerns from use cases.
Use cases produce domain objects; presenters decide how those objects are shaped
for external consumption. This prevents domain models from leaking into HTTP,
JSON, or UI contracts.

This module contains:
- Presenter implementations for the account-related use cases.
- Mappings from Account domain entities to AccountResponse schemas.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly.
- Must not contain domain or application business rules.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Moderately stable.
- Changes when response representations change, even if use case logic does not.

Usage:
- Called by use case interactors to produce output data.
- Used by delivery layers as the final source of response objects.
- Acts as the boundary between application policy and presentation format.
"""
from __future__ import annotations

from core.entities.account import Account

from features.accounts.ports import AccountGetterPort, AccountCreatorPort
from features.accounts.schemas import AccountResponse


class AccountGetterPresenter(AccountGetterPort.Out):
    """
    Presenter for the get-account use case.
    Converts a domain Account entity into an AccountResponse DTO.
    """

    def present(self, account: Account) -> AccountResponse:
        return AccountResponse(
            id=str(account.id),
            balance_pence=account.balance.pence,
        )


class AccountCreatorPresenter(AccountCreatorPort.Out):
    """
    Presenter for the create-account use case.
    Converts a newly created domain Account entity into an AccountResponse DTO.
    """

    def present(self, account: Account) -> AccountResponse:
        return AccountResponse(
            id=str(account.id),
            balance_pence=account.balance.pence,
        )
