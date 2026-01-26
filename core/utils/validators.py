"""
Ring: Domain (Shared Utilities)

Responsibility:
Provides minimal, domain-agnostic validation helpers that can be used to express
invariants and preconditions in a concise and intention-revealing way.

This module exists to:
- Centralise simple assertion logic used across the domain and application layers.
- Keep business rules readable without tying them to any specific entity or service.
- Avoid scattering raw `if` / `raise` patterns throughout the codebase.

Design intent:
- These checks are part of expressing domain correctness, not error handling strategy.
- The function is deliberately small and generic so it can be used anywhere without
  architectural coupling.
- It supports the idea that invalid domain states should fail fast and explicitly.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from application (features/), infrastructure (infra/), or delivery (root/).
- Must not reference frameworks, databases, HTTP, or I/O.

Stability:
- Highly stable.
- Its behaviour defines a basic building block for expressing correctness conditions.

Usage:
- Used by domain entities, domain services, and application use cases to assert
  required conditions.
- Acts as a lightweight, expressive alternative to inline assertions or ad-hoc checks.
"""

def require(condition: bool, message: str) -> None:
    """
    Minimal assertion helper for domain checks.
    """
    if not condition:
        raise ValueError(message)
