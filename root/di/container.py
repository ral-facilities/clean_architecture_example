# root/di/container.py
from __future__ import annotations

import logging
from dataclasses import dataclass

from infra.logging.logger import build_logger


@dataclass(frozen=True, slots=True)
class Container:
    """
    Application container holding shared concrete adapters.

    For this demo:
    - logger is process-wide and shared
    - DB session remains request-scoped via infra/db/session.get_session
    """

    logger: logging.Logger


def build_container() -> Container:
    return Container(logger=build_logger(name="demo"))
