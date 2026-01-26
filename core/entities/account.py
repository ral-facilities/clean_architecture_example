"""
Ring: Domain (Enterprise Business Rules)

Responsibility:
This module defines the Account domain entity together with the rules that govern
how an account's balance may change.
An Account represents the authoritative business concept of ownership and balance,
and it owns the legal operations that transform its own state.

It contains:
- Pure domain state (id, balance)
- Invariants that make an Account valid
- Domain behaviour that acts only on a single Account (credit and debit)

It does not contain:
- Persistence logic
- HTTP or API concerns
- Serialization or validation frameworks
- Application workflow or orchestration logic

Dependency constraints:
- Must only depend on other core modules (core.values, core.errors, etc.).
- Must never import from features/, infra/, or root/.
- Must never reference databases, ORMs, web frameworks, or I/O.

Stability:
- This is stable business policy.
- Changes here imply a change in what an Account is and how it is allowed to behave.
- Outer layers must adapt to this model, never the reverse.

Usage:
- Created and manipulated by application use cases to express valid domain state.
- Owns its own balance-changing behaviour for single-entity operations.
- Treated by infrastructure as opaque business data to persist or restore.
- Serves as the single source of truth for what an Account is and how it may change.
"""
from __future__ import annotations

from dataclasses import dataclass

from core.values.errors import InvalidAmountError, InsufficientFundsError
from core.values.objects import Money
from core.values.types import AccountId


@dataclass(slots=True)
class Account:
    id: AccountId
    balance: Money

    def __post_init__(self) -> None:
        if not self.balance.is_positive():
            raise InvalidAmountError("Account balance must be positive")

    def credit(self, amount: Money) -> Account:
        if not amount.is_positive():
            raise InvalidAmountError("Credit amount must be positive")

        return Account(
            id=self.id,
            balance=Money(self.balance.pence + amount.pence),
        )

    def debit(self, amount: Money) -> Account:
        if not amount.is_positive():
            raise InvalidAmountError("Debit amount must be positive")

        if self.balance.pence < amount.pence:
            raise InsufficientFundsError("Insufficient funds")

        return Account(
            id=self.id,
            balance=Money(self.balance.pence - amount.pence),
        )
