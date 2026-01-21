from __future__ import annotations

from features._shared.errors import ApplicationError


class AccountNotFoundError(ApplicationError):
    """Raised when an account ID does not exist."""


class AccountValidationError(ApplicationError):
    """Raised when account input data is invalid for the application."""
