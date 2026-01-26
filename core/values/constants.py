"""
Ring: Domain (Shared Kernel / Domain Constants)

Responsibility:
Defines fundamental domain constants that express global, non-negotiable business
assumptions. These values describe facts about the domain itself rather than behaviour.

This module contains:
- Canonical currency used by the system.
- Absolute minimum monetary constraints that apply everywhere.

Design intent:
- These values represent domain truth, not configuration.
- They are not environment-dependent and must not vary between deployments.
- If one of these changes, the meaning of the domain changes.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).
- Must not reference databases, frameworks, HTTP, or I/O.

Stability:
- Extremely stable.
- Changes here redefine the economic model of the system itself.

Usage:
- Used by value objects, entities, and domain services when enforcing monetary rules.
- Serves as the single source of truth for currency identity and absolute financial limits.
"""

MIN_TRANSFER_AMOUNT_PENCE = 1
CURRENCY = "GBP"
