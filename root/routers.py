"""
Ring: Composition Root (not on the Clean Architecture diagram)

Responsibility:
Registers all HTTP routers with the FastAPI application.
This module assembles delivery adapters (routers) and wires them to concrete
dependency providers defined in the root DI layer.

Design intent:
This is pure composition code.
It connects features to their implementations and integrates them into a single
running application, without containing any business or application logic.

This module contains:
- register_routers: the function that attaches all feature routers to the FastAPI app.

Dependency constraints:
- May depend on all inner layers (features, core, infra, root.di).
- Must not be imported by any inner layer.
- Must not contain business rules, use case logic, or domain policy.

Stability:
- Highly volatile.
- Changes whenever new features are added or routing or wiring changes.

Usage:
- Called during application startup from the application root.
- Acts as the central point where all feature routers are assembled.
"""
from __future__ import annotations

from fastapi import FastAPI

from features.accounts.routers import build_account_routers
from features.transfers.routers import build_transfer_routers
from root.di.accounts import get_account_creator, get_account_getter
from root.di.transfers import get_transfer_creator


def register_routers(app: FastAPI) -> None:
    app.include_router(
        build_account_routers(
            account_creator=get_account_creator,
            account_getter=get_account_getter,
        )
    )

    app.include_router(
        build_transfer_routers(
            transfer_creator=get_transfer_creator,
        )
    )
