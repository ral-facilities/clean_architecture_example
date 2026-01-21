# infra/db/accounts/repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.entities.account import Account
from core.values.types import AccountId

from features.accounts.ports import AccountRepoPort

from infra.db.accounts.mapper import to_entity, to_model
from infra.db.accounts.model import AccountModel


class AccountRepo(AccountRepoPort):
    """
    SQLAlchemy-backed AccountRepo.

    This implementation is intentionally simple:
    - `get` and `save` operate within a provided Session.
    - Transaction scoping is managed by infra/db/session.session_scope().
    """

    def __init__(self, *, session: Session) -> None:
        self._session = session

    def get(self, account_id: AccountId) -> Account | None:
        stmt = select(AccountModel).where(AccountModel.id == str(account_id))
        model = self._session.execute(stmt).scalar_one_or_none()
        return None if model is None else to_entity(model)

    def save(self, account: Account) -> None:
        """
        Upsert semantics for the demo.

        If the row exists, update the balance.
        If it does not, insert it.
        """
        existing = self._session.get(AccountModel, str(account.id))
        if existing is None:
            self._session.add(to_model(account))
            return

        existing.balance_pence = account.balance.pence
