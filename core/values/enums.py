from enum import Enum


class Currency(str, Enum):
    GBP = "GBP"


class TransferStatus(str, Enum):
    CREATED = "created"
    COMPLETED = "completed"
