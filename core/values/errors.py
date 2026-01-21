class DomainError(Exception):
    """Base class for domain-level errors."""

class InvalidAmountError(DomainError):
    pass

class SameAccountTransferError(DomainError):
    pass

class InsufficientFundsError(DomainError):
    pass
