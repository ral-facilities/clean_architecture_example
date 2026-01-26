"""
Ring: Application (Use Case / Feature Errors)

Responsibility:
Defines application-level errors specific to the Accounts feature.
These represent failures of use case execution or invalid application input, not
violations of core domain rules.

Design intent:
These errors sit between the domain and delivery layers.
They translate domain failures and missing resources into concepts meaningful at
the application boundary, without introducing protocol or framework concerns.

This module contains:
- AccountNotFoundError: raised when a requested account does not exist.
- AccountValidationError: raised when input data is invalid at the application level.

Dependency constraints:
- Must not import from any other feature!
- Must not depend on infrastructure implementations or frameworks directly!
- Must not contain persistence, HTTP, or serialization logic.
- May depend on the Domain layer (core/).
- May depend on shared application contracts in features/_shared.

Stability:
- Highly stable.
- Part of the feature’s public error contract.

Usage:
- Raised by use case interactors.
- Caught and translated by delivery layers into protocol-specific errors (e.g. HTTP responses).
- Serves as the boundary between domain failure and user-visible application failure.
"""

from __future__ import annotations

from features._shared.errors import ApplicationError


class AccountNotFoundError(ApplicationError):
    """Raised when an account ID does not exist."""


class AccountValidationError(ApplicationError):
    """Raised when account input data is invalid for the application."""
