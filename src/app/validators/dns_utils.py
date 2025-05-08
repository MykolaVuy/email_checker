import dns.resolver

def get_mx_record(email: str) -> str | None:
    try:
        domain = email.split("@")[-1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return str(mx_records[0].exchange).rstrip('.')
    except Exception:
        return None
