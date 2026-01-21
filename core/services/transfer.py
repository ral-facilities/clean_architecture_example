"""
Transfer domain services.

Domain rules that coordinate multiple accounts.
"""

from __future__ import annotations

from core.entities.account import Account
from core.entities.transfer import Transfer
from core.services.account import credit_account, debit_account
from core.values.objects import AppliedTransfer


def apply_transfer(
    *, from_account: Account, to_account: Account, transfer: Transfer
) -> AppliedTransfer:
    """
    Apply a transfer to two accounts.
    """
    updated_from = debit_account(account=from_account, amount=transfer.amount)
    updated_to = credit_account(account=to_account, amount=transfer.amount)

    return AppliedTransfer(
        updated_from_account=updated_from,
        updated_to_account=updated_to,
        transfer=transfer,
    )
