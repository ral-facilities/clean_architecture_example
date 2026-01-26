from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
Provider = Callable[..., T]
