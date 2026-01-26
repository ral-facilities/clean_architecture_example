"""
Ring: Application (Use Case / Feature Errors)

Responsibility:
Defines application-level errors specific to the Transfers feature.
These represent failures of transfer use case execution (missing resources,
invalid application input, insufficient funds as an application outcome), and are
distinct from low-level technical failures.

Design intent:
These errors translate domain failures into concepts meaningful at the application
boundary, without introducing protocol or framework concerns.

This module contains:
- TransferAccountNotFoundError: a referenced account does not exist.
- TransferValidationError: transfer request is invalid for the application.
- TransferInsufficientFundsError: source account cannot cover the transfer.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on this feature’s own ports, errors, and schemas.
- May depend on shared application contracts in features/_shared.

Stability:
- Highly stable.
- Part of the feature’s public error contract.

Usage:
- Raised by transfer use case interactors.
- Caught by delivery layers and translated into protocol-specific responses.
- Used to keep domain errors from leaking directly into external interfaces.
"""
from __future__ import annotations

from features._shared.errors import ApplicationError


class TransferAccountNotFoundError(ApplicationError):
    """Raised when a transfer references an account ID that does not exist."""


class TransferValidationError(ApplicationError):
    """Raised when transfer input data is invalid for the application."""


class TransferInsufficientFundsError(ApplicationError):
    """Raised when the source account lacks sufficient funds for the transfer."""
