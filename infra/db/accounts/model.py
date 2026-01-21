from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.session import ORMBase


class AccountModel(ORMBase):
    """
    ORM model for accounts.
    """

    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    balance_pence: Mapped[int] = mapped_column(Integer, nullable=False)
