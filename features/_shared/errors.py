class ApplicationError(Exception):
    """
    Base class for application-layer errors (feature/use-case errors).

    Distinct from domain errors in core/.
    """
