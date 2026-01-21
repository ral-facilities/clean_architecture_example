from __future__ import annotations

from abc import ABC
from typing import Any


class IOPorts(ABC):
    """
    Abstract base for use-case I/O port groups.

    Any subclass must define:
    - In: a Protocol representing the input port
    - Out: a Protocol representing the output port
    """

    In: type[Any]
    Out: type[Any]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls is IOPorts:
            return

        if not hasattr(cls, "In") or not isinstance(getattr(cls, "In"), type):
            raise TypeError(f"{cls.__name__} must define a nested class 'In'")

        if not hasattr(cls, "Out") or not isinstance(getattr(cls, "Out"), type):
            raise TypeError(f"{cls.__name__} must define a nested class 'Out'")
