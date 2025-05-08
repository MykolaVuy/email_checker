def is_ascii_email(email: str) -> bool:
    try:
        email.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False
