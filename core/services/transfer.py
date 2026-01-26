"""
Ring: Domain (Enterprise Business Rules)

Responsibility:
Defines domain services for inter-entity operations.
Domain services exist specifically for business rules that cannot belong to a single
entity because they coordinate behaviour across multiple independent entities.

This module expresses the business meaning of applying a Transfer as one coherent,
atomic domain operation involving two Account entities.

Principle:
- If a rule concerns only one entity, it belongs on that entity.
- If a rule coordinates multiple entities, it belongs in a domain service.

It models the rule that:
- A transfer is a coupled transformation of two balances:
  one account is debited and another is credited in a logically inseparable operation.

Dependency constraints:
- May only depend on core entities and core value objects.
- Must never import from features/, infra/, or root/.
- Must not reference persistence, transactions, HTTP, frameworks, or I/O.

Stability:
- Stable business policy.
- Changes here redefine how multiple entities are allowed to interact.

Usage:
- Called by application use cases when a business operation spans multiple entities.
- Produces pure domain results that outer layers may persist or present.
- Serves as the canonical definition of cross-entity business behaviour.
"""
from __future__ import annotations

from core.entities.account import Account
from core.entities.transfer import Transfer
from core.values.objects import AppliedTransfer

def apply_transfer(
    *, from_account: Account, to_account: Account, transfer: Transfer
) -> AppliedTransfer:
    """
    Apply a transfer to two accounts.
    """
    updated_from = from_account.debit(transfer.amount)
    updated_to = to_account.credit(transfer.amount)

    return AppliedTransfer(
        updated_from_account=updated_from,
        updated_to_account=updated_to,
        transfer=transfer,
    )
