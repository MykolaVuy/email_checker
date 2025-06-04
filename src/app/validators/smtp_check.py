import smtplib
import socket
import uuid
from app.config import (
    SMTP_FROM, SMTP_TIMEOUT, USE_EHLO,
    EHLO_DOMAIN, USE_RANDOM_FROM,
    CUSTOM_FROM_DOMAIN
)

def smtp_check(email: str, mx_host: str) -> tuple[int | None, str]:
    try:
        server = smtplib.SMTP(timeout=SMTP_TIMEOUT)
        server.connect(mx_host)

        if USE_EHLO and EHLO_DOMAIN:
            server.ehlo(EHLO_DOMAIN)
        else:
            server.helo(socket.gethostname())

        if USE_RANDOM_FROM and CUSTOM_FROM_DOMAIN:
            mail_from = f"check-{uuid.uuid4().hex[:6]}@{CUSTOM_FROM_DOMAIN}"
        else:
            mail_from = SMTP_FROM

        server.mail(mail_from)
        code, message = server.rcpt(email)
        server.quit()

        return code, message.decode() if isinstance(message, bytes) else message
    except Exception as e:
        return None, str(e)
