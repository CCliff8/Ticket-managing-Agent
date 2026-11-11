import re
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.ticket_triage.config import settings

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def _validate_email(address: str) -> str:
    address = address.strip()
    if not _EMAIL_RE.match(address):
        raise ValueError(f"Invalid email address: {address!r}")
    return address


def _sanitize_header(value: str, max_length: int = 200) -> str:
    """Remove newlines to prevent email header injection."""
    return value.replace("\r", "").replace("\n", "")[:max_length]


def send_email(to: str, subject: str, body: str) -> None:
    to = _validate_email(to)
    subject = _sanitize_header(subject)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = _sanitize_header(settings.email_address)
    msg["To"] = to
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(settings.email_address, settings.email_app_password)
        server.send_message(msg)
