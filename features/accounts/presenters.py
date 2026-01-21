# features/accounts/presenters.py
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
