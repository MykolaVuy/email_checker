import re
from app.validators import (
    is_ascii_email,
    is_disposable,
    get_mx_record,
    is_valid_email_format,
    smtp_check,
)

def check_email(email: str, verbosity: str | None = None) -> str:
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

    if code in (250, 251):
        return "valid"

    return format_response(code, message, verbosity)


def format_response(code: int | None, message: str | None, verbosity: str | None = None) -> str:
    if code is None:
        category = "no-code"
        cat_short = "NC"
    elif code in (550, 551, 553, 554, 521, 540):
        category = "hard-bounce"
        cat_short = "HB"
    elif code in (421, 450, 451, 452, 552):
        category = "soft-bounce"
        cat_short = "SB"
    elif code in (503, 504, 530, 534, 535):
        category = "protocol-error"
        cat_short = "PE"
    else:
        category = "unknown"
        cat_short = "UN"

    def clean(val):
        return "" if val in (None, "None") else str(val).strip()

    if verbosity == "short":
        short_msg = ""
        if message:
            match = re.search(r'^.*?[.!?](?:\s|$)', message.strip())
            short_msg = match.group(0).strip() if match else message.strip().splitlines()[0].strip()[:120]
        parts = ["invalid|smtp", category, clean(code), clean(short_msg)]
        return "|".join(parts).replace("||", "|")

    elif verbosity == "full":
        parts = ["invalid|smtp", category, clean(code), clean(message)]
        return "|".join(parts).replace("||", "|")

    else:  # default
        parts = ["invalid|smtp", cat_short, clean(code)]
        return " ".join(parts)
