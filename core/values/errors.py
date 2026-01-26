"""
Ring: Domain (Shared Kernel / Domain Errors)

Responsibility:
Defines the base class for all domain-level exceptions and the concrete errors that
represent violations of business rules.

Design intent:
All domain errors inherit from DomainError so business failures can be treated as a
single category, distinct from technical or infrastructural failures.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).

Stability:
- Highly stable.
- Part of the domain’s public error contract.

Usage:
- Raised by domain entities, value objects, and domain services when invariants are broken.
- Caught by outer layers and translated into protocol-specific errors (HTTP, UI, logs).
"""


class DomainError(Exception):
    """Base class for domain-level errors."""


class InvalidAmountError(DomainError):
    pass


class SameAccountTransferError(DomainError):
    pass


class InsufficientFundsError(DomainError):
    pass
