# root/main.py
from __future__ import annotations

from fastapi import FastAPI

from infra.db.session import create_all_db_tables
from root.errors import register_exception_handlers
from root.logging import attach_logger
from root.routers import register_routers
from root.di.container import build_container


def build_app() -> FastAPI:
    """
    Application entry point.

    Responsibilities:
    - initialise infra (DB schema, logging)
    - build the application container
    - register routers
    - register exception handlers
    """
    app = FastAPI()

    # Initialise shared infrastructure
    attach_logger(app)
    create_all_db_tables()

    # Build application container (process-wide singletons)
    container = build_container()

    # Register routers with wired dependencies
    register_exception_handlers(app)
    register_routers(app, container=container)

    return app


app = build_app()
