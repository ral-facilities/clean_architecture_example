# root/errors.py
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
    async def _account_validation(_: Request, exc: AccountValidationError) -> JSONResponse:
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

