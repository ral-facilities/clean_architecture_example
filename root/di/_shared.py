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