# root/main.py
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
        port=8000,
        reload=True,
    )
