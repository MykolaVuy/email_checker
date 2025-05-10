from app.validators import (
    is_ascii_email,
    is_disposable,
    get_mx_record,
    is_valid_email_format,
    is_smtp_valid,
)

def check_email(email: str) -> str:
    if not is_valid_email_format(email):
        return "invalid (regex)"

    if not is_ascii_email(email):
        return "invalid (non-ascii)"

    if is_disposable(email):
        return "invalid (disposable)"

    mx_host = get_mx_record(email)
    if not mx_host:
        return "invalid (mx-record)"

    if not is_smtp_valid(email, mx_host):
        return "invalid (smtp)"

    return "valid"
