# infra/db/transfers/model.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.session import ORMBase


class TransferModel(ORMBase):
    """
    ORM model for transfers.
    """

    __tablename__ = "transfers"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    from_account_id: Mapped[str] = mapped_column(String, nullable=False)
    to_account_id: Mapped[str] = mapped_column(String, nullable=False)

    amount_pence: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
