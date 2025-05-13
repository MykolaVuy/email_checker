import smtplib
import socket

from app.config import SMTP_FROM, SMTP_TIMEOUT

def smtp_check(email: str, mx_host: str) -> tuple[int | None, str]:
    try:
        server = smtplib.SMTP(timeout=SMTP_TIMEOUT)
        server.connect(mx_host)
        server.helo(socket.gethostname())
        server.mail(SMTP_FROM)
        code, message = server.rcpt(email)
        server.quit()

        return code, message.decode() if isinstance(message, bytes) else message
    except Exception as e:
        return None, str(e)
