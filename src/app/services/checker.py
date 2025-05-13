from app.validators import (
    is_ascii_email,
    is_disposable,
    get_mx_record,
    is_valid_email_format,
    smtp_check,
)

def check_email(email: str) -> str:
    if not is_valid_email_format(email):
        return "invalid|format"

    if not is_ascii_email(email):
        return "invalid|non-ascii"

    if is_disposable(email):
        return "invalid|disposable"

    mx_host = get_mx_record(email)
    if not mx_host:
        return "invalid|mx"

    code, message = smtp_check(email, mx_host)

    if code is None:
        return f"invalid|smtp no-code: {message}"

    if code in (550, 551, 553, 554):
        return f"invalid|smtp hard-bounce|{code}|{message}"

    if code in (421, 450, 451, 452):
        return f"invalid|smtp soft-bounce|{code}|{message}"

    if code in (250, 251):
        return "valid"

    return f"invalid|smtp unknown|{code}|{message}"
