from app.config import MAX_EMAILS_PER_RUN, DEBUG
from app.services import (
    check_email,
    load_emails,
    save_emails
)

def run_batch():
    df = load_emails()
    df_to_check = df[df["status"] == "undefined"].copy()

    if DEBUG:
        print(f"[runner] Before checking: {len(df_to_check)} emails")

    checked = 0
    for idx, row in df_to_check.iterrows():
        if checked >= MAX_EMAILS_PER_RUN:
            break
        email = row["email"]
        result = check_email(email)
        if DEBUG:
            print(f"[runner] {email} → {result}")
        df.at[idx, "status"] = result
        checked += 1

    save_emails(df)

    print(f"✅ Checking {checked} emails.")

if __name__ == "__main__":
    run_batch()
