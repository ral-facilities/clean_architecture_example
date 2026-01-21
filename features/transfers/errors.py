# features/transfers/errors.py
from __future__ import annotations

from features._shared.errors import ApplicationError


class TransferAccountNotFoundError(ApplicationError):
    """Raised when a transfer references an account ID that does not exist."""


class TransferValidationError(ApplicationError):
    """Raised when transfer input data is invalid for the application."""


class TransferInsufficientFundsError(ApplicationError):
    """Raised when the source account lacks sufficient funds for the transfer."""
