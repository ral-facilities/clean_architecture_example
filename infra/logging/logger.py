from __future__ import annotations

import logging
from logging import Logger

def build_logger(*, name: str = "demo", level: int = logging.INFO) -> Logger:
    """
    Build and configure the application logger.
    Notes:
    - Uses the standard library logging module.
    - Safe to call multiple times; handlers are only added once per logger name.
    - Configuration (handlers/format) is an infrastructure concern.
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
