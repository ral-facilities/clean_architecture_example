def require(condition: bool, message: str) -> None:
    """
    Minimal assertion helper for domain checks.
    """
    if not condition:
        raise ValueError(message)
