"""
Account domain services.

Domain rules that act on a single account.
"""

from __future__ import annotations

from core.entities.account import Account
from core.values.errors import InvalidAmountError, InsufficientFundsError
from core.values.objects import Money


def credit_account(*, account: Account, amount: Money) -> Account:
    """
    Increase an account balance by a positive amount.
    """
    if not amount.is_positive():
        raise InvalidAmountError("Credit amount must be positive")

    return Account(
        id=account.id,
        balance=Money(account.balance.pence + amount.pence),
    )


def debit_account(*, account: Account, amount: Money) -> Account:
    """
    Decrease an account balance by a positive amount, if funds allow.
    """
    if not amount.is_positive():
        raise InvalidAmountError("Debit amount must be positive")

    if account.balance.pence < amount.pence:
        raise InsufficientFundsError("Insufficient funds")

    return Account(
        id=account.id,
        balance=Money(account.balance.pence - amount.pence),
    )
