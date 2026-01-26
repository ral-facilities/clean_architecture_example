"""
Ring: Domain (Shared Kernel / Value Types)

Responsibility:
Defines strongly-typed identifiers used by domain entities.
These types give semantic meaning to otherwise primitive values and prevent
accidental mixing of unrelated identifiers.

Design intent:
- AccountId and TransferId are distinct domain concepts, even though both are strings.
- Using explicit types makes illegal states and invalid assignments harder to express.
- They encode domain meaning without adding behaviour or lifecycle.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).

Stability:
- Highly stable.
- Changes here redefine how identity is represented in the domain.

Usage:
- Used by domain entities to express identity.
- Used by outer layers as opaque identifiers without redefining their meaning.
"""

from typing import NewType

AccountId = NewType("AccountId", str)
TransferId = NewType("TransferId", str)
