from src.ticket_triage.sanitize import MAX_TICKET_LEN, sanitize_ticket


def test_strips_control_characters_but_keeps_whitespace():
    assert sanitize_ticket("a\x00b\x07c\nd\te") == "abc\nd\te"


def test_caps_length():
    assert len(sanitize_ticket("x" * (MAX_TICKET_LEN + 500))) == MAX_TICKET_LEN
