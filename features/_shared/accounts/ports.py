from typing import Protocol
from core.entities.account import Account
from core.values.custom_types import AccountId


class AccountRepoPort(Protocol):
    """
    Persistence port for accounts.
    Implemented by infrastructure adapters.
    """

    def get(self, account_id: AccountId) -> Account | None:
        raise NotImplementedError

    def save(self, account: Account) -> None:
        raise NotImplementedError
