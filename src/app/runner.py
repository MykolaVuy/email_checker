from app.config import MAX_EMAILS_PER_RUN, DEBUG
from app.services import (
    check_email,
    load_emails,
    save_emails
)

def parse_status_verbosity(status: str) -> tuple[bool, str | None]:
    if not status:
        return False, None

    parts = status.lower().strip().split()
    if not parts:
        return False, None

    base = parts[0]
    if base not in ("undefined", "check"):
        return False, None

    verbosity = None
    if len(parts) > 1:
        flag = parts[1]
        if flag in ("s", "short"):
            verbosity = "short"
        elif flag in ("f", "full"):
            verbosity = "full"

    return True, verbosity

def run_batch():
    df = load_emails()
    checked = 0

    for idx, row in df.iterrows():
        if checked >= MAX_EMAILS_PER_RUN:
            break

        status = str(row["status"]).strip().lower()
        should_check, verbosity = parse_status_verbosity(status)
        if not should_check:
            continue

        email = row["email"]
        result = check_email(email, verbosity)

        if DEBUG:
            print(f"[runner] {email} → {result}")

        df.at[idx, "status"] = result
        checked += 1

    save_emails(df)

    print(f"✅ Checked {checked} emails.")

if __name__ == "__main__":
    run_batch()
