"""
Ring: Composition Root

Responsibility:
Defines the per-request runtime context for the application.
This module assembles low-level infrastructure resources into a single object that
can be injected wherever a complete request-scoped context is needed.

Design intent:
This is pure composition and wiring.
It bundles:
- The database session,
- The shared application logger,
into a single immutable RequestContext object.
This avoids passing multiple independent dependencies through every constructor
and keeps request-scoped state explicit.

This module contains:
- RequestContext: an immutable container for per-request infrastructure resources.
- get_ctx: a FastAPI dependency that builds the RequestContext.
- SessionDep: a dependency alias for obtaining a database session.
- ContextDep: a dependency alias for obtaining the full request context.

Dependency constraints:
- May depend on infrastructure (database session, logging).
- May depend on the delivery framework (FastAPI).
- Must not be imported by domain or application layers.
- Must not contain business rules or application policy.

Stability:
- Highly volatile.
- Changes when request-scoped resources or wiring strategy changes.

Usage:
- Used by dependency wiring modules in root/di.
- Provides a single, explicit object that carries all request-scoped infrastructure.
- Acts as the bridge between FastAPI's request lifecycle and the application's needs.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from infra.db.session import get_session


@dataclass(frozen=True, slots=True)
class RequestContext:
    session: Session
    logger: logging.Logger


def get_ctx(session: SessionDep, request: Request) -> RequestContext:
    if not hasattr(request.app.state, "logger"):
        raise RuntimeError("Logger not attached")

    return RequestContext(
        session=session,
        logger=request.app.state.logger,
    )


SessionDep = Annotated[Session, Depends(get_session)]
ContextDep = Annotated[RequestContext, Depends(get_ctx)]
