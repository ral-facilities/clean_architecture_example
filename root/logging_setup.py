"""
Ring: Composition Root (not on the Clean Architecture diagram)

Responsibility:
Wires the logging infrastructure into the running application.
This module attaches a shared, process-wide logger to the FastAPI app and exposes
it as a dependency for delivery and application layers.

Design intent:
This code belongs to composition, not to logging itself.
It connects:
- The infrastructure logger implementation,
- With the delivery framework (FastAPI),
- By making the logger available through dependency injection.

This module contains:
- attach_logger: bootstraps the logger into the application state.
- get_logger: a FastAPI dependency that retrieves the shared logger.
- LoggerDep: a typed dependency alias for convenient injection.

Dependency constraints:
- May depend on infrastructure (infra.logging).
- May depend on the delivery framework (FastAPI).
- Must not contain business rules or application policy.
- Must not be imported by domain, application, or infrastructure layers.

Stability:
- Highly volatile.
- Changes when logging strategy or dependency wiring changes.

Usage:
- Called at application startup to attach the logger.
- Used by routers and interactors to obtain a configured logger via DI.
- Acts as the bridge between logging infrastructure and the running application.
"""
from __future__ import annotations

import logging
from typing import Annotated
from fastapi import Depends, Request
from infra.logging.logger import build_logger


def attach_logger(app) -> None:
    """
    Attach a process-wide logger to app.state.

    Logger initialisation stays in root; implementation stays in infra.
    """
    app.state.logger = build_logger(name="demo", level=logging.INFO)


def get_logger(request: Request) -> logging.Logger:
    """
    FastAPI dependency for retrieving the shared application logger.
    """
    return request.app.state.logger

LoggerDep = Annotated[logging.Logger, Depends(get_logger)]
