"""
Ring: Domain (Shared Kernel / Value Objects)

Responsibility:
Defines domain-wide enumerations that express fixed, closed sets of valid values.
These enums encode business vocabulary and state that must be consistent everywhere
in the system.

This module contains:
- Currency: the set of currencies recognised by the domain.
- TransferStatus: the lifecycle states a Transfer is allowed to have.

Design intent:
- Enums represent *domain language*, not technical convenience.
- They prevent illegal states by construction.
- They make business rules explicit and self-documenting.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).
- Must not reference databases, frameworks, HTTP, or I/O.

Stability:
- Highly stable.
- Changes here redefine the domain vocabulary and valid state space.

Usage:
- Used by domain entities, value objects, and domain services to express valid states.
- Used by outer layers for persistence, transport, and presentation without redefining meaning.
"""

from enum import Enum


class Currency(str, Enum):
    GBP = "GBP"


class TransferStatus(str, Enum):
    CREATED = "created"
    COMPLETED = "completed"
