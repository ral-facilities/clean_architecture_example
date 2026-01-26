"""
Ring: Composition Root

Responsibility:
Registers all exception-to-HTTP mappings for the application.
This module defines how domain and application errors are translated into concrete
HTTP responses for the delivery layer.

Design intent:
This is pure boundary adaptation.
It connects:
- Domain and application error types,
- To HTTP status codes and response formats,
- Without letting HTTP concepts leak into inner layers.

Neither the domain nor the application knows anything about status codes,
JSON responses, or FastAPI. All protocol-specific error handling lives here.

This module contains:
- register_exception_handlers: a function that binds exception handlers to FastAPI.
- A standard JSON error response factory for consistent formatting.

Dependency constraints:
- May depend on all inner layers (core, features, infra).
- May depend on the delivery framework (FastAPI).
- Must not be imported by any inner layer.
- Must not contain business rules or application logic.

Stability:
- Highly volatile.
- Changes whenever error semantics, HTTP mapping, or response format changes.

Usage:
- Called during application startup from the composition root.
- Acts as the single place where exception semantics are bound to HTTP semantics.
- Ensures a consistent error contract for all API endpoints.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.values.errors import DomainError
from features._shared.errors import ApplicationError
from features.accounts.errors import AccountNotFoundError, AccountValidationError
from features.transfers.errors import (
    TransferAccountNotFoundError,
    TransferInsufficientFundsError,
    TransferValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Map domain and application exceptions to HTTP responses.

    Routers do not catch exceptions. Everything bubbles here.
    """

    @app.exception_handler(DomainError)
    async def _domain_error(_: Request, exc: DomainError) -> JSONResponse:
        """
        Safety net: all DomainErrors become 400 by default.
        """
        return _json_error(400, exc)

    @app.exception_handler(ApplicationError)
    async def _application_error(_: Request, exc: ApplicationError) -> JSONResponse:
        """
        Safety net: any other ApplicationError becomes 400 by default.
        """
        return _json_error(400, exc)

    @app.exception_handler(AccountNotFoundError)
    async def _account_not_found(_: Request, exc: AccountNotFoundError) -> JSONResponse:
        return _json_error(404, exc)

    @app.exception_handler(TransferAccountNotFoundError)
    async def _transfer_account_not_found(
        _: Request, exc: TransferAccountNotFoundError
    ) -> JSONResponse:
        return _json_error(404, exc)

    @app.exception_handler(AccountValidationError)
    async def _account_validation(
        _: Request, exc: AccountValidationError
    ) -> JSONResponse:
        return _json_error(400, exc)

    @app.exception_handler(TransferValidationError)
    async def _transfer_validation(
        _: Request, exc: TransferValidationError
    ) -> JSONResponse:
        return _json_error(400, exc)

    @app.exception_handler(TransferInsufficientFundsError)
    async def _transfer_insufficient_funds(
        _: Request, exc: TransferInsufficientFundsError
    ) -> JSONResponse:
        return _json_error(409, exc)


def _json_error(status_code: int, exc: Exception) -> JSONResponse:
    """
    Standard JSON error response factory.

    Keeps error response formatting consistent across the application.
    """
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )
