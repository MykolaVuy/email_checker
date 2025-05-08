import smtplib
import socket

from app.config import SMTP_FROM, SMTP_TIMEOUT

def is_smtp_valid(email: str, mx_host: str) -> bool:
    try:
        server = smtplib.SMTP(timeout=SMTP_TIMEOUT)
        server.connect(mx_host)
        server.helo(socket.gethostname())
        server.mail(SMTP_FROM)
        code, _ = server.rcpt(email)
        server.quit()

        return code in (250, 251)
    except Exception:
        return False
