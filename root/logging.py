from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, Request

from infra.logging.logger import build_logger


def attach_logger(app) -> None:
    """
    Attach a process-wide logger to app.state.

    This keeps logger initialisation in root while the implementation stays in infra.
    """
    app.state.logger = build_logger(name="demo", level=logging.INFO)


def get_logger(request: Request) -> logging.Logger:
    """
    FastAPI dependency for retrieving the shared application logger.
    """
    return request.app.state.logger


LoggerDep = Annotated[logging.Logger, Depends(get_logger)]