import uuid


def new_id() -> str:
    """
    Generate a new unique identifier.

    Domain-agnostic utility.
    """
    return str(uuid.uuid4())
