import re

MAX_TICKET_LEN = 2000

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_ticket(text: str) -> str:
    """Strip control characters and cap length before text reaches any model."""
    return _CONTROL_CHARS.sub("", text)[:MAX_TICKET_LEN]
