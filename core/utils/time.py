"""
Ring: Domain (Shared Utilities)

Responsibility:
Provides a centralised, domain-agnostic source of the current time in UTC.
This function isolates time acquisition so that the rest of the system never
depends directly on system clocks.

This module defines:
- A single, canonical way to obtain the current UTC datetime.

Design intent:
- Time is an external dependency in disguise.
- By funnelling it through a single function, the system can later replace this
 with a clock port, mock, or deterministic time source without touching domain
 or application logic.

Dependency constraints:
- Must only depend on the Python standard library.
- Must never import from features/, infra/, or root/.
- Must not reference databases, frameworks, HTTP, or I/O.

Stability:
- Highly stable.
- Its existence protects the system from widespread refactors when time handling
 becomes more sophisticated.

Usage:
- Used by core, application, and infrastructure layers wherever the current time
 is required.
- Acts as the system’s single source of truth for “now”.
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Current UTC time.

    Isolated so it can later be replaced by a clock port if needed.
    """
    return datetime.now(tz=timezone.utc)
