# root/di/__init__.py
from __future__ import annotations

from root.di.accounts import AccountsDeps, build_accounts_deps
from root.di.container import Container, build_container
from root.di.transfers import TransfersDeps, build_transfers_deps

__all__ = [
    "AccountsDeps",
    "TransfersDeps",
    "Container",
    "build_accounts_deps",
    "build_transfers_deps",
    "build_container",
]
