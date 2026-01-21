# root/main.py
from __future__ import annotations

from fastapi import FastAPI

from infra.db.session import create_all_db_tables
from root.errors import register_exception_handlers
from root.logging import attach_logger
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
