import json
from app.config import DISPOSABLE_DOMAINS_FILE

_disposable_domains = None

def load_disposable_domains():
    global _disposable_domains
    if _disposable_domains is None:
        with open(DISPOSABLE_DOMAINS_FILE, "r") as f:
            _disposable_domains = set(json.load(f))
    return _disposable_domains

def is_disposable(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain in load_disposable_domains()
