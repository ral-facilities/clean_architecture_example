"""
Ring: Infrastructure (Logging)

Responsibility:
Defines the construction and configuration of the application logger.
This module owns how logging is formatted, where it is written, and how loggers are
initialised for use across the system.

Design intent:
Logging is a pure infrastructure concern.
Domain and application layers must be able to log without knowing:
- How logs are formatted
- Where logs are written
- Which handlers are attached
This module centralises that responsibility.

This module contains:
- build_logger: a factory for configured standard-library loggers.

Dependency constraints:
- Must not import from the Domain layer (core/).
- Must not import from the Application layer (features/*).
- May depend only on infrastructure and standard library modules.
- Must not contain business rules or application policy.

Stability:
- Highly volatile.
- Changes when logging format, destinations, or verbosity requirements change.

Usage:
- Called during application startup or wiring.
- The returned logger is injected into interactors and infrastructure components.
- Acts as the single source of truth for logging configuration.
"""

from __future__ import annotations

import logging
from logging import Logger


def build_logger(*, name: str = "demo", level: int = logging.INFO) -> Logger:
    """
    Build and configure the application logger.
    Notes:
    - Safe to call multiple times; handlers are only added once per logger name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
