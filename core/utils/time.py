from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Current UTC time.

    Isolated so it can later be replaced by a clock port if needed.
    """
    return datetime.now(tz=timezone.utc)
