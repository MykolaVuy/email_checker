import os
import re
import ast
from app.config import (
    USER_CONFIG_PATH, MAX_EMAILS_PER_RUN,
    SMTP_FROM, SMTP_TIMEOUT, USE_EHLO,
    EHLO_DOMAIN, USE_RANDOM_FROM,
    CUSTOM_FROM_DOMAIN, DEBUG
)

DEFAULTS = {
    "MAX_EMAILS_PER_RUN": MAX_EMAILS_PER_RUN,
    "SMTP_FROM": SMTP_FROM,
    "SMTP_TIMEOUT": SMTP_TIMEOUT,
    "USE_EHLO": USE_EHLO,
    "EHLO_DOMAIN": EHLO_DOMAIN,
    "USE_RANDOM_FROM": USE_RANDOM_FROM,
    "CUSTOM_FROM_DOMAIN": CUSTOM_FROM_DOMAIN,
    "DEBUG": DEBUG,
}

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?[A-Za-z]{2,}$"
)


def is_valid_email(value: str) -> bool:
    return value == "" or bool(EMAIL_RE.fullmatch(value))


def is_valid_domain(value: str) -> bool:
    return bool(DOMAIN_RE.fullmatch(value))


def is_valid_positive_int_in_range(value: str, min_value: int, max_value: int) -> bool:
    if not value.isdigit():
        return False
    num = int(value)
    return min_value <= num <= max_value and num > 0


def validate_param(key: str, value):
    if key in ("USE_EHLO", "USE_RANDOM_FROM", "DEBUG"):
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean (True/False)")
    elif key == "SMTP_FROM":
        if not isinstance(value, str) or not is_valid_email(value):
            raise ValueError(f"{key} must be a valid email address")
    elif key in ("EHLO_DOMAIN", "CUSTOM_FROM_DOMAIN"):
        if not isinstance(value, str) or (value and not is_valid_domain(value)):
            raise ValueError(f"{key} must be a valid domain")
    elif key == "MAX_EMAILS_PER_RUN":
        if not isinstance(value, int) or not is_valid_positive_int_in_range(str(value), 1, 1000):
            raise ValueError(f"{key} must be an integer between 1 and 1000")
    elif key == "SMTP_TIMEOUT":
        if not isinstance(value, int) or not is_valid_positive_int_in_range(str(value), 1, 60):
            raise ValueError(f"{key} must be an integer between 1 and 60")
    elif key not in DEFAULTS:
        raise ValueError(f"Unknown config key: {key}")


def load_user_config() -> dict:
    config = DEFAULTS.copy()
    if os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, "r") as f:
            for line in f:
                match = re.match(r"^([A-Z_]+)\s*=\s*(.+)$", line.strip())
                if match:
                    key, val = match.groups()
                    try:
                        config[key] = ast.literal_eval(val)
                    except Exception:
                        config[key] = val.strip('"\'')
    return config


def set_user_config_param(key: str, value):
    validate_param(key, value)
    config = load_user_config()
    config[key] = value

    with open(USER_CONFIG_PATH, "w") as f:
        f.write("# User configuration for email-checker-mv\n\n")
        for k, v in config.items():
            val_str = repr(v)
            f.write(f"{k} = {val_str}\n")

    updated_config = load_user_config()
    print(f"✅ User config updated in: {USER_CONFIG_PATH}\n")
    for k, v in updated_config.items():
        print(f"{k} = {repr(v)}")

    return updated_config


def smart_cast(value: str):
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "none":
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def set_user_config_entrypoint():
    import sys
    if len(sys.argv) != 2 or '=' not in sys.argv[1]:
        print("Usage: set-user-config key=value")
        return
    key, value = sys.argv[1].split("=", 1)
    try:
        casted_value = smart_cast(value)
        set_user_config_param(key, casted_value)
    except Exception as e:
        print(f"❌ Error: {e}")


def show_user_config_entrypoint():
    config = load_user_config()
    for k, v in config.items():
        print(f"{k} = {repr(v)}")
