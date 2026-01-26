"""
Ring: Composition Root (not on the Clean Architecture diagram)

Responsibility:
Defines the application entry point and performs system composition.
This module wires together infrastructure, application, and delivery concerns
into a running FastAPI application.

Design intent:
This is the single place where all layers are allowed to meet.
No business logic lives here. No domain rules live here. No application policy
lives here. It only composes already-defined parts.

This module contains:
- Application bootstrap logic.
- Infrastructure initialisation (database schema, logging).
- Registration of routers and exception handlers.
- The FastAPI app object.
- The uvicorn startup configuration for local execution.

Dependency constraints:
- May depend on all inner layers (infra, features, core).
- Nothing may depend on this module.
- Must not contain business rules, use case logic, or persistence logic.

Stability:
- Highly volatile.
- Changes whenever the delivery mechanism, framework, or wiring strategy changes.

Usage:
- Used as the entry point for running the application.
- Imported by uvicorn to load the ASGI app.
- Acts as the composition root that assembles the entire system.
"""
from __future__ import annotations

from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

# Add project root to sys.path for uvicorn.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.db.session import create_all_db_tables
from root.errors import register_exception_handlers
from root.logging_setup import attach_logger
from root.routers import register_routers


def build_app() -> FastAPI:
    """
    Application entry point.

    Responsibilities:
    - initialise infra (DB schema, logging)
    - register routers
    - register exception handlers
    """
    app = FastAPI()

    # Initialise shared infrastructure
    attach_logger(app)
    create_all_db_tables()

    # Wire application
    register_exception_handlers(app)
    register_routers(app)

    return app

app = build_app()

if __name__ == "__main__":
    uvicorn.run(
        "root.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
