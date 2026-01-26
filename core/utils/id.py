"""
Ring: Domain (Shared Utilities)

Responsibility:
Provides small, domain-agnostic utilities that are safe to use across the entire
application. These helpers do not encode business meaning themselves and do not
belong to any specific domain concept. They exist to support both the core layer
and all outer layers with neutral, reusable functionality.

This module defines:
- Generic utilities that are not tied to Accounts, Transfers, or any business rule.
- Pure helper functions that remain meaningful outside the domain model.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from features/, infra/, or root/.
- Must not reference databases, frameworks, HTTP, or I/O.

Stability:
- Highly stable.
- Changes here affect many layers, so the API should remain minimal and conservative.

Usage:
- Used by core to support domain object creation.
- May also be used freely by application, infrastructure, and root layers.
- Serves as a neutral utility layer that introduces no architectural coupling.
"""
import uuid


def new_id() -> str:
    """
    Generate a new unique identifier.

    Domain-agnostic utility.
    """
    return str(uuid.uuid4())
